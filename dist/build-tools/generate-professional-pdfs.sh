#!/bin/bash

# Professional PDF Generation Script for RAPS Marketing Materials
# Creates A4 PDFs in the style of cheatsheets.zip with proper layout and formatting

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PDF_READY_DIR="$PROJECT_DIR/pdf-ready"
OUTPUT_DIR="$PROJECT_DIR/pdfs"
TEMP_DIR="$PROJECT_DIR/temp-pdf"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create directories
mkdir -p "$OUTPUT_DIR" "$TEMP_DIR"

echo -e "${BLUE}🚀 RAPS Professional PDF Generator${NC}"
echo "=================================================="

# Check dependencies
check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}❌ $1 is required but not installed${NC}"
        return 1
    fi
    echo -e "${GREEN}✅ $1 found${NC}"
}

echo -e "\n${YELLOW}📋 Checking dependencies...${NC}"
check_dependency "pandoc" || exit 1
check_dependency "pdflatex" || echo -e "${YELLOW}⚠️  pdflatex not found, using weasyprint fallback${NC}"

# LaTeX template for professional cheatsheets
create_latex_template() {
    cat > "$TEMP_DIR/cheatsheet-template.tex" << 'EOF'
\documentclass[8pt,a4paper,landscape,twocolumn]{extarticle}
\usepackage[utf8]{inputenc}
\usepackage[margin=0.5in]{geometry}
\usepackage{multicol}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{tcolorbox}
\usepackage{fontspec}
\usepackage{hyperref}

% Colors (matching cheatsheets.zip style)
\definecolor{primary}{RGB}{51, 122, 183}
\definecolor{secondary}{RGB}{250, 204, 21}
\definecolor{accent}{RGB}{92, 184, 92}
\definecolor{dark}{RGB}{52, 58, 64}
\definecolor{light}{RGB}{248, 249, 250}

% Fonts
\setmainfont{Inter}[
    UprightFont = *-Regular,
    BoldFont = *-Bold,
    ItalicFont = *-Italic,
    BoldItalicFont = *-BoldItalic
]
\setmonofont{JetBrains Mono}

% Header and Footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textcolor{primary}{\textbf{$title$}}}
\fancyhead[R]{\textcolor{dark}{\small $subtitle$}}
\fancyfoot[L]{\textcolor{dark}{\small $version$}}
\fancyfoot[R]{\textcolor{dark}{\small Page \thepage}}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0.5pt}

% Custom boxes for sections
\newtcolorbox{codebox}{
    colback=light,
    colframe=primary,
    rounded corners,
    boxrule=1pt,
    left=2pt,
    right=2pt,
    top=2pt,
    bottom=2pt
}

\newtcolorbox{tipbox}{
    colback=secondary!10,
    colframe=secondary,
    rounded corners,
    boxrule=1pt,
    left=2pt,
    right=2pt,
    top=2pt,
    bottom=2pt
}

% Compact spacing
\setlength{\parindent}{0pt}
\setlength{\parskip}{2pt}
\setlength{\columnsep}{15pt}

\begin{document}
$body$
\end{document}
EOF
}

# HTML template for web-style PDFs
create_html_template() {
    cat > "$TEMP_DIR/web-template.html" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>$title$</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        @page {
            size: A4;
            margin: 0.5in;
            @top-left { content: "$title$"; font-weight: bold; color: #337ab7; }
            @top-right { content: "$subtitle$"; font-size: 0.9em; color: #343a40; }
            @bottom-left { content: "$version$"; font-size: 0.8em; color: #6c757d; }
            @bottom-right { content: "Page " counter(page); font-size: 0.8em; color: #6c757d; }
        }
        
        body {
            font-family: 'Inter', sans-serif;
            font-size: 8pt;
            line-height: 1.3;
            color: #212529;
            margin: 0;
            padding: 0;
            column-count: 2;
            column-gap: 15pt;
            column-fill: balance;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #337ab7;
            font-weight: 600;
            margin: 8pt 0 4pt 0;
            break-after: avoid;
        }
        
        h1 { font-size: 14pt; column-span: all; text-align: center; border-bottom: 2px solid #337ab7; padding-bottom: 4pt; margin-bottom: 10pt; }
        h2 { font-size: 11pt; color: #facc15; background: #343a40; padding: 2pt 4pt; margin-top: 10pt; }
        h3 { font-size: 10pt; }
        h4 { font-size: 9pt; }
        
        p { margin: 3pt 0; }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 4pt 0;
            font-size: 7pt;
            break-inside: avoid;
        }
        
        th, td {
            border: 1px solid #dee2e6;
            padding: 2pt 4pt;
            text-align: left;
        }
        
        th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #495057;
        }
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        code {
            font-family: 'JetBrains Mono', monospace;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 2pt;
            padding: 1pt 2pt;
            font-size: 7pt;
        }
        
        pre {
            font-family: 'JetBrains Mono', monospace;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 3pt;
            padding: 4pt;
            margin: 4pt 0;
            font-size: 7pt;
            overflow-x: auto;
            break-inside: avoid;
        }
        
        .tip-box {
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            border-left: 4px solid #ffc107;
            border-radius: 3pt;
            padding: 4pt 6pt;
            margin: 4pt 0;
            break-inside: avoid;
        }
        
        .warning-box {
            background-color: #f8d7da;
            border: 1px solid #dc3545;
            border-left: 4px solid #dc3545;
            border-radius: 3pt;
            padding: 4pt 6pt;
            margin: 4pt 0;
            break-inside: avoid;
        }
        
        .code-box {
            background-color: #e7f3ff;
            border: 1px solid #337ab7;
            border-left: 4px solid #337ab7;
            border-radius: 3pt;
            padding: 4pt 6pt;
            margin: 4pt 0;
            break-inside: avoid;
        }
        
        ul, ol {
            margin: 3pt 0;
            padding-left: 12pt;
        }
        
        li {
            margin: 1pt 0;
        }
        
        blockquote {
            border-left: 3px solid #facc15;
            padding-left: 6pt;
            margin: 4pt 0 4pt 6pt;
            font-style: italic;
            color: #6c757d;
        }
        
        hr {
            border: none;
            border-top: 1px solid #dee2e6;
            margin: 6pt 0;
        }
        
        .break-before {
            break-before: column;
        }
        
        .no-break {
            break-inside: avoid;
        }
    </style>
</head>
<body>
$body$
</body>
</html>
EOF
}

# Function to generate PDF from markdown
generate_pdf() {
    local input_file="$1"
    local output_name="$2"
    local title="$3"
    local subtitle="$4"
    local version="$5"
    
    echo -e "\n${YELLOW}📄 Processing: ${input_file}${NC}"
    echo "   Title: $title"
    echo "   Output: ${output_name}.pdf"
    
    # Create temporary HTML file with enhanced styling
    local temp_html="$TEMP_DIR/${output_name}.html"
    
    # Convert markdown to HTML with custom template
    pandoc "$input_file" \
        --to html5 \
        --template "$TEMP_DIR/web-template.html" \
        --variable title="$title" \
        --variable subtitle="$subtitle" \
        --variable version="$version" \
        --highlight-style=tango \
        --output "$temp_html"
    
    # Generate PDF using weasyprint or wkhtmltopdf
    if command -v weasyprint &> /dev/null; then
        echo "   Using WeasyPrint for PDF generation..."
        weasyprint "$temp_html" "$OUTPUT_DIR/${output_name}.pdf" \
            --format pdf \
            --encoding utf-8 \
            --optimize-images
    elif command -v wkhtmltopdf &> /dev/null; then
        echo "   Using wkhtmltopdf for PDF generation..."
        wkhtmltopdf \
            --page-size A4 \
            --orientation Portrait \
            --margin-top 0.5in \
            --margin-right 0.5in \
            --margin-bottom 0.5in \
            --margin-left 0.5in \
            --enable-local-file-access \
            --print-media-type \
            "$temp_html" "$OUTPUT_DIR/${output_name}.pdf"
    else
        echo -e "${RED}❌ No PDF generator found. Please install weasyprint or wkhtmltopdf${NC}"
        return 1
    fi
    
    if [ -f "$OUTPUT_DIR/${output_name}.pdf" ]; then
        local file_size=$(ls -lh "$OUTPUT_DIR/${output_name}.pdf" | awk '{print $5}')
        echo -e "${GREEN}✅ Generated: ${output_name}.pdf (${file_size})${NC}"
    else
        echo -e "${RED}❌ Failed to generate: ${output_name}.pdf${NC}"
        return 1
    fi
}

# Create templates
echo -e "\n${YELLOW}🎨 Creating PDF templates...${NC}"
create_html_template

# Generate PDFs for each document
echo -e "\n${YELLOW}📚 Generating professional PDFs...${NC}"

# APS Cheat Sheet
if [ -f "$PDF_READY_DIR/aps-cheatsheet-pdf.md" ]; then
    generate_pdf \
        "$PDF_READY_DIR/aps-cheatsheet-pdf.md" \
        "aps-cheatsheet" \
        "APS Developer Cheat Sheet" \
        "Single-page reference for Autodesk Platform Services APIs with RAPS shortcuts" \
        "RAPS v4.11.0 | APS APIs: Auth v2, DM v1, MD v2, OSS v2, DA v3 | February 2026"
fi

# Error Codes Reference
if [ -f "$PDF_READY_DIR/error-codes-pdf.md" ]; then
    generate_pdf \
        "$PDF_READY_DIR/error-codes-pdf.md" \
        "aps-error-codes" \
        "APS API Error Codes Reference" \
        "Complete troubleshooting guide for Autodesk Platform Services" \
        "RAPS v4.11.0 | APS APIs: Auth v2, DM v1, MD v2, OSS v2, DA v3 | February 2026"
fi

# Forge Migration Guide
if [ -f "$PDF_READY_DIR/forge-migration-pdf.md" ]; then
    generate_pdf \
        "$PDF_READY_DIR/forge-migration-pdf.md" \
        "forge-to-aps-migration" \
        "Forge to APS Migration Guide" \
        "Complete step-by-step migration walkthrough" \
        "RAPS v4.11.0 | Migration deadline: December 31, 2026 | February 2026"
fi

# Generate additional PDFs from existing markdown files
echo -e "\n${YELLOW}📋 Processing additional documents...${NC}"

# RAPS Developer Quickstart
if [ -f "$PROJECT_DIR/cheatsheets/raps-developer-quickstart.md" ]; then
    generate_pdf \
        "$PROJECT_DIR/cheatsheets/raps-developer-quickstart.md" \
        "raps-developer-quickstart" \
        "RAPS Developer Quick Start Guide" \
        "Get started with RAPS CLI for APS automation in minutes" \
        "RAPS v4.11.0 | Minimum Rust 1.88.0 | February 2026"
fi

# OAuth Scopes Reference  
if [ -f "$PROJECT_DIR/developer-resources/references/oauth-scopes.md" ]; then
    generate_pdf \
        "$PROJECT_DIR/developer-resources/references/oauth-scopes.md" \
        "aps-oauth-scopes" \
        "APS OAuth Scopes Reference" \
        "Complete guide to Autodesk Platform Services OAuth scopes and permissions" \
        "RAPS v4.11.0 | APS Authentication API v2 | February 2026"
fi

# Upload-Translate-View Recipe
if [ -f "$PROJECT_DIR/developer-resources/recipes/upload-translate-view.md" ]; then
    generate_pdf \
        "$PROJECT_DIR/developer-resources/recipes/upload-translate-view.md" \
        "aps-upload-translate-view" \
        "Upload → Translate → View Workflow Recipe" \
        "Complete step-by-step recipe for the most common APS workflow" \
        "RAPS v4.11.0 | APS APIs: OSS v2, Model Derivative v2, Viewer v7 | February 2026"
fi

# Cleanup
echo -e "\n${YELLOW}🧹 Cleaning up temporary files...${NC}"
rm -rf "$TEMP_DIR"

# Summary
echo -e "\n${GREEN}🎉 PDF generation completed!${NC}"
echo "=================================================="
echo -e "📁 Output directory: ${BLUE}$OUTPUT_DIR${NC}"
echo ""
echo "Generated PDFs:"
for pdf in "$OUTPUT_DIR"/*.pdf; do
    if [ -f "$pdf" ]; then
        local filename=$(basename "$pdf")
        local size=$(ls -lh "$pdf" | awk '{print $5}')
        echo -e "  📄 ${GREEN}$filename${NC} ($size)"
    fi
done

echo ""
echo -e "${BLUE}💡 Pro Tips:${NC}"
echo "  • PDFs are optimized for A4 printing"
echo "  • Professional layout matches cheatsheets.zip style"
echo "  • All PDFs include RAPS branding and version info"
echo "  • Use these for conferences, workshops, and distribution"

echo ""
echo -e "${YELLOW}📤 Next Steps:${NC}"
echo "  • Upload PDFs to GitHub releases"
echo "  • Add to marketing materials"
echo "  • Include in press kits"
echo "  • Share on social media"

exit 0
EOF

chmod +x "$PROJECT_DIR/pdf-generation/generate-professional-pdfs.sh"