// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.grokati.com',
  trailingSlash: 'never',
  integrations: [sitemap()],
  redirects: {
    '/articles/2026-08-13-grok-resets-limits-during-grok-46-launch':
      '/articles/2026-08-13-grok-resets-limits-for-grok-46-launch',
  },
});
