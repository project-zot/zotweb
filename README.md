# zot documentation

Source for the [zot](https://github.com/project-zot/zot) documentation site, built with [Mintlify](https://mintlify.com) and published at **https://docs.zotregistry.dev**. The apex domain, `zotregistry.dev`, is a static landing page (see [`landing/`](landing)) that also serves the Go vanity import for `zotregistry.dev/zot/v2`.

## Preview locally

```bash
npm install -g mint
mint dev            # http://localhost:3000
```

Checks that CI runs:

```bash
mint validate       # build validation
mint broken-links   # internal link check
```

## Layout

| Path | What it holds |
|---|---|
| `docs.json` | Site config: branding, navigation (tabs, versions), redirects, SEO |
| `index.mdx`, `quickstart.mdx`, `features.mdx` | Get started |
| `concepts/`, `install/`, `configuration/`, `security/`, `operations/` | Documentation |
| `use/`, `clients/`, `guides/` | Using zot, client setup, tutorials |
| `api-reference/` | Hand-written API pages and `openapi.yaml` (generates endpoint pages) |
| `developers/`, `community/`, `changelog.mdx` | Contributing, project, release notes |
| `v2.1.x/` | **Generated** snapshot of a released docs line. Don't edit by hand. |
| `landing/` | Static apex site, redirects for old URLs, Go vanity import |
| `scripts/` | Maintenance scripts (below) |
| `drafts/` | Migration notes and the cutover runbook. Not published. |
| `AGENTS.md` | Terminology and style rules for writers and AI tools |

## Writing

Follow [`AGENTS.md`](AGENTS.md): sentence-case headings, second person, absolute internal links (`/security/authentication`), and Mintlify components rather than Markdown extensions. Verify config keys and flags against the zot repository (`swagger/`, `examples/`, `pkg/`) instead of copying from older docs.

Edit the **latest** pages at the repository root. They describe `main`.

## Brand

The logo is a shield on a rounded block with a Z in the middle, with an indigo-to-violet gradient (`#4F46E5` to `#7C3AED`). Files: `logo/light.svg`, `logo/dark.svg` (lockups), `logo/mark.svg` (mark only), `favicon.svg`, and `images/og.png` (social image). Copies for the landing page are in `landing/assets/`. The `zot` wordmark is outlined from the [Outfit](https://github.com/Outfitio/Outfit-Fonts) typeface (SIL Open Font License 1.1).

## Maintenance tasks

### Add or change a page

1. Create or edit the `.mdx` file with `title`, `description` and `icon` frontmatter.
2. Add it to `navigation.versions[0]` (`latest`) in `docs.json`.
3. If you renamed or removed a published URL, add it to `scripts/redirect-map.json`, then run `python3 scripts/build-redirects.py`.

### Snapshot a release line

When a release line should stop receiving doc changes (for example `v2.2.x`), freeze it from the current latest pages:

```bash
python3 scripts/snapshot-version.py v2.2.x
mint validate
```

The script copies the pages to `v2.2.x/`, rewrites their internal links, and adds the version to `docs.json`. Re-running it for the same label rebuilds that snapshot from latest, so only do that while the line is still current. Backport fixes to an older line by editing its folder directly.

### Refresh the API reference

`api-reference/openapi.yaml` is derived from `swagger/swagger.yaml` in the zot repository, converted from Swagger 2.0 to OpenAPI 3 and then adjusted by hand (server, security schemes, tags, response codes). Regenerate it per release and re-apply the adjustments, then compare the endpoint list with `pkg/api/routes.go`. Endpoints that are not in the spec are documented in `api-reference/extensions.mdx`.

### Redirects from the previous site

Old MkDocs URLs (`/<version>/<section>/<page>/`) are mapped in `scripts/redirect-map.json`. `scripts/build-redirects.py` writes them to `docs.json` (docs-domain redirects) and to `landing/` (apex-domain redirect pages and the `404.html` fallback). CI fails if the generated files are out of date.

## Deployment

See [`drafts/CUTOVER.md`](drafts/CUTOVER.md) for the one-time domain cutover and rollback plan.
