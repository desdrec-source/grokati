// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Canonical site URL — match the primary host (www) used in production
export default defineConfig({
  site: 'https://www.grokati.com',
  trailingSlash: 'never',
  integrations: [sitemap()],
});