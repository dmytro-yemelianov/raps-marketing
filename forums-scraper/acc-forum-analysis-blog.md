---
title: "4,295 Feature Requests, 60 Delivered: Inside Autodesk's ACC Feedback Black Hole"
description: "We analyzed every idea submitted to Autodesk Construction Cloud's feedback forum. The data reveals a 96.6% abandonment rate and years-old requests still waiting."
date: 2026-01-16
author: "Dmytro Yemelianov"
tags: ["acc", "autodesk", "data-analysis", "developer-experience", "aec"]
keywords: ["ACC forum analysis", "Autodesk Construction Cloud", "BIM360", "feature requests", "APS developer"]
raps_commands: ["raps acc projects", "raps acc users"]
---

# 4,295 Feature Requests, 60 Delivered: Inside Autodesk's ACC Feedback Black Hole

**TL;DR:** We scraped and analyzed 4,295 ideas from Autodesk Construction Cloud's official feedback forum. Only 1.4% have been implemented. The #1 most-voted request has been ignored for 6+ years. Here's the full breakdown.

---

## The Data

Between December 2021 and January 2026, Autodesk Construction Cloud users submitted **4,295 feature requests** to the official ACC Ideas forum. These aren't random complaints — they're structured proposals with voting, discussion threads, and official status tracking.

We collected every single one.

| Metric | Value |
|--------|-------|
| Total ideas submitted | 4,295 |
| Total community votes (kudos) | 24,615 |
| Total views | 1,098,872 |
| Date range | Dec 2021 – Jan 2026 |

The question we wanted to answer: **What happens to user feedback?**

---

## The 96.6% Problem

Here's the status distribution:

| Status | Count | Percentage |
|--------|-------|------------|
| Gathering Support | 4,149 | **96.6%** |
| Implemented | 60 | 1.4% |
| Accepted | 37 | 0.9% |
| Under Review | 30 | 0.7% |
| Future Consideration | 18 | 0.4% |

Let that sink in. **96.6% of all feature requests sit in "Gathering Support" indefinitely.** This status means: acknowledged, but not being worked on, with no timeline or commitment.

Only 60 ideas — 1.4% — have actually shipped.

![Status Distribution Chart](/images/blog/acc-analysis/status-distribution.png)

---

## The Oldest Wounds

Some high-voted requests have been waiting for years:

### #1: "Allow adding users to MULTIPLE PROJECTS" — 344 kudos

> *"There is a major need to be able to add a new hire to many projects in ACC. Instead of wasting my time opening each project and manually adding a new user to 20 projects, we need a tool that will automate this process!"*

This request was **originally submitted to BIM360 SIX YEARS AGO**. It was marked "Under Review" two weeks after submission. Zero response since.

Current status: **Future Consideration** (since April 2024)

### #2: "ACC Markups need improving" — 246 kudos, 77 replies

> *"The markups in Autodesk Docs are terrible. BIM 360 Docs Markups are far superior. Put simply, we need BIM 360 Markups in Autodesk Docs."*

Submitted: **December 2021** — over 4 years ago.

Current status: **Future Consideration**

### #3: "Remove Inherited Permissions" — 175 kudos

A basic permission management feature requested in December 2023. Still waiting.

---

## What Users Actually Want

We categorized all 4,295 ideas by topic. Here's where the pain concentrates:

| Category | Ideas | Total Kudos | Avg Kudos/Idea |
|----------|-------|-------------|----------------|
| Documents & Files | 1,697 | 10,960 | 6.5 |
| User Management & Permissions | 1,505 | 10,368 | 6.9 |
| Viewer & 3D | 1,583 | 10,222 | 6.5 |
| Submittals & RFIs | 992 | 5,900 | 5.9 |
| Photos & Media | 311 | 2,844 | **9.1** |

**Photos & Media** has the highest average engagement per idea (9.1 kudos) despite fewer total submissions. This suggests intense, focused frustration:

- No folder organization for photos (131 kudos)
- No permission controls for photos (100 kudos)  
- No bulk editing (92 kudos)

These are basic features users desperately want.

---

## The Bulk Operations Gap

We identified a pattern: **bulk/batch operations** appear across every category.

| Pain Pattern | Ideas | Kudos |
|--------------|-------|-------|
| Missing features (general) | 1,068 | 6,622 |
| UX/workflow friction | 634 | 4,793 |
| **Bulk/batch operations** | 490 | 3,860 |
| Permissions complexity | 504 | 3,251 |
| Export limitations | 420 | 2,480 |

Users want to:
- Add users to multiple projects at once
- Edit multiple photos simultaneously
- Export permissions across folders
- Bulk update issues, submittals, RFIs

ACC forces everything to be done one-by-one.

---

## The 2025 Explosion

Submission volume has grown dramatically:

| Year | Ideas | Growth |
|------|-------|--------|
| 2023 | 35 | — |
| 2024 | 733 | 20x |
| 2025 | 3,400 | **4.6x** |

3,400 ideas in 2025 alone. Either ACC adoption is exploding, user frustration is peaking, or both.

---

## International Signal: Japan

We noticed 59 Japanese-language submissions, with 23 appearing on a single day (September 30, 2025). This suggests organized feedback campaigns from Japanese construction firms — a signal that ACC is expanding into enterprise markets with enterprise-scale requirements.

Sample requests (translated):
- Free entry fields per form question
- Auto-save for photos
- Enhanced search functionality
- Faster issue status updates

---

## What Actually Gets Implemented?

Of the 60 implemented ideas, the highest-voted was:

**"Measure coordinate XYZ in 3D view"** — 276 kudos

This took years to ship. Other implementations:
- View all projects a user is assigned to (91 kudos)
- Export permissions overview (68 kudos)  
- Scrollable PDFs (61 kudos)

Notice these are relatively small quality-of-life improvements, not the structural changes users request most.

---

## The Competitive Landscape

Third-party tools like [Naviate Cloud Manager](https://www.naviate.com/naviate-for-acc/naviate-cloud-manager/) have emerged to fill gaps — specifically bulk user management and project creation.

But Naviate:
- Requires enterprise licensing (no public pricing)
- Is Windows desktop-only (300MB+ installer)
- Covers projects + members, but not photos, permissions auditing, submittals, or document metadata
- Can't be scripted or integrated into CI/CD pipelines

The gap remains wide open for developer-focused tooling.

---

## What This Means for Developers

If you're building on APS/ACC, this data suggests:

1. **Don't wait for Autodesk** — high-priority requests languish for years
2. **API automation is underserved** — 145 ideas explicitly request programmatic access
3. **Bulk operations = instant value** — any tool that batches ACC operations solves real pain
4. **Permission management is broken** — auditing and inheritance controls are desperately needed

---

## The RAPS Angle

Full disclosure: I built [RAPS CLI](https://rapscli.xyz) to solve some of these problems programmatically.

Where ACC's UI forces click-by-click workflows, `raps` lets you script it:

```bash
# List all projects you have access to
raps acc projects list

# Export project members to CSV
raps acc users list --project "Building-A" --format csv > members.csv

# Bulk operations via scripting
for project in $(raps acc projects list --format json | jq -r '.[].id'); do
  raps acc users add --project $project --email "newuser@company.com"
done
```

It won't fix Autodesk's forum abandonment rate, but it gives developers a way to route around the limitations.

---

## Methodology

**Data collection:** We scraped the ACC Ideas forum (`forums.autodesk.com/t5/acc-ideas/`) in January 2026, collecting all publicly visible ideas with metadata (title, body, kudos, views, replies, status, dates).

**Analysis:** Python (pandas) for categorization and statistics. Topic classification used keyword matching against 18 category groups.

**Limitations:** 
- Only public forum data (no internal Autodesk metrics)
- Keyword categorization may misclassify edge cases
- "Gathering Support" may include ideas Autodesk is tracking internally

**Full code and data:** [github.com/dmytro-yemelianov/raps-research](https://github.com/dmytro-yemelianov/raps-research)

---

## Conclusion

The ACC Ideas forum is where feature requests go to die. With a 96.6% abandonment rate and top requests ignored for 6+ years, users have learned that feedback rarely translates to product changes.

This isn't necessarily malice — large enterprises struggle to prioritize thousands of competing demands. But the data reveals a systematic gap between what users need and what Autodesk delivers.

For developers and power users, the practical response is: **build or buy workarounds**. The API exists. The pain points are documented. The only question is who fills the vacuum.

---

*Have data or analysis to add? [Open an issue](https://github.com/dmytro-yemelianov/raps-research/issues) or reach out on [LinkedIn](https://linkedin.com/in/dmytro-yemelianov).*

---

**Related:**
- [RAPS CLI Documentation](/docs/)
- [ACC API Troubleshooting Guide](/learn/troubleshooting/)
- [BIM360 to ACC Migration](/learn/guides/migration/)
