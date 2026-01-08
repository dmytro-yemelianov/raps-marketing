import { defineCollection, z } from 'astro:content';

const articles = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date(),
    author: z.string().default('RAPS Team'),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

const guides = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.enum(['getting-started', 'authentication', 'api', 'advanced', 'troubleshooting']),
    difficulty: z.enum(['beginner', 'intermediate', 'advanced']),
    readTime: z.number().optional(),
    order: z.number().optional(),
  }),
});

const cheatsheets = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.enum(['api', 'cli', 'authentication', 'workflows']),
    order: z.number().optional(),
    downloadUrl: z.string().optional(),
  }),
});

const campaigns = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    campaign: z.string(),
    status: z.enum(['planning', 'active', 'completed']).default('planning'),
    startDate: z.coerce.date().optional(),
    endDate: z.coerce.date().optional(),
    targetAudience: z.array(z.string()).default([]),
  }),
});

const strategy = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.enum(['brand', 'competitive', 'community', 'growth']),
    priority: z.enum(['low', 'medium', 'high']).default('medium'),
    lastUpdated: z.coerce.date(),
  }),
});

const analytics = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    metrics: z.array(z.string()).default([]),
    reportType: z.enum(['dashboard', 'framework', 'analysis']),
    frequency: z.enum(['daily', 'weekly', 'monthly', 'quarterly']).optional(),
  }),
});

const recipes = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    difficulty: z.enum(['beginner', 'intermediate', 'advanced']),
    estimatedTime: z.string(),
    prerequisites: z.array(z.string()).default([]),
    apis: z.array(z.string()).default([]),
  }),
});

const references = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.enum(['api', 'error-codes', 'scopes', 'endpoints']),
    lastUpdated: z.coerce.date(),
    completeness: z.enum(['partial', 'complete']).default('complete'),
  }),
});

const community = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    platform: z.enum(['forums', 'discord', 'reddit', 'github']),
    engagement: z.enum(['low', 'medium', 'high']).default('medium'),
    lastUpdated: z.coerce.date(),
  }),
});

const press = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    type: z.enum(['release', 'announcement', 'template']),
    publishDate: z.coerce.date().optional(),
    status: z.enum(['draft', 'approved', 'published']).default('draft'),
  }),
});

const calendar = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    calendarType: z.enum(['master', 'campaign', 'theme', 'integrated']),
    timeframe: z.string(),
    lastUpdated: z.coerce.date(),
  }),
});

export const collections = {
  'articles': articles,
  'guides': guides,
  'cheatsheets': cheatsheets,
  'recipes': recipes,
  // TODO: Add frontmatter to these collections:
  // 'campaigns': campaigns,
  // 'strategy': strategy,
  // 'analytics': analytics,
  // 'references': references,
  // 'community': community,
  // 'press': press,
  // 'calendar': calendar,
};