# Case Study: Startup MVP

## Case Study Overview

**Industry**: PropTech Startup  
**Company Size**: 10 employees  
**Project Duration**: 6 weeks  
**Engagement Type**: MVP development  

---

## The Challenge

An early-stage PropTech startup needed to build an MVP for their demo day:

### The Vision
A platform for property developers to visualize building models directly from architectural files, without needing expensive CAD software.

### Constraints
- **6-week deadline** for investor demo
- **Limited budget** ($15K total for development)
- **No APS experience** on founding team
- **Must look professional** for Series A pitch

### Technical Requirements
- Upload architectural files (RVT, DWG, IFC)
- View 3D models in browser
- Basic measurement and markup tools
- Shareable links for stakeholders

---

## The Solution

Built a focused MVP using APS Model Derivative and Viewer APIs.

### Architecture

```
┌───────────────────────────────────────────────────────┐
│                    MVP Architecture                    │
├───────────────────────────────────────────────────────┤
│                                                        │
│   ┌──────────────────────────────────────────────┐    │
│   │              React Frontend                   │    │
│   │         (Next.js + Tailwind CSS)             │    │
│   └───────────────────┬──────────────────────────┘    │
│                       │                               │
│   ┌───────────────────▼──────────────────────────┐    │
│   │             Node.js Backend                   │    │
│   │         (Express + RAPS CLI)                 │    │
│   └───────────────────┬──────────────────────────┘    │
│                       │                               │
│         ┌─────────────┼─────────────┐                │
│         ▼             ▼             ▼                │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│   │   OSS    │  │  Model   │  │  Forge   │          │
│   │  Upload  │  │Derivative│  │  Viewer  │          │
│   └──────────┘  └──────────┘  └──────────┘          │
│                                                        │
└───────────────────────────────────────────────────────┘
```

### MVP Features Delivered

**Week 1-2: Core Upload & Translation**
- Drag-and-drop file upload
- Automatic OSS bucket management
- SVF2 translation with progress

**Week 3-4: Viewer Integration**
- Embedded Forge Viewer
- Basic navigation (orbit, pan, zoom)
- Model tree with hide/show

**Week 5: Sharing & Polish**
- Shareable links with expiration
- Measurement extension
- Basic markup tools
- Responsive design

**Week 6: Testing & Demo Prep**
- Bug fixes and edge cases
- Demo script preparation
- Backup plans for demo day

---

## Key Decisions

### Why RAPS CLI as Backend Engine

Instead of writing APS SDK code from scratch:

| Approach | Development Time | Risk |
|----------|-----------------|------|
| Raw APS APIs | 3-4 weeks | High (OAuth complexity) |
| Official SDKs | 2-3 weeks | Medium |
| **RAPS CLI (shell exec)** | **1 week** | **Low (battle-tested)** |

The startup's backend simply shells out to RAPS:

```javascript
const { exec } = require('child_process');

async function uploadAndTranslate(filePath) {
  // Upload to OSS
  const uploadResult = await execRaps(`object upload ${BUCKET} ${filePath} --output json`);
  const urn = JSON.parse(uploadResult).objectId;
  
  // Start translation
  await execRaps(`translate start ${urn} --format svf2 --output json`);
  
  return urn;
}

async function checkStatus(urn) {
  const result = await execRaps(`translate status ${urn} --output json`);
  return JSON.parse(result);
}
```

This approach:
- ✅ Eliminated weeks of OAuth debugging
- ✅ Handled edge cases (chunking, retry) automatically
- ✅ Provided JSON output for easy parsing
- ✅ Allowed focus on product features, not API plumbing

---

## Results

### Demo Day Success
- ✅ Working product for investor demo
- ✅ Processed 20+ models live during presentation
- ✅ Investors impressed with polish level
- ✅ **Secured $1.2M seed round**

### Technical Metrics

| Metric | Result |
|--------|--------|
| Development time | 6 weeks |
| Total cost | $14,500 |
| Uptime during demo | 100% |
| Model processing success rate | 98% |
| Average translation time | 3-8 minutes |

### Post-MVP Roadmap

After funding, the plan includes:
1. Replace shell exec with proper SDK integration
2. Add Design Automation for parametric features
3. Implement multi-tenant architecture
4. Add collaboration features

---

## Founder Testimonial

> "We had zero experience with Autodesk APIs and needed something working in 6 weeks. The RAPS approach got us to demo day with a product that actually worked. The investors thought we'd been building for months."
> 
> — *CTO, [Startup]*

---

## Lessons Learned

### What Worked
1. **Pragmatic Architecture**: Shell exec to CLI was "good enough" for MVP
2. **Focused Scope**: Said no to features that weren't demo-critical
3. **Progress Indicators**: Users wait patiently when they see progress
4. **Fallback Plans**: Had backup translated models for demo day

### What We'd Do Differently
1. **Earlier Viewer Testing**: Some file types took longer than expected
2. **Better Error Messages**: End users need friendly errors
3. **Usage Analytics**: Should have added from day one

---

## Technologies Used

- **Frontend**: Next.js, React, Tailwind CSS
- **Backend**: Node.js, Express
- **CLI**: RAPS (for APS operations)
- **Viewer**: Autodesk Forge Viewer
- **Hosting**: Vercel (frontend) + Railway (backend)
- **Storage**: APS OSS (transient buckets)

---

## Budget Breakdown

| Item | Cost |
|------|------|
| Development (6 weeks @ $2K/week) | $12,000 |
| APS Cloud Credits | $500 |
| Hosting (3 months) | $300 |
| Design/Polish | $1,700 |
| **Total** | **$14,500** |

---

## Replicable for Your Startup

This MVP approach works for:
- Property visualization platforms
- Construction management tools
- Architectural collaboration apps
- Manufacturing part viewers
- Any product needing CAD viewing

**Key Insight**: Don't reinvent APS integration for an MVP. Use RAPS to get to market fast, then optimize later.
