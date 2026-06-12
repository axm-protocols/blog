// Minimal i18n: a UI string dictionary + tiny helpers. Post content itself lives
// in the markdown files (<slug>.fr.md / <slug>.en.md); this only covers chrome.

export const LANGS = ['fr', 'en'] as const;
export type Lang = (typeof LANGS)[number];
const DEFAULT_LANG: Lang = 'fr';

export const ui = {
  fr: {
    'site.name': 'Gabriel Jarry',
    'nav.home': 'Accueil',
    'nav.blog': 'Blog',
    'home.latest': 'Derniers billets',
    'blog.title': 'Tous les billets',
    'post.back': '← Tous les billets',
    'post.readingNote': 'Cet article existe aussi en',
  },
  en: {
    'site.name': 'Gabriel Jarry',
    'nav.home': 'Home',
    'nav.blog': 'Blog',
    'home.latest': 'Latest posts',
    'blog.title': 'All posts',
    'post.back': '← All posts',
    'post.readingNote': 'This article is also available in',
  },
} as const;

export function t(lang: Lang, key: keyof (typeof ui)['fr']): string {
  return ui[lang][key] ?? ui[DEFAULT_LANG][key];
}
