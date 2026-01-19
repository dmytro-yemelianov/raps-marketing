# PDF Generation Instructions

## Converting Marketing Materials to A4 PDFs

### Prerequisites
- Node.js with puppeteer for HTML to PDF conversion
- Pandoc for Markdown to PDF conversion
- WeasyPrint for CSS-styled PDFs

### Setup
```bash
# Install required tools
npm install -g puppeteer-pdf

# Or use pandoc
sudo apt-get install pandoc texlive-xetex

# Or use weasyprint
pip install weasyprint
```

## Conversion Methods

### Method 1: Using Pandoc (Recommended)
```bash
# Install pandoc with LaTeX support
pandoc --version

# Convert with A4 format and professional styling
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  --variable=papersize:a4 \
  --variable=margin-top:2cm \
  --variable=margin-bottom:2cm \
  --variable=margin-left:2.5cm \
  --variable=margin-right:2.5cm \
  --variable=fontsize:11pt \
  --variable=mainfont:"Inter" \
  --variable=monofont:"JetBrains Mono" \
  --highlight-style=github \
  --toc \
  --toc-depth=3
```

### Method 2: Using HTML + CSS + Puppeteer
```javascript
// convert-pdf.js
const puppeteer = require('puppeteer');

async function convertToPDF(htmlContent, outputPath) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.setContent(htmlContent);
  
  await page.pdf({
    path: outputPath,
    format: 'A4',
    margin: {
      top: '2cm',
      right: '2cm', 
      bottom: '2cm',
      left: '2cm'
    },
    printBackground: true,
    preferCSSPageSize: true
  });
  
  await browser.close();
}
```

### Method 3: Using WeasyPrint
```bash
# Convert HTML to PDF with CSS styling
weasyprint input.html output.pdf \
  --format pdf \
  --presentational-hints \
  --optimize-size
```

## Professional PDF Styling

### CSS for Print Media
```css
@page {
  size: A4;
  margin: 2cm;
  
  @top-left {
    content: "RAPS Marketing Materials";
    font-size: 9pt;
    color: #666;
  }
  
  @top-right {
    content: "rapscli.xyz";
    font-size: 9pt;
    color: #666;
  }
  
  @bottom-center {
    content: "Page " counter(page) " of " counter(pages);
    font-size: 9pt;
    color: #666;
  }
}

@media print {
  body {
    font-family: 'Inter', sans-serif;
    font-size: 11pt;
    line-height: 1.4;
    color: #333;
  }
  
  h1 {
    color: #facc15;
    border-bottom: 2px solid #facc15;
    padding-bottom: 0.5em;
    page-break-after: avoid;
  }
  
  h2 {
    color: #1f2937;
    margin-top: 1.5em;
    page-break-after: avoid;
  }
  
  table {
    border-collapse: collapse;
    width: 100%;
    font-size: 10pt;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  th {
    background-color: #f8f9fa;
    font-weight: 600;
  }
  
  code {
    background-color: #f1f5f9;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9pt;
  }
  
  pre {
    background-color: #1e293b;
    color: #e2e8f0;
    padding: 1em;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 9pt;
  }
  
  .page-break {
    page-break-before: always;
  }
  
  .no-break {
    page-break-inside: avoid;
  }
}
```

## Automated Conversion Script

### Batch PDF Generation
```bash
#!/bin/bash
# convert-all.sh

# Directories
INPUT_DIR="."
OUTPUT_DIR="./pdf"
CSS_FILE="./pdf-generation/print-styles.css"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Convert all markdown files to PDF
for md_file in *.md; do
  if [[ -f "$md_file" ]]; then
    filename=$(basename "$md_file" .md)
    echo "Converting $md_file to PDF..."
    
    # Convert to HTML first with custom CSS
    pandoc "$md_file" \
      -f markdown \
      -t html5 \
      --css="$CSS_FILE" \
      --self-contained \
      --toc \
      --toc-depth=3 \
      --highlight-style=github \
      -o "$OUTPUT_DIR/${filename}.html"
    
    # Convert HTML to PDF
    puppeteer-pdf "$OUTPUT_DIR/${filename}.html" \
      --format=A4 \
      --margin-top=20mm \
      --margin-bottom=20mm \
      --margin-left=25mm \
      --margin-right=25mm \
      --print-background \
      > "$OUTPUT_DIR/${filename}.pdf"
    
    # Clean up HTML file
    rm "$OUTPUT_DIR/${filename}.html"
    
    echo "✅ Created: $OUTPUT_DIR/${filename}.pdf"
  fi
done

echo "🎉 All conversions complete!"
```

## Professional Templates

### Press Release Template
```css
/* Press release specific styles */
.press-release {
  font-family: 'Times New Roman', serif;
}

.press-release h1 {
  font-size: 18pt;
  text-align: center;
  margin-bottom: 1em;
}

.press-release .dateline {
  font-weight: bold;
  margin-bottom: 1em;
}

.press-release .contact-info {
  border-top: 1px solid #ddd;
  margin-top: 2em;
  padding-top: 1em;
  font-size: 10pt;
}

.press-release .boilerplate {
  font-style: italic;
  margin-top: 1.5em;
  padding: 1em;
  background-color: #f8f9fa;
  border-left: 4px solid #facc15;
}
```

### Cheat Sheet Template
```css
/* Cheat sheet specific styles */
.cheat-sheet {
  font-family: 'Inter', sans-serif;
  font-size: 10pt;
}

.cheat-sheet h1 {
  background: linear-gradient(135deg, #facc15, #f59e0b);
  color: white;
  padding: 1em;
  margin: -2cm -2cm 1em -2cm;
  font-size: 20pt;
}

.cheat-sheet h2 {
  background-color: #1f2937;
  color: white;
  padding: 0.5em;
  margin: 1em -0.5em 0.5em -0.5em;
}

.cheat-sheet table {
  font-size: 9pt;
  margin-bottom: 1em;
}

.cheat-sheet .command-box {
  background-color: #1e293b;
  color: #e2e8f0;
  padding: 0.5em;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 8pt;
  margin: 0.5em 0;
}

.cheat-sheet .tip-box {
  background-color: #fef3c7;
  border-left: 4px solid #f59e0b;
  padding: 0.5em;
  margin: 0.5em 0;
  font-size: 9pt;
}
```

## Quality Control

### PDF Validation Checklist
- [ ] A4 page size (210 × 297 mm)
- [ ] Consistent margins (2cm minimum)
- [ ] Professional fonts (Inter, Times New Roman)
- [ ] Readable font size (10-12pt body, appropriate headings)
- [ ] Proper page breaks (no orphaned headers)
- [ ] Table formatting (borders, alignment)
- [ ] Code blocks (dark background, monospace font)
- [ ] Brand colors (RAPS yellow #facc15)
- [ ] Header/footer with branding
- [ ] Table of contents (for documents >3 pages)
- [ ] Contact information included
- [ ] No broken links or references
- [ ] Consistent formatting throughout
- [ ] Professional appearance suitable for printing

### File Naming Convention
```
Format: [document-type]-[version]-[date].pdf

Examples:
- press-release-raps-4-0-launch-v1-2026-03-15.pdf
- cheatsheet-developer-quickstart-v4-2026-01-15.pdf
- cheatsheet-enterprise-admin-v4-2026-01-15.pdf
- cheatsheet-automation-patterns-v4-2026-01-15.pdf
```

## Distribution Preparation

### File Organization
```
pdf/
├── press-releases/
│   ├── raps-4-0-launch.pdf
│   └── mcp-server-announcement.pdf
├── cheatsheets/
│   ├── developer-quickstart.pdf
│   ├── enterprise-admin.pdf
│   └── automation-patterns.pdf
└── combined/
    └── raps-marketing-materials-complete.pdf
```

### Final Steps
1. Generate all PDFs using the conversion script
2. Review each PDF for quality and formatting
3. Test print one copy of each document  
4. Upload to marketing materials repository
5. Update GitHub Pages with download links
6. Distribute to marketing team and partners

---

**Tools Required**:
- Pandoc with XeLaTeX
- Node.js with Puppeteer
- Professional fonts (Inter, JetBrains Mono)
- CSS print stylesheets

**Quality Standards**: All PDFs must meet enterprise presentation standards suitable for customer distribution and press kit inclusion.