# RAPS Research

Data-driven analysis of developer pain points in the AEC/CAD industry.

## ACC Forum Analysis

We analyzed **4,295 feature requests** from Autodesk Construction Cloud's official Ideas forum to understand what users actually need versus what gets delivered.

### Key Findings

| Metric | Value |
|--------|-------|
| Implementation Rate | **1.4%** |
| Ideas in "Gathering Support" | **96.6%** |
| Oldest Unaddressed Request | **4+ years** (Markups) |
| Total Community Votes | 24,615 |

### Files

```
acc-forum-analysis/
├── analysis.py          # Python analysis script
├── data/
│   └── acc_ideas.csv    # Raw data (4,295 ideas)
├── results/
│   └── analysis_results.json
└── README.md
```

### Running the Analysis

```bash
# Install dependencies
pip install pandas

# Run analysis
python analysis.py --input data/acc_ideas.csv --output results/

# Output: results/analysis_results.json
```

### Methodology

**Data Collection:** Scraped the ACC Ideas forum (`forums.autodesk.com/t5/acc-ideas/`) in January 2026 using Python (requests + BeautifulSoup). Collected all publicly visible ideas with metadata.

**Classification:** Topic categorization uses keyword matching against 18 predefined category groups. Pain pattern detection uses similar approach for 9 pattern types.

**Limitations:**
- Public forum data only (no internal Autodesk metrics)
- Keyword classification may misclassify edge cases
- "Gathering Support" may include ideas tracked internally

### Interactive Report

View the full analysis with interactive charts: [rapscli.xyz/research/acc-analysis](https://rapscli.xyz/research/acc-analysis)

### Blog Post

Read the detailed breakdown: [4,295 Feature Requests, 60 Delivered](https://rapscli.xyz/blog/acc-forum-analysis)

---

## Cross-Platform CAD/PLM Research

We've also conducted research comparing developer pain points across:
- Autodesk APS/Forge
- PTC Onshape
- Dassault 3DEXPERIENCE/SOLIDWORKS
- Siemens Teamcenter/NX Open

Key finding: **Developer pain points are universal across platforms.** Authentication complexity, file translation failures, SDK version conflicts, and documentation gaps affect developers regardless of vendor.

See: [Developer Pain Points Are Universal](docs/cross-platform-pain-points.md)

---

## Contributing

Found errors in our analysis? Have additional data to contribute?

1. Open an issue describing the problem or contribution
2. For data corrections, include source links
3. For new analysis, submit a PR with methodology documentation

---

## License

Data and analysis code: MIT License

This research is conducted independently and is not affiliated with or endorsed by Autodesk, PTC, Dassault Systèmes, or Siemens.

---

## About

This research is part of the [RAPS CLI](https://rapscli.xyz) project — developer tools for Autodesk Platform Services.

**Author:** Dmytro Yemelianov  
**Contact:** [LinkedIn](https://linkedin.com/in/dmytro-yemelianov) | [GitHub](https://github.com/dmytro-yemelianov)
