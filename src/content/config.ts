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
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
