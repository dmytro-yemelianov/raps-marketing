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

export const collections = {
  'articles': articles,
  'guides': guides,
  'cheatsheets': cheatsheets,
};