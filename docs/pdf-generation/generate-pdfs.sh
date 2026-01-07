#!/bin/bash

# RAPS Marketing Materials PDF Generation Script
# Converts all markdown materials to professional A4 PDFs

set -e  # Exit on error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_ROOT/pdf-output"
CSS_FILE="$SCRIPT_DIR/print-styles.css"
TEMP_DIR="/tmp/raps-pdf-generation"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    local missing_deps=()
    
    if ! command -v pandoc &> /dev/null; then
        missing_deps+=("pandoc")
    fi
    
    if ! command -v xelatex &> /dev/null; then
        missing_deps+=("xelatex (texlive-xetex)")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        echo ""
        echo "Install missing dependencies:"
        echo "  Ubuntu/Debian: sudo apt-get install pandoc texlive-xetex"
        echo "  macOS: brew install pandoc basictex"
        echo "  Windows: Download from https://pandoc.org/installing.html"
        exit 1
    fi
    
    log_success "All dependencies found"
}

# Setup directories
setup_directories() {
    log_info "Setting up directories..."
    
    rm -rf "$OUTPUT_DIR" "$TEMP_DIR"
    mkdir -p "$OUTPUT_DIR/press-releases"
    mkdir -p "$OUTPUT_DIR/cheatsheets" 
    mkdir -p "$OUTPUT_DIR/combined"
    mkdir -p "$TEMP_DIR"
    
    log_success "Directories created"
}

# Generate PDF with pandoc
generate_pdf() {
    local input_file="$1"
    local output_file="$2"
    local title="$3"
    local doc_type="$4"
    
    log_info "Converting $(basename "$input_file") to PDF..."
    
    # Create temporary HTML with styling
    local temp_html="$TEMP_DIR/$(basename "$input_file" .md).html"
    
    # Add document class to markdown
    local temp_md="$TEMP_DIR/$(basename "$input_file")"
    echo "<div class=\"$doc_type\">" > "$temp_md"
    cat "$input_file" >> "$temp_md"
    echo "</div>" >> "$temp_md"
    
    # Convert to HTML first
    pandoc "$temp_md" \
        -f markdown \
        -t html5 \
        --css="$CSS_FILE" \
        --self-contained \
        --toc \
        --toc-depth=3 \
        --highlight-style=github \
        --template=html5 \
        --metadata title="$title" \
        --metadata date="$(date '+%B %d, %Y')" \
        --metadata author="RAPS Marketing Team" \
        -o "$temp_html"
    
    # Convert HTML to PDF using pandoc with xelatex
    pandoc "$temp_html" \
        -f html \
        -t pdf \
        --pdf-engine=xelatex \
        --variable=papersize:a4 \
        --variable=margin-top:20mm \
        --variable=margin-bottom:20mm \
        --variable=margin-left:25mm \
        --variable=margin-right:25mm \
        --variable=fontsize:11pt \
        --variable=mainfont:"Inter" \
        --variable=monofont:"JetBrains Mono" \
        --variable=geometry:a4paper \
        --variable=colorlinks:true \
        --variable=linkcolor:blue \
        --variable=urlcolor:blue \
        --variable=toccolor:black \
        -o "$output_file"
    
    if [ -f "$output_file" ]; then
        local file_size=$(du -h "$output_file" | cut -f1)
        log_success "Created: $(basename "$output_file") ($file_size)"
    else
        log_error "Failed to create: $(basename "$output_file")"
        return 1
    fi
}

# Generate all press releases
generate_press_releases() {
    log_info "Generating press release PDFs..."
    
    local press_dir="$PROJECT_ROOT/press/press-releases"
    
    if [ -d "$press_dir" ]; then
        for md_file in "$press_dir"/*.md; do
            if [ -f "$md_file" ]; then
                local filename=$(basename "$md_file" .md)
                local title=$(head -n 1 "$md_file" | sed 's/^# //')
                generate_pdf "$md_file" "$OUTPUT_DIR/press-releases/${filename}.pdf" "$title" "press-release"
            fi
        done
    else
        log_warning "Press releases directory not found: $press_dir"
    fi
}

# Generate all cheat sheets
generate_cheatsheets() {
    log_info "Generating cheat sheet PDFs..."
    
    local cheat_dir="$PROJECT_ROOT/cheatsheets"
    
    if [ -d "$cheat_dir" ]; then
        for md_file in "$cheat_dir"/*.md; do
            if [ -f "$md_file" ]; then
                local filename=$(basename "$md_file" .md)
                local title=$(head -n 1 "$md_file" | sed 's/^# //')
                generate_pdf "$md_file" "$OUTPUT_DIR/cheatsheets/${filename}.pdf" "$title" "cheat-sheet"
            fi
        done
    else
        log_warning "Cheat sheets directory not found: $cheat_dir"
    fi
}

# Create combined PDF with all materials
create_combined_pdf() {
    log_info "Creating combined PDF with all materials..."
    
    local combined_md="$TEMP_DIR/all-materials.md"
    local combined_pdf="$OUTPUT_DIR/combined/raps-marketing-materials-complete.pdf"
    
    # Create title page
    cat > "$combined_md" << 'EOF'
---
title: "RAPS Marketing Materials"
subtitle: "Complete Press Kit and Documentation"
author: "RAPS Marketing Team"
date: "2026"
geometry: "a4paper,margin=25mm"
fontsize: 11pt
mainfont: "Inter"
monofont: "JetBrains Mono"
colorlinks: true
linkcolor: blue
urlcolor: blue
toccolor: black
toc: true
toc-depth: 3
---

<div class="combined-materials">

# RAPS Marketing Materials

*Complete Press Kit and Documentation Package*

---

## Table of Contents

This document contains the complete set of RAPS marketing materials including press releases, developer guides, and enterprise documentation.

### Included Materials:
- Press Releases
- Developer Quick Start Guide  
- Enterprise Admin Guide
- APS Automation Patterns

---

EOF
    
    # Add press releases section
    echo "# Press Releases" >> "$combined_md"
    echo "" >> "$combined_md"
    
    for md_file in "$PROJECT_ROOT/press/press-releases"/*.md; do
        if [ -f "$md_file" ]; then
            echo "## $(basename "$md_file" .md | tr '-' ' ' | sed 's/\b\w/\u&/g')" >> "$combined_md"
            echo "" >> "$combined_md"
            cat "$md_file" | sed 's/^# /### /' >> "$combined_md"
            echo "" >> "$combined_md"
            echo "\\pagebreak" >> "$combined_md"
            echo "" >> "$combined_md"
        fi
    done
    
    # Add cheat sheets section
    echo "# Documentation and Guides" >> "$combined_md"
    echo "" >> "$combined_md"
    
    for md_file in "$PROJECT_ROOT/cheatsheets"/*.md; do
        if [ -f "$md_file" ]; then
            echo "## $(basename "$md_file" .md | tr '-' ' ' | sed 's/\b\w/\u&/g')" >> "$combined_md"
            echo "" >> "$combined_md"
            cat "$md_file" | sed 's/^# /### /' >> "$combined_md"
            echo "" >> "$combined_md"
            echo "\\pagebreak" >> "$combined_md"
            echo "" >> "$combined_md"
        fi
    done
    
    echo "</div>" >> "$combined_md"
    
    # Generate the combined PDF
    generate_pdf "$combined_md" "$combined_pdf" "RAPS Marketing Materials" "combined-materials"
}

# Generate file manifest
generate_manifest() {
    log_info "Generating file manifest..."
    
    local manifest_file="$OUTPUT_DIR/MANIFEST.md"
    
    cat > "$manifest_file" << EOF
# RAPS Marketing Materials - File Manifest

Generated: $(date '+%Y-%m-%d %H:%M:%S')

## Press Releases
EOF
    
    if ls "$OUTPUT_DIR/press-releases"/*.pdf 1> /dev/null 2>&1; then
        for pdf_file in "$OUTPUT_DIR/press-releases"/*.pdf; do
            local filename=$(basename "$pdf_file")
            local filesize=$(du -h "$pdf_file" | cut -f1)
            echo "- **$filename** ($filesize)" >> "$manifest_file"
        done
    else
        echo "- No press releases generated" >> "$manifest_file"
    fi
    
    cat >> "$manifest_file" << EOF

## Cheat Sheets
EOF
    
    if ls "$OUTPUT_DIR/cheatsheets"/*.pdf 1> /dev/null 2>&1; then
        for pdf_file in "$OUTPUT_DIR/cheatsheets"/*.pdf; do
            local filename=$(basename "$pdf_file")
            local filesize=$(du -h "$pdf_file" | cut -f1)
            echo "- **$filename** ($filesize)" >> "$manifest_file"
        done
    else
        echo "- No cheat sheets generated" >> "$manifest_file"
    fi
    
    cat >> "$manifest_file" << EOF

## Combined Materials
EOF
    
    if ls "$OUTPUT_DIR/combined"/*.pdf 1> /dev/null 2>&1; then
        for pdf_file in "$OUTPUT_DIR/combined"/*.pdf; do
            local filename=$(basename "$pdf_file")
            local filesize=$(du -h "$pdf_file" | cut -f1)
            echo "- **$filename** ($filesize)" >> "$manifest_file"
        done
    else
        echo "- No combined materials generated" >> "$manifest_file"
    fi
    
    cat >> "$manifest_file" << EOF

## Usage Instructions

### Printing
All PDFs are formatted for A4 paper with 20-25mm margins. Recommended print settings:
- Paper: A4 (210 × 297 mm)
- Quality: High/Best
- Color: Color (for brand elements)
- Scaling: None (100%)

### Distribution
These materials are approved for:
- Customer presentations
- Partner distribution  
- Press kit inclusion
- Trade show handouts
- Internal training

### Contact
For questions about these materials:
- Email: marketing@rapscli.xyz
- Website: https://rapscli.xyz
EOF
    
    log_success "Manifest created: $(basename "$manifest_file")"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
}

# Main execution
main() {
    echo "🎯 RAPS Marketing Materials PDF Generator"
    echo "========================================"
    echo ""
    
    check_dependencies
    setup_directories
    
    generate_press_releases
    generate_cheatsheets
    create_combined_pdf
    generate_manifest
    
    cleanup
    
    echo ""
    log_success "PDF generation complete!"
    echo ""
    echo "📁 Output directory: $OUTPUT_DIR"
    echo "📊 Files generated:"
    find "$OUTPUT_DIR" -name "*.pdf" | while read -r pdf_file; do
        local filesize=$(du -h "$pdf_file" | cut -f1)
        echo "   $(basename "$pdf_file") ($filesize)"
    done
    echo ""
    echo "📋 See MANIFEST.md for complete file listing and usage instructions"
    echo ""
}

# Trap to ensure cleanup on exit
trap cleanup EXIT

# Run main function
main "$@"