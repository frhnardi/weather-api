# CLAUDE.md — weather-api

## What this repo is

A trivial Python (FastAPI) HTTP service instantiated from
`platform-golden-path/templates/service-python`. It is the **second** compliant
service on the platform (after the Go `sample-service`) — its job is to prove the
paved road is reusable across languages and across more than one service.

## Constraints

- Keep it trivial: `/healthz` plus one demo endpoint (`/weather`). Business logic
  dilutes the point, which is the paved road around the code.
- CI stays ~5 lines calling `frhnardi/platform-golden-path/.github/workflows/golden-path.yml`
  with `service-name: weather-api`, `language: python`. If more YAML creeps in
  here, that is the golden path leaking complexity — fix it upstream.
- No Kubernetes manifests here. Deployment lives in
  `platform-gitops/apps/weather-api/` and is updated by the promotion PR (digest).
- The service must satisfy the platform's baseline policies via its runtime:
  distroless nonroot (UID 65532), read-only rootfs, no capabilities.

## Onboarding checklist (one-time, done by a human)

1. Create the GitHub repo `weather-api` and push this code.
2. In `platform-infra`, add `weather-api` to `federated_repositories` (purpose
   `publisher`) and `terraform apply` — grants AcrPush + a federated credential.
3. Set repo variables `AZURE_CLIENT_ID` (from `terraform output github_client_ids`),
   `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `ACR_NAME`. Org secrets
   `GITOPS_APP_ID` / `GITOPS_APP_PRIVATE_KEY` are inherited automatically.
4. `apps/weather-api/` already exists in `platform-gitops`; the first pipeline run
   opens the digest-bump PR against it.
