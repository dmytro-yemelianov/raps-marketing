# 📄 RAPS Marketing PDFs

**Professional A4 PDFs for distribution, workshops, and reference**

---

## 🎯 Available PDFs

### 📋 Developer Cheat Sheets
- **[aps-cheatsheet.pdf](./aps-cheatsheet.pdf)** - Single-page APS API reference with RAPS shortcuts
- **[raps-developer-quickstart.pdf](./raps-developer-quickstart.pdf)** - Get started with RAPS CLI in minutes

### 📚 Reference Guides  
- **[aps-error-codes-reference.pdf](./aps-error-codes-reference.pdf)** - Complete troubleshooting guide for APS APIs
- **[aps-oauth-scopes-reference.pdf](./aps-oauth-scopes-reference.pdf)** - OAuth scopes and permissions guide

### 🔄 Migration Resources
- **[forge-to-aps-migration-guide.pdf](./forge-to-aps-migration-guide.pdf)** - Step-by-step Forge to APS migration

---

## 📏 Specifications

### Format Details
- **Page Size:** A4 (210 × 297 mm)
- **Orientation:** Portrait
- **Margins:** 0.75 inches
- **Font:** Professional sans-serif
- **Size:** ~300KB each (optimized for download)

### Design Features
- ✅ Professional layout inspired by cheatsheets.zip
- ✅ RAPS branding and version information
- ✅ Print-optimized formatting
- ✅ Clean typography without emoji dependencies
- ✅ Table of contents and section numbering
- ✅ Consistent header/footer design

---

## 🎨 Design Philosophy

### Visual Hierarchy
1. **Clear Section Headers** - Easy navigation
2. **Consistent Tables** - Structured information display
3. **Code Highlighting** - Syntax-highlighted examples
4. **Professional Typography** - Readable fonts and spacing
5. **RAPS Branding** - Consistent color scheme and logos

### Content Strategy
- **Value-First Approach** - Useful standalone content
- **RAPS Integration** - Natural CLI introduction
- **Version Tracking** - Current RAPS and APS versions
- **Print-Friendly** - Optimized for physical distribution

---

## 📤 Usage Rights

### Distribution
- ✅ **Conferences** - Free distribution at developer events
- ✅ **Workshops** - Training and educational materials
- ✅ **Social Media** - Sharing and promotion
- ✅ **Corporate** - Internal training and reference

### Attribution
When sharing these PDFs:
- Credit: "RAPS Marketing Team"
- Link: rapscli.xyz
- Version: Include current version info

---

## 🔄 Regeneration

### Automated Updates
PDFs are automatically generated from source markdown files:

```bash
# Regenerate all PDFs
cd pdf-generation/
python create-clean-pdfs.py
```

### Source Files
- `pdf-ready/aps-cheatsheet-pdf.md` → `aps-cheatsheet.pdf`
- `pdf-ready/error-codes-pdf.md` → `aps-error-codes-reference.pdf`
- `pdf-ready/forge-migration-pdf.md` → `forge-to-aps-migration-guide.pdf`
- `cheatsheets/raps-developer-quickstart.md` → `raps-developer-quickstart.pdf`
- `developer-resources/references/oauth-scopes.md` → `aps-oauth-scopes-reference.pdf`

### Version Updates
When updating PDFs:
1. Update source markdown files
2. Update version numbers in frontmatter
3. Run regeneration script
4. Commit updated PDFs

---

## 📊 Analytics & Feedback

### Distribution Tracking
- **Download counts** via GitHub release metrics
- **Social sharing** via link tracking
- **Conference distribution** via feedback forms
- **Workshop usage** via trainer reports

### Quality Metrics
- **Print quality** - A4 formatting verification
- **Content accuracy** - Technical review process
- **User feedback** - Community input integration
- **Version freshness** - Quarterly update cycle

---

## 🛠️ Technical Details

### Generation Process
1. **Source Processing** - Markdown cleaning and emoji removal
2. **Pandoc Conversion** - LaTeX-based PDF generation
3. **Style Application** - Professional formatting templates
4. **Quality Control** - Automated validation checks

### Dependencies
- **Pandoc** 2.0+ with LaTeX support
- **Python** 3.6+ for processing scripts
- **pdflatex** for final PDF generation
- **Git** for version control integration

### File Structure
```
pdfs/
├── README.md                              # This file
├── aps-cheatsheet.pdf                     # APS API cheat sheet
├── aps-error-codes-reference.pdf          # Error troubleshooting
├── aps-oauth-scopes-reference.pdf         # OAuth scopes guide
├── forge-to-aps-migration-guide.pdf       # Migration walkthrough
└── raps-developer-quickstart.pdf          # RAPS CLI quick start
```

---

## 🎯 Strategic Impact

### Marketing Goals
- **Developer Acquisition** - High-value reference materials
- **Brand Recognition** - Consistent RAPS presence
- **Community Building** - Shareable expert resources
- **SEO Enhancement** - PDF content in search results

### Success Metrics
- **Downloads** from GitHub releases
- **Shares** on social platforms
- **Conference feedback** from attendees
- **Community mentions** in forums/Discord

---

## 📞 Support

### Issues & Improvements
- **GitHub Issues** - Report PDF generation problems
- **Discord Community** - Get help with PDF usage
- **Marketing Team** - Contact for distribution partnerships

### Contributing
- **Content Updates** - Submit PRs for accuracy improvements
- **Design Feedback** - Suggest layout enhancements
- **Translation** - Help localize materials

---

*Last updated: January 2026 | RAPS v4.2.1*  
*Next review: April 2026 | Marketing Team*