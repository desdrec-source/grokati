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
    category: z.enum(['models', 'imagine', 'bot', 'build', 'voice']).default('models'),
  }),
});

export const collections = { articles };