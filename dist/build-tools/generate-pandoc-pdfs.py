#!/usr/bin/env python3
"""
Professional PDF Generator for RAPS Marketing Materials
Enhanced version with proper TOC, metadata, and branding
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def clean_markdown_for_pdf(content):
    """Clean markdown and fix empty bullets"""
    
    # Remove emoji characters
    emoji_pattern = re.compile("["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    content = emoji_pattern.sub('', content)
    
    # Fix headers - preserve proper hierarchy
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Fix bullet points - remove empty bullets and emoji prefixes
        if re.match(r'^\s*[-*+]\s*([^\w\s]*\s*)?(.+)', line):
            indent = len(line) - len(line.lstrip())
            bullet_match = re.match(r'^\s*[-*+]\s*([^\w\s]*\s*)?(.+)', line)
            if bullet_match:
                bullet_content = bullet_match.group(2).strip()
                if bullet_content and bullet_content != '':  # Only add non-empty bullets
                    cleaned_lines.append(' ' * indent + '- ' + bullet_content)
        # Fix headers - remove emoji prefixes
        elif line.strip().startswith('#'):
            header_match = re.match(r'^(\s*#+)\s*([^\w\s]*\s*)?(.+)', line)
            if header_match:
                header_level = header_match.group(1)
                header_text = header_match.group(3).strip()
                if header_text:
                    cleaned_lines.append(header_level + ' ' + header_text)
        else:
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    # Clean excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    
    return content

def create_yaml_header(title, subtitle, version, revision):
    """Create proper YAML header with metadata"""
    
    return f"""---
title: "{title}"
subtitle: "{subtitle}"
author: "RAPS Development Team"
date: "{datetime.now().strftime('%B %Y')}"
version: "{version}"
revision: "{revision}"
subject: "Autodesk Platform Services Developer Resource"
keywords: "APS, Autodesk, Platform Services, RAPS, CLI, API, Developer Tools"
creator: "RAPS PDF Generator"
producer: "RAPS Marketing Team - rapscli.xyz"
toc-title: "Table of Contents"
geometry: margin=0.75in
papersize: a4
fontsize: 10pt
documentclass: article
classoption: oneside
header-includes: |
  \\usepackage{{fancyhdr}}
  \\usepackage{{lastpage}}
  \\usepackage{{xcolor}}
  \\usepackage{{graphicx}}
  \\definecolor{{rapsblue}}{{RGB}}{{102,126,234}}
  \\definecolor{{rapsgray}}{{RGB}}{{108,117,125}}
  \\pagestyle{{fancy}}
  \\fancyhf{{}}
  \\fancyhead[L]{{\\small\\textcolor{{rapsgray}}{{{title}}}}}
  \\fancyhead[R]{{\\small\\textcolor{{rapsgray}}{{RAPS v{version}}}}}
  \\fancyfoot[L]{{\\small\\textcolor{{rapsgray}}{{Generated: {datetime.now().strftime('%B %Y')}}}}}
  \\fancyfoot[C]{{\\small\\textcolor{{rapsgray}}{{rapscli.xyz}}}}
  \\fancyfoot[R]{{\\small\\textcolor{{rapsgray}}{{Page \\thepage\\ of \\pageref{{LastPage}}}}}}
  \\renewcommand{{\\headrulewidth}}{{0.4pt}}
  \\renewcommand{{\\footrulewidth}}{{0.4pt}}
---

"""

def generate_enhanced_pdf(input_file, output_name, title, subtitle, version, revision="1.0"):
    """Generate PDF with proper structure and metadata"""
    
    print(f"📄 Processing: {input_file.name}")
    print(f"   Title: {title}")
    print(f"   Version: {version} | Revision: {revision}")
    
    try:
        # Read content
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove existing YAML frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Clean content
        content = clean_markdown_for_pdf(content)
        
        # Create enhanced temp file with proper YAML header
        temp_file = input_file.parent / f"{output_name}_enhanced.md"
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(create_yaml_header(title, subtitle, version, revision))
            f.write(content)
        
        # Generate PDF with enhanced pandoc options
        cmd = [
            'pandoc',
            str(temp_file),
            '-o', str(output_dir / f"{output_name}.pdf"),
            '--pdf-engine=pdflatex',
            '--table-of-contents',
            '--toc-depth=3',
            '--number-sections',
            '--highlight-style=tango',
            '--standalone',
            '--variable=colorlinks:true',
            '--variable=linkcolor:blue',
            '--variable=urlcolor:blue',
            '--variable=toccolor:blue'
        ]
        
        print(f"   Running: pandoc with enhanced options...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120)
        
        # Check if PDF was created
        output_path = output_dir / f"{output_name}.pdf"
        if output_path.exists():
            size = output_path.stat().st_size
            size_mb = size / (1024 * 1024)
            print(f"✅ Generated: {output_name}.pdf ({size_mb:.1f}MB)")
            
            # Copy to docs directory for GitHub Pages
            docs_pdf_dir = project_dir / "docs" / "pdfs"
            docs_pdf_dir.mkdir(exist_ok=True)
            
            docs_output = docs_pdf_dir / f"{output_name}.pdf"
            with open(output_path, 'rb') as src, open(docs_output, 'wb') as dst:
                dst.write(src.read())
            print(f"   📋 Copied to: docs/pdfs/{output_name}.pdf")
            
            success_count[0] += 1
        else:
            print(f"❌ Failed: {output_name}.pdf not created")
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout generating {output_name}.pdf - file may be too complex")
    except subprocess.CalledProcessError as e:
        print(f"❌ Pandoc error for {output_name}: {e}")
        print(f"   Stderr: {e.stderr}")
    except Exception as e:
        print(f"❌ Error generating {output_name}: {e}")
    finally:
        # Clean up temp file
        temp_file = input_file.parent / f"{output_name}_enhanced.md"
        if temp_file.exists():
            temp_file.unlink()

# Configuration
script_dir = Path(__file__).parent
project_dir = script_dir.parent
pdf_ready_dir = project_dir / "pdf-ready"
output_dir = project_dir / "pdfs"

# Create output directories
output_dir.mkdir(exist_ok=True)
(project_dir / "docs" / "pdfs").mkdir(parents=True, exist_ok=True)

# Track success
success_count = [0]

print("🚀 RAPS Professional PDF Generator v2.0")
print("=" * 55)
print("✨ Features:")
print("   • Multi-level clickable table of contents")
print("   • Professional headers/footers with RAPS branding")
print("   • Document metadata and versioning")
print("   • Clean bullet points (no empty bullets)")
print("   • A4 optimized layout")
print()

# Check pandoc
try:
    result = subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
    print("✅ Pandoc available")
except (subprocess.CalledProcessError, FileNotFoundError):
    print("❌ Pandoc not found. Please install pandoc.")
    sys.exit(1)

print("\n📚 Generating professional PDFs...")

# Document definitions with proper versioning
documents = [
    {
        'file': pdf_ready_dir / 'aps-cheatsheet-pdf.md',
        'output': 'aps-cheatsheet',
        'title': 'APS Developer Cheat Sheet',
        'subtitle': 'Single-page reference for Autodesk Platform Services APIs',
        'version': '4.2.1',
        'revision': '2.1'
    },
    {
        'file': pdf_ready_dir / 'error-codes-pdf.md',
        'output': 'aps-error-codes-reference',
        'title': 'APS API Error Codes Reference',
        'subtitle': 'Complete troubleshooting guide for Autodesk Platform Services',
        'version': '4.2.1',
        'revision': '1.8'
    },
    {
        'file': pdf_ready_dir / 'forge-migration-pdf.md',
        'output': 'forge-to-aps-migration-guide',
        'title': 'Forge to APS Migration Guide',
        'subtitle': 'Complete step-by-step migration walkthrough',
        'version': '4.2.1',
        'revision': '1.5'
    },
    {
        'file': project_dir / 'cheatsheets' / 'raps-developer-quickstart.md',
        'output': 'raps-developer-quickstart',
        'title': 'RAPS Developer Quick Start Guide',
        'subtitle': 'Get started with RAPS CLI for APS automation',
        'version': '4.2.1',
        'revision': '3.2'
    }
]

# Process documents
for doc in documents:
    if doc['file'].exists():
        generate_enhanced_pdf(
            doc['file'],
            doc['output'],
            doc['title'],
            doc['subtitle'],
            doc['version'],
            doc['revision']
        )
        print()  # Add spacing between documents
    else:
        print(f"⚠️  File not found: {doc['file']}")

# Summary
print("🎉 PDF generation completed!")
print("=" * 40)
print(f"📁 Output directory: {output_dir}")
print(f"📁 GitHub Pages: docs/pdfs/")
print(f"✅ Successfully generated: {success_count[0]} PDFs")

if success_count[0] > 0:
    print("\n📋 Generated PDFs:")
    for pdf in sorted(output_dir.glob("*.pdf")):
        size = pdf.stat().st_size / (1024 * 1024)
        print(f"  📄 {pdf.name} ({size:.1f}MB)")

print("\n🎨 Enhanced Features Applied:")
print("  ✓ Multi-level table of contents with clickable links")
print("  ✓ Document metadata (title, author, version, keywords)")
print("  ✓ Professional headers with RAPS branding")
print("  ✓ Footers with rapscli.xyz and page numbers") 
print("  ✓ Clean bullet points (empty bullets removed)")
print("  ✓ Proper section numbering and hierarchy")
print("  ✓ A4 page layout with professional margins")
print("  ✓ Version and revision tracking")

print("\n📤 Ready for:")
print("  • GitHub Pages distribution")
print("  • Conference and workshop handouts")
print("  • Professional presentations")
print("  • Marketing press kit inclusion")