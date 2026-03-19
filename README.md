# RAPS Marketing

Marketing site, research reports, DevCon materials, and pitch collateral for [Rapsody](https://rapscli.xyz) — the commercial APS platform.

## Directory Structure

```
raps-marketing/
├── src/                        # Astro site source
│   ├── components/             # React/Astro components (PainPointMatrix, etc.)
│   ├── content/                # Content collections (articles, guides, cheatsheets,
│   │                             campaigns, analytics, press, recipes, references)
│   ├── layouts/                # Astro page layouts
│   ├── pages/                  # Routes: articles, guides, tools, pdfs, devcon, recipes
│   └── styles/                 # Global CSS
├── public/                     # Static assets (PDFs, images, favicon)
├── devcon/                     # DevCon CFP drafts and images
│   ├── 1257-ai-pair-assistant.md
│   ├── 1258-zero-to-production.md
│   ├── 1259-acc-enterprise-scale.md
│   └── cfp2026.md / cfp_good.md
├── pitch/                      # Investor/partner pitch materials
├── forums-scraper/             # Autodesk & ACC forum scrapers and analysis
│   ├── acc_ideas_scraper_v2.py # ACC Ideas Forum scraper (4,295 ideas)
│   ├── autodesk_forum_api.py   # Forum API client
│   └── *.md / *.html           # Analysis reports and guides
├── reports/                    # Market research outputs
│   ├── forums_analysis_2026-02.md
│   ├── marketplace_analysis_2026-02.md
│   ├── stackoverflow_analysis_2026-02.md
│   └── *.json / *.html         # Data files and rendered reports
├── upwork/                     # Freelancer collateral and proposals
│   ├── collateral/             # Capability deck, FAQ, social proof
│   ├── portfolio/
│   └── proposals/
├── scripts/                    # Build helpers (clean-astro-cache.mjs)
├── astro.config.mjs            # Astro configuration
├── tailwind.config.mjs         # Tailwind CSS with RAPS brand colors
└── package.json                # Node dependencies
```

## Development

Requires Node.js 18+.

```bash
npm install
npm run dev       # Start dev server at http://localhost:4321
npm run build     # Build to ./dist/
npm run preview   # Preview production build
```

## Content Editing

- **Articles/Guides**: Add `.md` or `.mdx` files to `src/content/articles/` or `src/content/guides/` with frontmatter (title, description, publishDate, tags).
- **Interactive tools**: React components in `src/components/`, pages in `src/pages/tools/`.
- **DevCon CFPs**: Markdown files in `devcon/`.
- **Research**: Run scrapers in `forums-scraper/`, output lands in `reports/`.

## Key Data Points (Feb 2026 Research)

| Source | Records | Insight |
|--------|---------|---------|
| ACC Ideas Forum | 4,295 ideas | 1.4% implementation rate |
| StackOverflow | 4,582 questions | 13% unanswered |
| Autodesk Marketplace | 259 ACC apps | Zero CLI or MCP tools |

## Deployment

```bash
npm run build     # Output in dist/
vercel --prod     # Or deploy dist/ to Netlify/GitHub Pages
```
