import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    source: z.string(),
    sourceUrl: z.string().url(),
    author: z.string().default('Grokati'),
    draft: z.boolean().default(false),
    featured: z.boolean().optional(),
    category: z.enum(['models', 'imagine', 'bot', 'build', 'voice']).default('models'),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    hasVideo: z.boolean().default(false),
  }),
});

export const collections = { articles };
