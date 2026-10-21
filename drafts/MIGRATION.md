# zotregistry.dev migration map

Source: `project-zot.github.io/docs/` (MkDocs). Target: Mintlify MDX in this repo.
`drafts/` is excluded from publishing via `.mintignore`.

Status key: **keep** = convert, light edit · **split** = break into several pages · **merge** = fold into another page · **rewrite** = new text using old as source · **new** = no source page · **drop**

## Audit findings

- Only mkdocs macro in content: `{% raw %}` blocks in `articles/kind-deploy.md` (strip them; keep the `{{.State.Running}}` Go templates).
- Pages that exist but are **not in the mkdocs nav**: `articles/cve-scanning.md` (522 lines), `articles/events.md` (145). Both are linked from other pages; promote them into the nav.
- `articles/clustering.md` is a 4-line stub; real content is `scaleout.md` and `high-availability.md`. Merge into one **Clustering** section.
- `general/glossary.md` opens with a table of emoji admonition icons (`:pencil2:`, `:bulb:`, `:warning:`). Replace with Mintlify callouts and drop that section.
- `general/whats-new.md` is 703 lines in one page (v2.1.10 - v2.1.22 and earlier). Move to a Changelog using `<Update>` components, one per release.
- `developer-guide/api-reference.md` (1,101 lines) is hand-written; `zot/swagger/swagger.yaml` covers only 15 paths (dist-spec, catalog, `_zot/ext/*`, `/zot/auth/*`). Use OpenAPI for those; keep hand-written pages for what swagger lacks (GraphQL `/v2/_zot/ext/search`, mgmt details, ORAS referrers). **Verify per endpoint before deleting.**
- `admin-guide/admin-configuration.md` (610 lines) mixes overview and reference; split by config section.
- `articles/authn-authz.md` (1,116 lines) and `articles/graphql.md` (1,057 lines) are too long to navigate; split.
- Copyright/trademark footer text: copy from `mkdocs.yml` `copyright`.
- 111 relative `../x.md` links to rewrite.
- 422-entry spellcheck wordlist (`.wordlist.txt`) is usable as a terminology seed and CI spell-check input.

### Launch blocker: Go vanity import path

`mkdocs`/`mike` deploy publishes `go-import/redirect.html` and `docs/v2/index.html` so that `zotregistry.dev/zot/v2` resolves to `github.com/project-zot/zot` for `go get` (meta `go-import` tag). **Mintlify cannot serve custom `<meta>` HTML at arbitrary paths**, so moving the apex domain would break `go get zotregistry.dev/zot/v2`. Options (decide before Phase 5):
1. Keep `zotregistry.dev` on GitHub Pages serving only the vanity redirect, and put Mintlify on `docs.zotregistry.dev`.
2. Put a small proxy/edge rule in front that answers `?go-get=1` requests.
3. Change the module path (breaking; not recommended).

**Decided:** option 1. Docs live at `docs.zotregistry.dev` (Mintlify); the apex `zotregistry.dev` is a static landing page in `landing/` (GitHub Pages, `CNAME` included) that also serves the `go-import` meta tags at `/`, `/zot/` and `/zot/v2/`.

## Decisions (2026-10-20)

- 3 tabs: Documentation (Guides folded in), API reference, Developers.
- Versions: `latest` now; a `v2.1.x` snapshot is created in Phase 5 once content is stable (Mintlify versions need a copied page tree).
- Config examples: ~12 curated scenarios, not all 60+.
- `introduction.mdx` is `index.mdx` in the new structure.
- Swagger is **2.0**; Mintlify needs OpenAPI 3.x. Convert (e.g. `swagger2openapi`) in Phase 4 and check endpoints against the hand-written reference.
- Redirects must cover moving from `zotregistry.dev/<old path>` to `docs.zotregistry.dev/<new path>`; keep old-path stubs on the apex site (or a redirect map in `landing/404.html`).

## Page map

| Source (`docs/…`) | Lines | Target | Status |
|---|---|---|---|
| `index.md` + `material/overrides/home.html` | 4 | `index.mdx` | rewrite (hero + cards) |
| `general/concepts.md` | 95 | `introduction.mdx` | merge (with `project.md` intro) |
| `general/features.md` | 37 | `features.mdx` | rewrite (feature cards, linked) |
| `general/architecture.md` | 101 | `concepts/architecture.mdx` | keep |
| `general/extensions.md` | 83 | `concepts/extensions.mdx` | keep |
| `general/glossary.md` | 39 | `reference/glossary.mdx` | keep, drop icon table |
| `general/releases.md` | 155 | `install/releases.mdx` | keep |
| `general/whats-new.md` | 703 | `changelog.mdx` | split into `<Update>` per release |
| `general/project.md` | 19 | `community/about.mdx` | keep + expand |
| (`zot/COMPARISON.md`) | — | `concepts/comparison.mdx` | rewrite from repo file |
| `admin-guide/admin-getting-started.md` | 285 | `quickstart.mdx` + `install/binary.mdx` | split/rewrite |
| `install-guides/install-guide-linux.md` | 318 | `install/linux.mdx` | keep (Steps) |
| `install-guides/install-guide-k8s.md` | 369 | `install/kubernetes-helm.mdx` | keep |
| `articles/docker.md` | 352 | `install/docker.mdx` (server) + `clients/docker.mdx` (client) | split |
| `articles/kind-deploy.md` | 218 | `guides/kind.mdx` | keep, strip `{% raw %}` |
| (none) | — | `install/upgrade.mdx` | new |
| `admin-guide/admin-configuration.md` | 610 | `configuration/overview.mdx`, `…/http.mdx`, `…/log.mdx`, `…/extensions.mdx`, `…/background-tasks.mdx`, … | split |
| `articles/storage.md` | 745 | `configuration/storage/{overview,local,s3,gcs,azure,cache-drivers}.mdx` | split |
| (`zot/examples/config-*.json`) | — | `configuration/examples.mdx` | new (curated) |
| `articles/authn-authz.md` | 1116 | `security/{authentication,mtls,ldap,openid,api-keys,access-control}.mdx` | split |
| `articles/verifying-signatures.md` | 236 | `security/signatures.mdx` | keep |
| `articles/immutable-tags.md` | 49 | `security/immutable-tags.mdx` | keep |
| `articles/security-posture.md` | 106 | `security/posture.mdx` | keep |
| `articles/cve-scanning.md` | 522 | `security/cve-scanning.mdx` | keep, promote to nav |
| `articles/retention.md` | 302 | `operations/retention-gc.mdx` | keep (+ GC from admin-config) |
| `articles/mirroring.md` | 712 | `operations/mirroring.mdx` | keep, tabs per mode |
| `articles/high-availability.md` | 41 | `operations/clustering/high-availability.mdx` | keep |
| `articles/scaleout.md` | 361 | `operations/clustering/scale-out.mdx` | keep |
| `articles/clustering.md` | 4 | `operations/clustering/overview.mdx` | rewrite (stub) |
| `articles/monitoring.md` | 163 | `operations/monitoring.mdx` | keep |
| `articles/events.md` | 145 | `operations/events.mdx` | keep, promote to nav |
| `articles/benchmarking-with-zb.md` | 143 | `operations/benchmarking-zb.mdx` | keep |
| `articles/pprofiling.md` | 129 | `operations/profiling.mdx` | keep |
| (none) | — | `operations/backup-restore.mdx`, `operations/troubleshooting.mdx`, `operations/production-checklist.mdx` | new |
| `user-guides/user-guide-datapath.md` | 305 | `use/push-pull.mdx` (CodeGroup per tool) | keep |
| `user-guides/user-guide-gui.md` | 102 | `use/web-ui.mdx` | keep |
| `user-guides/zli.md` | 560 | `use/zli.mdx` + `use/zli-reference.mdx` | split |
| `articles/graphql.md` | 1057 | `use/search-graphql.mdx` + `use/graphql-examples.mdx` | split |
| `articles/containerd.md` | 54 | `clients/containerd.mdx` | keep |
| `articles/building-ci-cd-pipeline.md` | 112 | `guides/ci-cd-pipeline.mdx` | keep |
| `articles/workflow.md` | 331 | `guides/provenance-workflow.mdx` | keep |
| (none) | — | `clients/compatibility.mdx` | new |
| `developer-guide/api-user-guide.md` | 288 | `api-reference/introduction.mdx` | keep |
| `developer-guide/api-reference.md` | 1101 | OpenAPI pages from swagger + `api-reference/{search,mgmt,…}.mdx` | rewrite (verify vs swagger) |
| `developer-guide/onboarding.md` | 197 | `developers/onboarding.mdx` | keep |
| `developer-guide/extensions-dev.md` | 74 | `developers/extensions.mdx` | keep |
| `developer-guide/contributing.md` | 63 | `developers/contributing.mdx` | keep |
| `docs/v2/index.html`, `go-import/redirect.html` | — | n/a | **drop from site**; see vanity import blocker |

Assets: `docs/assets/images/*` (jpg/png/svg) -> `images/`, rename to descriptive kebab-case, add alt text. Drop `assets/images/logo.svg` (replaced).

## Redirects (to finish in Phase 5)

Old mkdocs URLs use `/articles/<name>/`, `/admin-guide/…`, `/install-guides/…`, `/user-guides/…`, `/developer-guide/…`, `/general/…`. Every row above gives the target; generate `docs.json` `redirects` from this table.

## Progress

**Batch 1 done (2026-10-20):** `index`, `quickstart`, `features`, `concepts/{architecture,extensions,comparison}`, `reference/glossary`, `install/{choose-method,linux,docker,kubernetes-helm,releases,upgrade}`, `clients/docker`. `mint validate` and `mint broken-links` pass.

Fixes made while migrating (verify with maintainers):
- Removed `{{ git.tag }}` macro (Linux and Helm guides); Linux download uses `releases/latest/download/`.
- `make image` and `make binary-stacker` do not exist; real targets are `docker-image` and `oci-image`.
- `adduser --gecos --disabled-login` consumed the flag as the GECOS value; now `--gecos ""`. User creation moved before the service unit.
- Replaced leftover `zothub.io` cert paths with `registry.example.com`.
- `zot/COMPARISON.md` is stale (zot v1.3.0, says not a CNCF project); not migrated. Comparison page is qualitative with no competitor table.
- Open question: Helm repo URL `https://zotregistry.dev/helm-charts` must keep working after the apex moves to the landing page (it is served by the org's GitHub Pages).
- Open question: Dockerfile-built images have no extensions in the default config; published (stacker) images enable search/ui/mgmt.

**Batch 2 done (2026-10-20):** `configuration/*` (6 + 6 storage) and `security/*` (10). Pages verified against `../zot` by four parallel reviewers; `mint validate` and `mint broken-links` pass.

Corrections to old docs (verified in code): mTLS `tls` belongs under `http.tls` (`cacert` enables mTLS); login URL is `/zot/auth/login`; LDAP TLS on by default; htpasswd checked before LDAP; hot reload is file-watcher based and covers more than authz; rate limit is per client IP; binary does not create `config.json`; `extensions.mgmt`/`apikey` ignored; `ui` requires `search`; CVE scanning rejected with remote storage; S3 `forcepathstyle` defaults to false; no `prometheus.readTimeout/writeTimeout`; added undocumented keys (CEL `conditions`, `disableAnonymousCatalog`, `externalUrl`, `allowOrigin`, Trivy options, API key section).

Open questions for maintainers:
- `storage.fastRestart` is in old docs but not found in code (omitted).
- `examples/config-gcs.json` uses `credentialsFile`, which the GCS driver ignores (driver reads `keyfile`/`credentials`).
- DynamoDB with GCS/Azure: code comment says S3 only.
- `lint` block without `enable` may panic (no nil check); documented `enable` as required.
- API key `scopes` stored but no enforcement found; documented as metadata.
- `detectionPriority` allowed values; `zxp` default read timeout 30s.
- `profile` listed as extension in old docs/releases page but is a build tag, not a config key (fix `install/releases.mdx`).

**Fix after batch 1:** `install/releases` extension list corrected (`profile` is a build label, no config key; `mgmt` key in shipped config is redundant).

**Batch 3 done (2026-10-20):** `operations/*` (12, of which backup-restore, troubleshooting, production-checklist are new), `use/*` (6, with `zli-reference` and `search-graphql-examples` added to nav), `clients/{containerd,compatibility}`, `guides/*` (3). Remaining stubs: `changelog`, `community/about`, `api-reference/*`, `developers/*`.

Corrections to old docs (verified in code): retention policies without `repositories` match nothing; subpaths don't inherit `gc`; retention only runs inside GC; first matching `keepTags` entry wins; sync `tags.excludeRegex` (not `tags.tags.*`); cluster members must include self, `hashKey` exactly 16 chars, proxied requests rejected with 508; GraphQL: wrong/misspelled query names, `offset` counts results not pages, default sorts, request limits; zli: `config` subcommands, `repo list`, per-command `--sort-by`; UI is the `ui` extension needing `search`; 17 real `zot_*` metrics; zxp exposes Prometheus metrics; zb undocumented flags, `-o json` no-op; provenance workflow rewritten (old pinned zot 2.0.0-rc6/cosign 2.1.1 and removed env var).

Open questions for maintainers (batch 3):
- Which release introduced streaming sync (`stream`, `maxConcurrentStreams`) and `sessionDriver`?
- UI with local-storage scale-out: kept old "not supported" claim, unverified.
- `zb -o json` appears to do nothing; zb image tag (`latest` vs `zb-linux-amd64`)?
- Should `/livez`, `/readyz`, `/startupz` stay unauthenticated?
- zli bugs: `zli search subject --help` prints stray `" +`; `cve affected --repo` help text wrong.
- Web UI screenshots show old logo and `zothub.io`; need retaking.
- kind scripts in the zot repo use image name `zot-minimal-linux-amd64` vs docs `ghcr.io/project-zot/zot-minimal`.
- Does zot test still need `COSIGN_EXPERIMENTAL=1` with cosign 3?
- GraphQL `LastPullTimestamp` zero value (`0001-…` vs `1970-…`).
- Backup/restore: live-copy consistency of storage/`meta.db`, skipping `.uploads`, restoring remote-dedupe bucket without cache are untested (page says so).
- `cosigned` replacement (policy-controller) in CI/CD tutorial unverified offline.
- Compatibility matrix: containerd and kubelet rows are "documented" only.

**Batch 4 done (2026-10-20):** `changelog` (28 releases, dated from git tags), `developers/*`, `community/about`, `api-reference/*` + `api-reference/openapi.yaml` (converted from Swagger 2.0; 25 generated endpoint pages). All content pages migrated; no stubs remain.

Corrections to old docs (verified in code): minimal binary is `zot-linux-amd64-minimal`; MetaDB file is `meta.db`; extension build tags use `//go:build` + `_disabled.go`; `/oras/artifacts/v1/...` route does not exist; upload-start route needs trailing slash; login is `GET /zot/auth/login`; API key revoke path is `/zot/auth/apikey`; SECURITY.md says use private GitHub advisories (old docs listed an email and a 45-day window).

Routes in code but absent from swagger: `/v2/_zot/ext/search`, `/zot/auth/login`, `/zot/auth/callback/{provider}`, `/zot/auth/token`, pprof, metrics, `/livez` `/readyz` `/startupz`, debug-only swagger/playground. Swagger annotation bugs upstream: trailing slashes, `n`/`last` marked required, blob GET typed as manifest.

Open questions (batch 4): `SECURITY.md` supported versions (lists only 2.0.x); is `security@zotregistry.dev` monitored; CNCF Sandbox status unverified in repo; adopters list is only Cisco; v2.0.0 changelog date equals rc8 tag date; no v2.1.1 section in source; GraphQL error response shape unverified.

**Phase 5 done (2026-10-20), repo-side:** redirect map (`scripts/redirect-map.json`, `build-redirects.py`) applied to `docs.json` (41 redirects) and `landing/` (42 redirect pages + `404.html` fallback tested for versioned/unversioned/.html/unknown paths); `v2.1.x` snapshot via `scripts/snapshot-version.py` (versioned OpenAPI uses `directory` so endpoint URLs don't collide); SEO metatags + OG image; CI workflows (`docs-ci`, `spellcheck` advisory/untested, `landing-pages`); `README.md`; `drafts/CUTOVER.md` runbook. Contrast checked (all pairs >= 6.29:1). Not done: domain/DNS/Mintlify account/apex swap (need account owner), retaken UI screenshots, mobile/dark visual checks.
