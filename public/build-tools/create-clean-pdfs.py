#!/usr/bin/env python3
"""
Professional PDF Generator for RAPS Marketing Materials
Creates clean, A4-formatted PDFs without emoji dependencies
"""

import os
import re
import subprocess
import sys
from pathlib import Path

def clean_markdown_for_pdf(content):
    """Remove emojis and clean markdown for PDF generation"""
    
    # Remove emoji characters
    emoji_pattern = re.compile("["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    content = emoji_pattern.sub('', content)
    
    # Clean up headers - remove emoji and clean formatting
    content = re.sub(r'#{1,6}\s*[^\w\s]*\s*([^#\n]+)', r'# \1', content)
    
    # Clean bullet points
    content = re.sub(r'^\s*[-*]\s*[^\w\s]*\s*(.+)', r'- \1', content, flags=re.MULTILINE)
    
    # Fix table headers
    content = re.sub(r'\|\s*\*\*([^*]+)\*\*\s*\|', r'| **\1** |', content)
    
    # Clean excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    
    return content

def generate_pdf(input_file, output_name, title, subtitle, version):
    """Generate PDF using pandoc with clean content"""
    
    print(f"📄 Processing: {input_file.name}")
    print(f"   Output: {output_name}.pdf")
    
    # Read and clean content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove YAML frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Clean content
    content = clean_markdown_for_pdf(content)
    
    # Create temp file
    temp_file = input_file.parent / f"{output_name}_clean.md"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Generate PDF with pandoc
    cmd = [
        'pandoc',
        str(temp_file),
        '-o', str(output_dir / f"{output_name}.pdf"),
        '--pdf-engine=pdflatex',
        f'--variable=title:{title}',
        f'--variable=subtitle:{subtitle}',
        f'--variable=version:{version}',
        '--variable=geometry:margin=0.75in',
        '--variable=fontsize:10pt',
        '--variable=papersize:a4',
        '--highlight-style=tango',
        '--table-of-contents',
        '--number-sections'
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        if (output_dir / f"{output_name}.pdf").exists():
            size = (output_dir / f"{output_name}.pdf").stat().st_size
            size_mb = size / (1024 * 1024)
            print(f"✅ Generated: {output_name}.pdf ({size_mb:.1f}MB)")
            success_count[0] += 1
        else:
            print(f"❌ Failed: {output_name}.pdf")
    except subprocess.CalledProcessError as e:
        print(f"❌ Pandoc error: {e}")
        print(f"   Stderr: {e.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up temp file
        if temp_file.exists():
            temp_file.unlink()

# Configuration
script_dir = Path(__file__).parent
project_dir = script_dir.parent
pdf_ready_dir = project_dir / "pdf-ready"
output_dir = project_dir / "pdfs"

# Create output directory
output_dir.mkdir(exist_ok=True)

# Track success
success_count = [0]

print("🚀 RAPS Professional PDF Generator (Python + Pandoc)")
print("=" * 55)

# Check pandoc availability
try:
    subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
    print("✅ Pandoc found")
except (subprocess.CalledProcessError, FileNotFoundError):
    print("❌ Pandoc not found. Please install pandoc.")
    sys.exit(1)

print("\n📚 Generating clean, professional PDFs...")

# Documents to process
documents = [
    {
        'file': pdf_ready_dir / 'aps-cheatsheet-pdf.md',
        'output': 'aps-cheatsheet',
        'title': 'APS Developer Cheat Sheet',
        'subtitle': 'Single-page reference for Autodesk Platform Services APIs',
        'version': 'RAPS v4.2.1 | January 2026'
    },
    {
        'file': pdf_ready_dir / 'error-codes-pdf.md',
        'output': 'aps-error-codes-reference',
        'title': 'APS API Error Codes Reference',
        'subtitle': 'Complete troubleshooting guide for Autodesk Platform Services',
        'version': 'RAPS v4.2.1 | January 2026'
    },
    {
        'file': pdf_ready_dir / 'forge-migration-pdf.md',
        'output': 'forge-to-aps-migration-guide',
        'title': 'Forge to APS Migration Guide',
        'subtitle': 'Complete step-by-step migration walkthrough',
        'version': 'RAPS v4.2.1 | Migration deadline: December 31, 2026'
    }
]

# Additional documents from main repository
additional_docs = [
    {
        'file': project_dir / 'cheatsheets' / 'raps-developer-quickstart.md',
        'output': 'raps-developer-quickstart',
        'title': 'RAPS Developer Quick Start Guide',
        'subtitle': 'Get started with RAPS CLI for APS automation',
        'version': 'RAPS v4.2.1 | January 2026'
    },
    {
        'file': project_dir / 'developer-resources' / 'references' / 'oauth-scopes.md',
        'output': 'aps-oauth-scopes-reference',
        'title': 'APS OAuth Scopes Reference',
        'subtitle': 'Complete guide to OAuth scopes and permissions',
        'version': 'RAPS v4.2.1 | January 2026'
    }
]

# Process all documents
all_docs = documents + additional_docs

for doc in all_docs:
    if doc['file'].exists():
        generate_pdf(
            doc['file'],
            doc['output'],
            doc['title'],
            doc['subtitle'],
            doc['version']
        )
    else:
        print(f"⚠️  Skipping missing file: {doc['file']}")

# Summary
print(f"\n🎉 PDF generation completed!")
print("=" * 40)
print(f"📁 Output directory: {output_dir}")
print(f"✅ Successfully generated: {success_count[0]} PDFs")
print()

if list(output_dir.glob("*.pdf")):
    print("Generated PDFs:")
    for pdf in sorted(output_dir.glob("*.pdf")):
        size = pdf.stat().st_size / (1024 * 1024)
        print(f"  📄 {pdf.name} ({size:.1f}MB)")
else:
    print("❌ No PDFs were generated successfully")

print()
print("💡 Pro Tips:")
print("  • PDFs are optimized for A4 printing")
print("  • Clean, professional layout without emojis") 
print("  • Include RAPS branding and version info")
print("  • Ready for conferences and distribution")

print()
print("📤 Next Steps:")
print("  • Upload to GitHub releases")
print("  • Add to marketing press kit")
print("  • Share on social media")
print("  • Include in workshop materials")