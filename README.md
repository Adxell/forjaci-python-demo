# forjaci Python demo

A small HTTP service (Python standard library only) built, tested, signed and scanned by [forjaci](https://github.com/Adxell/forjaci).

| Endpoint | Response |
|---|---|
| `GET /?name=ada` | `{"message": "hello, ada", "version": "dev"}` |
| `GET /healthz` | `{"status": "ok"}` |

## Run it locally

```sh
python -m app.server            # http://localhost:8080
python -m pytest -q             # after: pip install -r requirements-dev.txt
docker build -t python-demo . && docker run --rm -p 8080:8080 python-demo
```

## Pipeline (`.forjaci.yml`)

1. **test**: installs the hash-pinned test dependencies from PyPI (the only hosts the step can reach) and runs pytest.
2. **image**: builds the Dockerfile with no network, pushes it to the forjaci registry, signs it by digest and attaches an SPDX SBOM. Only the main branch is signed.
3. **scan**: Grype checks the SBOM and fails the pipeline on a critical vulnerability.
4. **deploy** (commented out): enroll a deployment agent named `prod`, then uncomment the step to run the signed image with a health check on `/healthz`.

In forjaci: **Projects → New project**, paste this repository's URL (no token needed for a public repository), then **Fetch and run**.
