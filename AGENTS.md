# Documentation project instructions

## About this project

- Documentation site for **zot**, a vendor-neutral, OCI-native container image registry (CNCF project), built on [Mintlify](https://mintlify.com)
- Pages are MDX files with YAML frontmatter; configuration lives in `docs.json`
- Content is migrated from the MkDocs site in `../project-zot.github.io/docs/`; see `drafts/MIGRATION.md` for the page map
- Source of truth for behavior is the zot repo (`../zot`): `swagger/swagger.yaml` for the API, `examples/config-*.json` for configuration. Do not invent options; verify against these.
- Use the Mintlify MCP server, `https://mcp.mintlify.com`, to edit content and settings via MCP
- Use the Mintlify docs MCP server, `https://www.mintlify.com/docs/mcp`, to query information about using Mintlify via MCP

## Terminology

- **zot**: lowercase, always, even at the start of a sentence. Binary and project name.
- **zli**: command-line client. **zb**: benchmarking tool. Code-format when naming the executable.
- **OCI**: Open Container Initiative. Write "OCI Distribution Specification" first, then "dist-spec".
- Use "registry" for a zot server, "repository" for a named collection of images (`myrepo/app`), "tag" and "digest" as in the OCI spec.
- **MetaDB**: the zot metadata database. Use "extension" (not "plugin") for optional zot features.
- Use "full" and "minimal" for the two binary flavors; "zot-linux-amd64" style names are code-formatted.
- cosign, notation, skopeo, oras, regclient, crane, helm, containerd, cri-o: lowercase tool names, code-formatted when used as commands.
- Config keys are code-formatted exactly as in the JSON schema (`accessControl`, `gc`, `dedupe`).
- Seed list of project terms: `../project-zot.github.io/.wordlist.txt`.

## Style preferences

- Use active voice and second person ("you")
- Keep sentences concise: one idea per sentence
- Use sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, config keys, and code references
- Use Mintlify components instead of MkDocs syntax: `<Note>`, `<Tip>`, `<Warning>`, `<Steps>`, `<Tabs>`, `<CodeGroup>`, `<Accordion>`, `<ParamField>`
- Config snippets are JSON by default; add YAML tabs only where zot supports and the example exists
- Every runnable example must work against the current release; prefer `localhost:5000` as the registry address
- Link internally with absolute paths (`/security/authentication`), never `.md` relative links
- Every page has `title` and `description` frontmatter

## Content boundaries

- Document released, supported behavior. Note the version for features added in a release (for example, "Added in v2.1.20").
- Do not document internal-only test scripts or CI details beyond what contributors need.
- Don't duplicate reference content: link to the config reference or the API reference instead of restating it.
- Security issues are reported privately; never publish exploit details.
