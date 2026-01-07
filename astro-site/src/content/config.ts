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

const crossPlatform = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    platform: z.array(z.enum(['aps', 'onshape', 'solidworks', 'teamcenter', 'nx', 'all'])),
    painPoint: z.enum(['authentication', 'translation', 'sdk', 'documentation', 'errors', 'webhooks']),
    severity: z.enum(['low', 'medium', 'high', 'critical']),
    publishDate: z.coerce.date(),
  }),
});

export const collections = {
  'articles': articles,
  'guides': guides,
  'cross-platform': crossPlatform,
};