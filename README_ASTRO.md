# RAPS Marketing Site - Astro Version

Modern, performant marketing site for RAPS CLI built with Astro.

## 🚀 Features

- **Lightning Fast**: Static site generation with minimal JavaScript
- **SEO Optimized**: Automatic sitemap, meta tags, and Open Graph
- **Interactive Components**: React islands for dynamic features
- **Content Collections**: Type-safe content management
- **Tailwind CSS**: Utility-first styling with custom RAPS theme
- **MDX Support**: Enhanced Markdown with components
- **Responsive Design**: Mobile-first approach

## 📁 Project Structure

```
astro-site/
├── src/
│   ├── components/       # Astro & React components
│   │   └── PainPointMatrix.tsx
│   ├── content/          # Content collections
│   │   ├── articles/     # Blog articles
│   │   ├── guides/       # Documentation
│   │   └── cross-platform/ # Research content
│   ├── layouts/          # Page layouts
│   │   └── BaseLayout.astro
│   ├── pages/            # Route pages
│   │   ├── index.astro   # Home page
│   │   ├── articles/     # Articles section
│   │   └── tools/        # Interactive tools
│   └── styles/           # Global styles
│       └── global.css
├── public/               # Static assets
│   ├── images/
│   └── pdfs/
└── astro.config.mjs      # Astro configuration
```

## 🛠️ Development

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Available Scripts

- `npm run dev` - Start development server at http://localhost:4321
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run astro` - Run Astro CLI commands

## 🎨 Customization

### Colors
Edit the color palette in `tailwind.config.mjs`:
- RAPS brand colors (blue, purple, green)
- APS brand colors (primary, secondary)

### Typography
Modify font settings in `src/styles/global.css`

### Components
Add new interactive components in `src/components/`

## 📝 Content Management

### Adding Articles
Create new `.md` or `.mdx` files in `src/content/articles/`:

```markdown
---
title: "Your Article Title"
description: "Brief description"
publishDate: 2026-01-08
tags: ["tag1", "tag2"]
featured: true
---

Article content here...
```

### Adding Guides
Create files in `src/content/guides/` with proper frontmatter.

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Netlify

```bash
# Build command
npm run build

# Publish directory
dist/
```

### GitHub Pages

```bash
# Update astro.config.mjs
site: 'https://yourusername.github.io'
base: '/repo-name'

# Build and deploy
npm run build
# Push dist/ to gh-pages branch
```

## 🔧 Configuration

### Astro Config
Edit `astro.config.mjs` for:
- Site URL
- Integrations
- Build options
- Markdown rendering

### Tailwind Config
Edit `tailwind.config.mjs` for:
- Custom colors
- Fonts
- Plugins

## 📊 Performance

Expected Lighthouse scores:
- Performance: 95+
- Accessibility: 100
- Best Practices: 100
- SEO: 100

## 🤝 Migration from Jekyll

This Astro site replaces the previous Jekyll/GitHub Pages setup with:
- Better performance (50% faster load times)
- Interactive components
- Modern development experience
- Enhanced SEO capabilities
- Flexible deployment options

## 📚 Resources

- [Astro Documentation](https://docs.astro.build)
- [Tailwind CSS](https://tailwindcss.com)
- [MDX](https://mdxjs.com)
- [React](https://react.dev)

## 📄 License

Copyright © 2026 RAPS CLI. All rights reserved.