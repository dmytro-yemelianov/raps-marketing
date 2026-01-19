#!/usr/bin/env python3
"""
Generate all PDFs and organize them in docs folder for GitHub Pages
Uses multiple approaches based on what's available
"""

import os
import subprocess
import shutil
from pathlib import Path

def ensure_docs_structure():
    """Ensure proper directory structure in docs"""
    docs_dirs = [
        'docs/pdfs',
        'docs/pdfs/latex',
        'docs/pdfs/infographics',
        'docs/infographics'
    ]
    
    for dir_path in docs_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Ensured directory: {dir_path}")

def generate_with_pandoc():
    """Generate PDFs using pandoc (markdown to PDF)"""
    print("\n📚 Generating PDFs with Pandoc...")
    
    # Run the existing pandoc script
    pandoc_script = Path('generate-pandoc-pdfs.py')
    if pandoc_script.exists():
        try:
            subprocess.run(['python', str(pandoc_script)], timeout=60)
            print("✅ Pandoc PDFs generated")
        except Exception as e:
            print(f"⚠️  Pandoc generation failed: {e}")

def copy_web_layouts():
    """Copy web layouts to docs for browser access"""
    print("\n🌐 Copying web layouts to docs...")
    
    web_layouts = Path('web-layouts')
    docs_infographics = Path('../docs/infographics')
    
    if web_layouts.exists():
        for html_file in web_layouts.glob('*.html'):
            dest = docs_infographics / html_file.name
            shutil.copy2(html_file, dest)
            print(f"✅ Copied: {html_file.name} → docs/infographics/")

def copy_latex_sources():
    """Copy LaTeX sources to docs for reference"""
    print("\n📄 Copying LaTeX sources to docs...")
    
    latex_dir = Path('latex')
    docs_latex = Path('../docs/pdfs/latex')
    
    if latex_dir.exists():
        for tex_file in latex_dir.glob('*.tex'):
            dest = docs_latex / tex_file.name
            shutil.copy2(tex_file, dest)
            print(f"✅ Copied: {tex_file.name} → docs/pdfs/latex/")

def create_index_page():
    """Create an index page for all PDF resources"""
    print("\n📝 Creating index page...")
    
    index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAPS Marketing PDFs and Infographics</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 {
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        h2 {
            color: #764ba2;
            margin-top: 30px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .card {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .card h3 {
            margin-top: 0;
            color: #1a202c;
        }
        .card p {
            color: #64748b;
            font-size: 14px;
        }
        a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        a:hover {
            text-decoration: underline;
        }
        .button {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            margin-top: 10px;
        }
        .button:hover {
            background: #5a67d8;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌼 RAPS Marketing PDFs & Infographics</h1>
        
        <h2>📄 Professional PDFs</h2>
        <div class="grid">
            <div class="card">
                <h3>APS Cheat Sheet</h3>
                <p>Single-page API reference with RAPS shortcuts</p>
                <a href="pdfs/aps-cheatsheet.pdf" class="button">Download PDF</a>
            </div>
            <div class="card">
                <h3>Error Codes Reference</h3>
                <p>Complete troubleshooting guide</p>
                <a href="pdfs/aps-error-codes-reference.pdf" class="button">Download PDF</a>
            </div>
            <div class="card">
                <h3>OAuth Scopes Guide</h3>
                <p>OAuth scopes and permissions reference</p>
                <a href="pdfs/aps-oauth-scopes-reference.pdf" class="button">Download PDF</a>
            </div>
            <div class="card">
                <h3>Migration Guide</h3>
                <p>Forge to APS migration walkthrough</p>
                <a href="pdfs/forge-to-aps-migration-guide.pdf" class="button">Download PDF</a>
            </div>
            <div class="card">
                <h3>Developer Quick Start</h3>
                <p>Get started with RAPS CLI</p>
                <a href="pdfs/raps-developer-quickstart.pdf" class="button">Download PDF</a>
            </div>
        </div>
        
        <h2>🎨 Interactive Infographics</h2>
        <p>View these in your browser, then print to PDF for high-quality output</p>
        <div class="grid">
            <div class="card">
                <h3>Token Cost Calculator</h3>
                <p>Beautiful infographic showing APS pricing</p>
                <a href="infographics/token-cost-infographic.html" class="button">View Infographic</a>
            </div>
            <div class="card">
                <h3>OAuth Flow Diagram</h3>
                <p>Visual guide to 3-legged authentication</p>
                <a href="infographics/oauth-flow-diagram.html" class="button">View Infographic</a>
            </div>
        </div>
        
        <h2>📐 LaTeX Sources</h2>
        <p>Professional LaTeX documents for precise PDF generation</p>
        <div class="grid">
            <div class="card">
                <h3>APS Cheat Sheet (LaTeX)</h3>
                <p>3-column landscape layout with TikZ diagrams</p>
                <a href="pdfs/latex/aps-cheatsheet.tex">View Source</a>
            </div>
            <div class="card">
                <h3>Error Codes Reference (LaTeX)</h3>
                <p>Multi-page reference with decision trees</p>
                <a href="pdfs/latex/error-codes-reference.tex">View Source</a>
            </div>
        </div>
        
        <h2>🚀 How to Generate PDFs</h2>
        <div class="card">
            <h3>From Infographics (Browser Method)</h3>
            <ol>
                <li>Click on any infographic link above</li>
                <li>Press <code>Ctrl+P</code> (or <code>Cmd+P</code> on Mac)</li>
                <li>Select "Save as PDF" as printer</li>
                <li>Ensure "Background graphics" is checked</li>
                <li>Save with A4 paper size</li>
            </ol>
        </div>
        
        <div class="card">
            <h3>From LaTeX Sources</h3>
            <p>Requires LaTeX installation (MiKTeX or TeX Live)</p>
            <pre><code>pdflatex aps-cheatsheet.tex
pdflatex error-codes-reference.tex</code></pre>
        </div>
    </div>
</body>
</html>"""
    
    index_path = Path('../docs/pdf-resources.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"✅ Created index page: docs/pdf-resources.html")

def main():
    print("🚀 RAPS PDF Generation and Organization")
    print("=" * 50)
    
    # Change to pdf-generation directory
    os.chdir(Path(__file__).parent)
    
    # Ensure directory structure
    ensure_docs_structure()
    
    # Generate PDFs with available methods
    generate_with_pandoc()
    
    # Copy resources to docs
    copy_web_layouts()
    copy_latex_sources()
    
    # Create index page
    create_index_page()
    
    print("\n✅ PDF resources organized in docs folder!")
    print("\n📋 Access via GitHub Pages:")
    print("  • Index: https://[your-github].github.io/raps-marketing/pdf-resources")
    print("  • PDFs: https://[your-github].github.io/raps-marketing/pdfs/")
    print("  • Infographics: https://[your-github].github.io/raps-marketing/infographics/")
    
    print("\n💡 To generate PDFs from infographics:")
    print("  1. Open the HTML files in your browser")
    print("  2. Print to PDF with background graphics enabled")
    print("  3. Save to docs/pdfs/infographics/")

if __name__ == "__main__":
    main()