import { defineCollection, z } from 'astro:content';

// One blog collection. Each post is a file named <slug>.<lang>.md so the FR/EN
// versions of the same article share a slug and differ only by the lang segment.
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    lang: z.enum(['fr', 'en']),
    key: z.string(),         // SHARED across languages → pairs FR/EN for the toggle
    urlslug: z.string(),     // localized URL segment (slug is reserved by Astro)
    accessibilite: z.number().int().min(1).max(3).optional(),  // 1 grand public · 2 quelques notions · 3 initiés
    draft: z.boolean().default(false),      // exclu du build → aucune URL
    unlisted: z.boolean().default(false),   // construit et accessible par lien direct, mais absent de la liste
  }),
});

export const collections = { blog };
