import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const articles = await getCollection('articles', ({ data }) => !data.draft);
  const sorted = articles.sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
  );

  return rss({
    title: 'Grokati — Grok & xAI News',
    description: 'High-signal, accurate coverage of Grok and xAI updates. Accuracy over volume.',
    site: context.site!,
    items: sorted.map((article) => ({
      title: article.data.title,
      description: article.data.description,
      pubDate: article.data.pubDate,
      link: `/articles/${article.id}`,
      // Include source for transparency
      customData: `<source>${article.data.source}</source>`,
    })),
    customData: `<language>en-us</language>`,
  });
}
