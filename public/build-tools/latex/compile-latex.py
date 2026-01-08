#!/usr/bin/env python3
"""
Compile LaTeX files to professional PDFs
"""

import subprocess
import sys
from pathlib import Path

def compile_latex(tex_file, output_dir):
    """Compile LaTeX file to PDF using pdflatex or xelatex"""
    
    print(f"📄 Compiling: {tex_file.name}")
    
    # Try xelatex first (better font support)
    compilers = ['xelatex', 'pdflatex']
    
    for compiler in compilers:
        try:
            cmd = [
                compiler,
                '-interaction=nonstopmode',
                '-output-directory', str(output_dir),
                str(tex_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                pdf_name = tex_file.stem + '.pdf'
                pdf_path = output_dir / pdf_name
                
                if pdf_path.exists():
                    size = pdf_path.stat().st_size / (1024 * 1024)
                    print(f"✅ Generated: {pdf_name} ({size:.1f}MB) using {compiler}")
                    
                    # Copy to docs/pdfs
                    docs_pdf_dir = Path(__file__).parent.parent.parent / 'docs' / 'pdfs'
                    docs_pdf_dir.mkdir(exist_ok=True)
                    
                    with open(pdf_path, 'rb') as src, open(docs_pdf_dir / pdf_name, 'wb') as dst:
                        dst.write(src.read())
                    
                    return True
                    
        except FileNotFoundError:
            print(f"⚠️  {compiler} not found")
            continue
        except subprocess.TimeoutExpired:
            print(f"⏰ {compiler} timed out")
            continue
        except Exception as e:
            print(f"❌ Error with {compiler}: {e}")
            continue
    
    return False

# Main
script_dir = Path(__file__).parent
output_dir = script_dir.parent.parent / 'pdfs'
output_dir.mkdir(exist_ok=True)

print("🚀 LaTeX PDF Compilation")
print("=" * 40)

# LaTeX files to compile
tex_files = [
    'aps-cheatsheet.tex',
    'error-codes-reference.tex'
]

success_count = 0

for tex_name in tex_files:
    tex_file = script_dir / tex_name
    if tex_file.exists():
        if compile_latex(tex_file, output_dir):
            success_count += 1
    else:
        print(f"⚠️  File not found: {tex_file}")

print(f"\n✅ Successfully compiled: {success_count} PDFs")
print("\n📋 Note: Install MiKTeX or TeX Live for LaTeX compilation")