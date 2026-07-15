# weather-api

A deliberately boring Python (FastAPI) service, the **second** service instantiated
from `platform-golden-path/templates/service-python` — proof the paved road is
reusable across languages (Go `sample-service`, Python here).

Push code → lint/test → Semgrep → Trivy → distroless image → SBOM → keyless
cosign signature → SLSA provenance → GitOps promotion PR → Kyverno-admitted,
running in AKS. No security knowledge required of the developer.

## Endpoints

| Method | Path | |
|---|---|---|
| GET | `/healthz` | liveness/readiness probe |
| GET | `/weather?city=` | deterministic dummy forecast (defaults to `jakarta`) |

## Local

```bash
pip install -r requirements.txt ruff pytest httpx
ruff check . && pytest        # what CI runs
python main.py                # serve on :8080
curl localhost:8080/weather?city=bandung
```

## How it ships

CI is ~5 lines that call the reusable golden-path workflow (`.github/workflows/ci.yml`).
Everything else — scanning, signing, attestation, the digest-bump PR against
`platform-gitops` — happens on the paved road. Deployment manifests live in
`platform-gitops/apps/weather-api/`, never here.
# trigger ci
