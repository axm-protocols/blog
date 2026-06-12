# blog

Personal blog of Gabriel Jarry — notes on agentic AI and how I work with it.
Built with [Astro](https://astro.build) + Svelte islands, bilingual (FR/EN),
deployed on Cloudflare Pages at **https://gabriel.axm-protocols.io**.

## Develop

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static output -> dist/
```

## Write a post

Add two files under `src/content/blog/`, sharing the same `key`:

- `my-topic.fr.mdx` — `lang: fr`, `urlslug: mon-sujet`
- `my-topic.en.mdx` — `lang: en`, `urlslug: my-topic`

Frontmatter: `title`, `description`, `date`, `lang`, `key` (shared FR/EN, drives
the language toggle), `urlslug` (localized URL segment). MDX lets you import a
Svelte component (e.g. an interactive chart) and drop it into the prose.

## Deploy

Pushes to `main` trigger `.github/workflows/deploy.yml`, which builds the site and
deploys it to the Cloudflare Pages project **`blog`** via `wrangler-action`.

Required GitHub repository secrets:

- `CLOUDFLARE_API_TOKEN` — a token with the **Cloudflare Pages: Edit** permission.
- `CLOUDFLARE_ACCOUNT_ID` — the account ID.

The custom domain `gabriel.axm-protocols.io` is attached to the `blog` Pages
project once (Cloudflare dashboard → Pages → blog → Custom domains, or
`wrangler pages domain add gabriel.axm-protocols.io --project-name=blog`); DNS is
created automatically since the zone is already on Cloudflare.

### Manual deploy (optional)

```bash
npm run build
npx wrangler pages deploy dist --project-name=blog
```
