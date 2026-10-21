# Cutover runbook: zotregistry.dev to Mintlify

Target state:

| Host | Serves | Hosted on |
|---|---|---|
| `docs.zotregistry.dev` | Documentation (this repo) | Mintlify |
| `zotregistry.dev` | Landing page, old-URL redirects, Go vanity import | GitHub Pages |
| `zotregistry.dev/helm-charts` | Helm repository (unchanged) | GitHub Pages (`project-zot/helm-charts`) |

Steps marked **(you)** need an account owner or DNS access. Nothing here has been done yet.

## Why the apex stays on GitHub Pages

`go get zotregistry.dev/zot/v2` fetches `https://zotregistry.dev/zot/v2?go-get=1` and reads a `go-import` meta tag. The module path is used in 434 files of the zot repository, so it must keep resolving. Mintlify can't serve those tags, so the apex stays static. `landing/` already contains them at `/`, `/zot/` and `/zot/v2/`.

## 1. Before you start

- [ ] Merge this repository's docs to its default branch.
- [ ] `mint validate` and `mint broken-links` pass in CI.
- [ ] Review the open questions in `drafts/MIGRATION.md` with the zot maintainers. Several statements in the docs depend on their answers.
- [ ] Retake the web UI screenshots (`images/`) with the current UI. They still show the old logo.

## 2. Publish docs on a Mintlify subdomain (you)

1. `mint login` (or `mint signup`), then connect this repository with the Mintlify GitHub app in the dashboard.
2. Confirm the site builds at the `*.mintlify.site` URL shown by `mint status`.
3. In the dashboard, add the custom domain `docs.zotregistry.dev`. Mintlify shows the DNS target.
4. In DNS, add `CNAME docs → <target from Mintlify>`. Wait for the certificate to issue.
5. Check: `curl -sI https://docs.zotregistry.dev/ | head -1`, plus the version switcher and an API endpoint page.

## 3. Switch the apex to the landing page (you)

The apex site is served from `project-zot/project-zot.github.io`.

1. Back up the `gh-pages` branch (for example, push it to `gh-pages-mkdocs-archive`).
2. Replace the site content with `landing/` from this repository: `index.html`, `404.html`, `assets/`, `latest/`, `zot/`, `CNAME`, `.nojekyll`.
   - Remove the old mike versioned directories so they don't shadow the redirect pages. `landing/latest/` and `404.html` redirect old URLs, including `/vX.Y.Z/...`.
3. Retire the MkDocs deploy in that repository: disable `deploy.yml` and archive `mkdocs.yml`, `docs/` and `material/`.
4. Keep the `CNAME` file (`zotregistry.dev`).

Alternative: deploy `landing/` from this repository with `.github/workflows/landing-pages.yml`. That needs the apex custom domain to move to this repository's Pages site, and `helm-charts` must still resolve under the apex domain. Verify before you choose it.

## 4. Verify

```bash
# Go vanity import still works
curl -s 'https://zotregistry.dev/zot/v2?go-get=1' | grep go-import
go list -m zotregistry.dev/zot/v2@latest

# Helm repository still works
curl -sI https://zotregistry.dev/helm-charts/index.yaml | head -1
helm repo add project-zot https://zotregistry.dev/helm-charts && helm search repo project-zot

# Old URLs redirect (follow redirects, show the final URL)
for p in latest/articles/mirroring/ v2.1.22/user-guides/zli/ articles/docker/; do
  curl -sIL -o /dev/null -w "%{url_effective} %{http_code}\n" https://zotregistry.dev/$p
done
```

Expected: the last loop ends on `https://docs.zotregistry.dev/...` pages. The unknown-path fallback is a client-side redirect in `404.html`, so test it in a browser.

## 5. Update references

- [ ] `README.md` in `project-zot/zot`: "Documentation for zot is located at https://zotregistry.dev" to `https://docs.zotregistry.dev`.
- [ ] GitHub repository website field and description for `project-zot/zot`.
- [ ] Helm chart `home` URL and README, and the Artifact Hub listing.
- [ ] `Documentation=` line in the systemd unit shown in `install/linux.mdx` (it points at `https://zotregistry.dev/`, which still works).
- [ ] CNCF landscape and any CNCF project page that links the old docs.
- [ ] Submit `https://docs.zotregistry.dev/sitemap.xml` to search consoles.

## Known limitations

- Anchors from old URLs are carried over but many headings changed, so some links land at the top of the page.
- `404.html` redirects client-side and returns HTTP 404 for those paths. The 41 main pages under `/latest/` have real redirect pages. Versioned paths (`/v2.1.22/...`) rely on the fallback.
- The `v2.1.x` snapshot is identical to latest today, so both versions appear in search. `seo.indexing: navigable` is set, but consider restricting indexing of snapshots once they diverge.
- The spellcheck workflow is advisory and untested (no `aspell` available when it was written).
- Analytics are not configured. Add them in the Mintlify dashboard if wanted.

## Rollback

1. Restore the previous apex content from the archive branch and re-enable the MkDocs deploy.
2. Remove the `docs` CNAME (or leave it, it's harmless).
3. The old site and the new docs can run side by side indefinitely, since they live on different hosts.
