import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  // Native i18n: /fr and /en routes, French as default (served at root after redirect).
  i18n: {
    locales: ['fr', 'en'],
    defaultLocale: 'fr',
    routing: { prefixDefaultLocale: true },
  },
  integrations: [mdx(), svelte()],
});
