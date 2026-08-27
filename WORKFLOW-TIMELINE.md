# GitHub Consolidation — Migration Stage Execution Matrix
**Repository:** [hcsc-devops/gh-migration](https://github.com/hcsc-devops/gh-migration)
**Primary actor:** Andres Garcia · **Scope:** all org-to-org runbook stages
**Generated:** 2026-08-12

## Stage and Run Summary

Each row maps a migration stage to its automation and lists the latest successful and failed/cancelled run. **Author** is the GitHub Actions actor that started the run. Run details are retained only for runs authored by Andres Garcia; other stage and workflow information remains listed.

> Durations shown as **hh:mm** (run `updated_at − created_at`).
> Links open directly to the GitHub Actions run page.

| # | Stage | Script / CLI | Workflow | Latest Success | Success Author | Dur | Latest Failure / Cancel | Failure Author | Dur | Notes |
|---|-------|-------------|----------|----------------|----------------|-----|-------------------------|----------------|-----|-------|
| 1 | **Org migration (GEI)** | `gh gei migrate-org` | [migrate-org.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/migrate-org.yml) | [#30 — 2026-08-11](https://github.com/hcsc-devops/gh-migration/actions/runs/31492144361) | Andres Garcia | 9m | [#27 cancelled — 2026-07-29](https://github.com/hcsc-devops/gh-migration/actions/runs/30468978644) | Andres Garcia | 6h | Runs #26 and #27 hit the 6h GitHub-hosted runner ceiling; run #28 (24h) hit `timeout-minutes: 1440` on a self-hosted runner. |
| 2 | **Org-level asset replay** (rulesets, variables, custom properties) | `gh api` via `export-org-assets` / `apply-org-assets` jobs | [migrate-org.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/migrate-org.yml) (inline jobs) | Same as #30 above | Andres Garcia | — | — | — | — | Asset replay is embedded in `migrate-org.yml`; controlled by `migrate_rulesets`, `migrate_variables`, `migrate_custom_properties` inputs. |
| 3 | **Repo/env secrets migration** (Python/PyNaCl) | [`migrate-secrets-direct.py`](org-migration/secrets/migrate-secrets-direct.py) — deploy / trigger / poll / cleanup | [migrate-org-configs.yml](.github/workflows/migrate-org-configs.yml) | — | — | — | — | — | — | Andres Garcia's direct source-runner workflow resolves repository, environment, and organization secrets, encrypts them with PyNaCl, and writes encrypted values to the destination GitHub API. See the [direct secret migration documentation](org-migration/docs/migrate-secrets-direct.md). It is disabled by default and enabled with `migrate_secrets_invasive`. |
| 4 | **Packages migration** (container + ecosystem) | `python org-migration/main.py --config config.yml packages` | None — manual CLI only | — | — | — | — | — | — | **No dedicated workflow.** Covers `ghcr.io`, npm, maven, gradle, nuget, and rubygems. |
| 5 | **Team creation** | `create-teams.sh` / `create-teams.yml` | [create-teams.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/create-teams.yml) | — | — | — | — | — | — | App-ID role-team model. GEI org migration carries teams from source; use this only to reconcile missing role teams post-migration. |
| 6 | **Team assignment to repos** | `assign-teams.yml` | [assign-teams.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/assign-teams.yml) | [#171 — 2026-07-21](https://github.com/hcsc-devops/gh-migration/actions/runs/29844919152) | Andres Garcia | 1m | [#170 failure — 2026-07-21](https://github.com/hcsc-devops/gh-migration/actions/runs/29844795217) | Andres Garcia | 1m | Assigns teams to repositories per the App-ID model. |
| 7 | **Team assignment report** | — | [team-assignment-report.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/team-assignment-report.yml) | — | — | — | — | — | — | Verification report for team assignment completeness across the destination organization. |
| 8 | **Set migrated repos internal** | `gh api -X PATCH /repos/…` | [migrate-org.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/migrate-org.yml) (inline job) | — | — | — | — | — | — | Done inline by `migrate-org.yml` via `set_visibility_internal` for the org-to-org path. |
| 9 | **Mannequin reclaim** | `gh gei generate-mannequin-csv` + `gh gei reclaim-mannequin` | [reclaim-mannequins.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/reclaim-mannequins.yml) | — | — | — | — | — | — | Maps mannequin placeholder accounts to real HCSC users. |
| 10 | **App-ID / AD-role repo config** | `configure-repos-by-appid.sh` | [configure-repos-by-appid.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/configure-repos-by-appid.yml) | — | — | — | — | — | — | Applies repository settings driven by App-ID and AD-role mappings. |
| 11 | **Repo-level rulesets / variables / webhooks** (AI-9) | `gh api` REST loops | None — manual CLI only | — | — | — | — | — | — | **No dedicated workflow.** Tracked in DEVOPS-14835 (variables) and DEVOPS-14836 (webhooks). |
| 12 | **GHAS enablement** (AI-8) | `gh api -X PATCH /repos/…` | None — manual CLI only | — | — | — | — | — | — | **No dedicated workflow.** Bulk-enable per repository after cutover; see DEVOPS-14669. |
| 13 | **Self-hosted runner duplication** (AI-5) | `./config.sh --url … --runnergroup … --labels … --token` | None — manual only | — | — | — | — | — | — | **No workflow.** Seven public runners are planned for duplication on HCSC Enterprise. |
| 14 | **Org webhook re-activation** (AI-7) | `gh api -X PATCH orgs/…/hooks/<id>` | None — manual CLI only | — | — | — | — | — | — | GEI migrates webhook configuration but leaves hooks inactive without a secret. |
| 15 | **Post-migration integrity checks** | `check_repo()` bash function (see runbook) | None — manual CLI only | — | — | — | — | — | — | Compare commit, branch, and tag counts per repository before sign-off. |
| 16 | **IIQ / SCIM team membership** (AI-1) | IIQ/SCIM → Active Directory | None — Identity team owns | — | — | — | — | — | — | GEI carries teams and repository access, **not membership**. Provisioned through IIQ SCIM sync. |

## Run Details

### Mannequin Reclaim

| Latest Success | Author | Duration | Link | Latest Failure | Author | Duration | Link |
|----------------|--------|----------|------|----------------|--------|----------|------|
| — | — | — | — | — | — | — | — |

### Teams

| Workflow | Latest Success | Author | Dur | Latest Failure | Author | Dur |
|----------|----------------|--------|-----|----------------|--------|-----|
| [create-teams.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/create-teams.yml) | — | — | — | — | — | — |
| [assign-teams.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/assign-teams.yml) | [#171 — 2026-07-21](https://github.com/hcsc-devops/gh-migration/actions/runs/29844919152) | Andres Garcia | 1m | [#170 — 2026-07-21](https://github.com/hcsc-devops/gh-migration/actions/runs/29844795217) | Andres Garcia | 1m |
| [team-assignment-report.yml](https://github.com/hcsc-devops/gh-migration/actions/workflows/team-assignment-report.yml) | — | — | — | — | — | — |

## Stages Without a Dedicated Workflow

These stages are documented in the runbook with CLI commands but have no dedicated workflow file in `hcsc-devops/gh-migration`. They must be executed manually or tracked as separate automation tasks.

| Stage | Runbook section | Command entry-point | Jira task | Status |
|-------|----------------|---------------------|-----------|--------|
| Repo/env secrets migration | Secrets & packages / AI-3 | [`migrate-secrets-direct.py`](org-migration/secrets/migrate-secrets-direct.py) | — | Direct source-runner workflow is available in `migrate-org-configs.yml`; see the [detailed documentation](org-migration/docs/migrate-secrets-direct.md); disabled by default until the official migration window. |
| Packages migration | Secrets & packages / AI-4 | `python org-migration/main.py … packages` | — | Manual CLI only |
| Repo-level rulesets replay | AI-9 | `gh api` REST loop | — | **To build** |
| Repo-level variables replay | AI-9 | `gh api` REST loop | DEVOPS-14835 | **To build** |
| Repo-level webhook recreation | AI-7 / AI-9 | `gh api -X POST repos/…/hooks` | DEVOPS-14836 | **To build** |
| GHAS bulk-enable | GHAS / AI-8 | `gh api -X PATCH /repos/…` | DEVOPS-14669 | **TBD** |
| Self-hosted runner duplication | Runners strategy / AI-5 | `./config.sh --url … --token …` | DEVOPS-14832 | In progress |
| Org webhook re-activation | AI-7 | `gh api -X PATCH orgs/…/hooks/<id>` | — | Manual at cutover |
| Post-migration integrity check | Post-migration integrity checks | `check_repo()` bash function | — | Manual at cutover |
| IIQ / SCIM team membership | AI-1 / GHAS / IIQ section | IIQ SCIM group sync | — | Identity team |
| Copilot Business provisioning | GHAS / Copilot section | `gh api -X POST …/copilot/billing/…` | — | TBD |
| Audit log streaming to Splunk | Post-cutover / Hypercare | Splunk index config | — | Verify before decommission |