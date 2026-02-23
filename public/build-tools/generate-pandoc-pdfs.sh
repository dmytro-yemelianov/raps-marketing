#!/bin/bash

# Professional PDF Generation using Pandoc + LaTeX
# Creates A4 PDFs in cheatsheets.zip style

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PDF_READY_DIR="$PROJECT_DIR/pdf-ready"
OUTPUT_DIR="$PROJECT_DIR/pdfs"
TEMP_DIR="$PROJECT_DIR/temp-pdf"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

mkdir -p "$OUTPUT_DIR" "$TEMP_DIR"

echo -e "${BLUE}🚀 RAPS Professional PDF Generator (Pandoc + LaTeX)${NC}"

# Create LaTeX template
cat > "$TEMP_DIR/professional.latex" << 'EOF'
\documentclass[10pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=0.7in]{geometry}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{listings}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{array}
\usepackage{parskip}
\usepackage{hyperref}

% Colors
\definecolor{primary}{RGB}{51, 122, 183}
\definecolor{secondary}{RGB}{250, 204, 21}
\definecolor{codeblue}{RGB}{0, 122, 204}

% Header/Footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textcolor{primary}{\textbf{$title$}}}
\fancyhead[R]{\textcolor{gray}{\small $subtitle$}}
\fancyfoot[L]{\textcolor{gray}{\small $version$}}
\fancyfoot[R]{\textcolor{gray}{\small Page \thepage}}

% Title formatting
\makeatletter
\renewcommand{\maketitle}{
  \begin{center}
    {\Huge\textcolor{primary}{\textbf{$title$}}}\\[0.2em]
    {\large\textcolor{gray}{$subtitle$}}\\[0.3em]
    {\small\textcolor{gray}{$version$}}
  \end{center}
  \vspace{1em}
}
\makeatother

% Code formatting
\lstset{
  basicstyle=\ttfamily\footnotesize,
  backgroundcolor=\color{gray!10},
  frame=single,
  breaklines=true,
  captionpos=b
}

% Hyperlink setup
\hypersetup{
  colorlinks=true,
  linkcolor=primary,
  urlcolor=codeblue,
  citecolor=primary
}

\begin{document}
\maketitle
$body$
\end{document}
EOF

# Function to generate PDF
generate_pdf_pandoc() {
    local input_file="$1"
    local output_name="$2"
    local title="$3"
    local subtitle="$4"
    local version="$5"
    
    echo -e "\n${YELLOW}📄 Processing: $(basename "$input_file")${NC}"
    
    # Use pandoc with LaTeX
    pandoc "$input_file" \
        --pdf-engine=pdflatex \
        --template="$TEMP_DIR/professional.latex" \
        --variable title="$title" \
        --variable subtitle="$subtitle" \
        --variable version="$version" \
        --highlight-style=tango \
        --variable geometry:margin=0.7in \
        --variable fontsize=10pt \
        --output "$OUTPUT_DIR/${output_name}.pdf" \
        2>/dev/null || {
            echo -e "${YELLOW}⚠️  LaTeX failed, trying simple pandoc...${NC}"
            # Fallback to simple pandoc
            pandoc "$input_file" \
                --variable title="$title" \
                --variable subtitle="$subtitle" \
                --variable version="$version" \
                --variable geometry:margin=0.7in \
                --variable fontsize=10pt \
                --highlight-style=tango \
                --output "$OUTPUT_DIR/${output_name}.pdf"
        }
    
    if [ -f "$OUTPUT_DIR/${output_name}.pdf" ]; then
        local size=$(ls -lh "$OUTPUT_DIR/${output_name}.pdf" | awk '{print $5}')
        echo -e "${GREEN}✅ Generated: ${output_name}.pdf (${size})${NC}"
    else
        echo -e "❌ Failed: ${output_name}.pdf"
        return 1
    fi
}

# Generate PDFs
echo -e "\n${YELLOW}📚 Generating PDFs...${NC}"

# APS Cheat Sheet
generate_pdf_pandoc \
    "$PDF_READY_DIR/aps-cheatsheet-pdf.md" \
    "aps-cheatsheet" \
    "APS Developer Cheat Sheet" \
    "Single-page reference for Autodesk Platform Services APIs" \
    "RAPS v4.11.0 | February 2026"

# Error Codes Reference
generate_pdf_pandoc \
    "$PDF_READY_DIR/error-codes-pdf.md" \
    "aps-error-codes" \
    "APS Error Codes Reference" \
    "Complete troubleshooting guide" \
    "RAPS v4.11.0 | February 2026"

# Migration Guide
generate_pdf_pandoc \
    "$PDF_READY_DIR/forge-migration-pdf.md" \
    "forge-to-aps-migration" \
    "Forge to APS Migration Guide" \
    "Complete step-by-step migration walkthrough" \
    "RAPS v4.11.0 | Migration deadline: Dec 31, 2026"

# Additional docs if they exist
docs_to_process=(
    "$PROJECT_DIR/cheatsheets/raps-developer-quickstart.md:raps-quickstart:RAPS Developer Quick Start:Get started with RAPS CLI in minutes"
    "$PROJECT_DIR/developer-resources/references/oauth-scopes.md:aps-oauth-scopes:APS OAuth Scopes Reference:Complete guide to OAuth scopes"
)

for doc_info in "${docs_to_process[@]}"; do
    IFS=':' read -r filepath filename title subtitle <<< "$doc_info"
    if [ -f "$filepath" ]; then
        generate_pdf_pandoc \
            "$filepath" \
            "$filename" \
            "$title" \
            "$subtitle" \
            "RAPS v4.11.0 | February 2026"
    fi
done

# Cleanup
rm -rf "$TEMP_DIR"

# Summary
echo -e "\n${GREEN}🎉 PDF generation completed!${NC}"
echo "Output directory: $OUTPUT_DIR"
echo ""
echo "Generated PDFs:"
ls -la "$OUTPUT_DIR"/*.pdf 2>/dev/null | awk '{print "  📄 " $9 " (" $5 ")"}'

echo ""
echo -e "${BLUE}📤 Upload these PDFs to GitHub releases for distribution${NC}"
EOF

chmod +x "$PROJECT_DIR/pdf-generation/generate-pandoc-pdfs.sh"