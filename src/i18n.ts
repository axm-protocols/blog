// Minimal i18n: a UI string dictionary + tiny helpers. Post content itself lives
// in the markdown files (<slug>.fr.md / <slug>.en.md); this only covers chrome.

export const LANGS = ['fr', 'en'] as const;
export type Lang = (typeof LANGS)[number];
export const DEFAULT_LANG: Lang = 'fr';

export const ui = {
  fr: {
    'site.name': 'Gabriel Jarry',
    'site.tagline': "Notes sur l'IA, la vérification et ce qui se trouve entre les deux.",
    'nav.home': 'Accueil',
    'nav.blog': 'Blog',
    'home.intro':
      "Je travaille sur la vérification des systèmes d'IA — comment savoir, et prouver, qu'un modèle fait ce qu'il prétend. J'écris ici des notes de fond, en français et en anglais.",
    'home.latest': 'Derniers billets',
    'blog.title': 'Tous les billets',
    'blog.all': 'Tous les billets',
    'post.back': '← Tous les billets',
    'post.readingNote': 'Cet article existe aussi en',
  },
  en: {
    'site.name': 'Gabriel Jarry',
    'site.tagline': 'Notes on AI, verification, and what sits between them.',
    'nav.home': 'Home',
    'nav.blog': 'Blog',
    'home.intro':
      "I work on verifying AI systems — how to know, and prove, that a model does what it claims. I write long-form notes here, in French and English.",
    'home.latest': 'Latest posts',
    'blog.title': 'All posts',
    'blog.all': 'All posts',
    'post.back': '← All posts',
    'post.readingNote': 'This article is also available in',
  },
} as const;

export function t(lang: Lang, key: keyof (typeof ui)['fr']): string {
  return ui[lang][key] ?? ui[DEFAULT_LANG][key];
}

export const otherLang = (lang: Lang): Lang => (lang === 'fr' ? 'en' : 'fr');
export const langLabel: Record<Lang, string> = { fr: 'Français', en: 'English' };
