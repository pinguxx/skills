---
name: release-hygiene
description: Pre-release and repository cleanup checklist covering stale version sweeps, changelog and docs sync, dead file pruning, and full verification gates before tagging or publishing.
---

# Release & Repo Hygiene

Run this checklist before cutting a release or cleaning up a repository.

## 1. Version Sync Sweep
After bumping the version in the primary manifest (`package.json`, `Cargo.toml`, `pyproject.toml`, etc.), sweep the entire repository for stale references to the previous version:

```bash
git grep -n "<PREV_VERSION>" -- ':!CHANGELOG.md' ':!package-lock.json' ':!pnpm-lock.yaml' ':!yarn.lock'
```

Update every remaining live reference across READMEs, HTML pages, badges, API/MCP manifests, and starter templates. Leave historical changelog entries untouched.

## 2. Docs & Dead File Audit
- Check for orphaned scripts, unused demos, duplicate docs, or outdated tool/API names.
- Slim down bloated docs: remove marketing filler, duplicate tables, and dead examples. Run the `unslop` skill on public READMEs and release notes.
- Confirm no secrets, tokens, `.env` files, or private drafts are staged or tracked in git.

## 3. Full Verification Gates
Before tagging or pushing a release, run all available project gates and confirm zero failures:
1. Unit, integration, and coverage tests.
2. Strict typecheck and linter.
3. Production build and bundle/size budget check.
4. Browser E2E and accessibility checks (if present).
5. Clean `git status` and verified `CHANGELOG.md` entry for the new version.
