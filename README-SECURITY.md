# VAmPI — DevSecOps Security Pipeline (SAST + DAST)

This repository includes a simple, fully free DevSecOps workflow that runs:

- **SAST** (static application security testing) on the source code.
- **DAST** (dynamic application security testing) against the running API.

## Tools (Free)

- **SAST**: Bandit (Python security linter)
- **DAST**: OWASP ZAP Baseline Scan

## How the pipeline works

The GitHub Actions workflow runs on **push**, **pull request**, and **manual dispatch**.

### 1) SAST — Bandit

- Installs dependencies.
- Scans the repository with Bandit.
- Generates a JSON report.
- Continues even if issues are found (this project is intentionally vulnerable).

### 2) DAST — OWASP ZAP Baseline

- Starts the API.
- Initializes the database by calling `/createdb`.
- Runs ZAP Baseline against the live API.
- Generates an HTML report.
- Continues even if issues are found.

## Reports (Artifacts)

Each workflow run uploads the following artifacts:

- **bandit-report.json** (SAST)
- **zap_report.html** (DAST)

## Workflow file

The workflow definition is located at:

- .github/workflows/security.yml

## Optional local execution

You can run the same tools locally if needed.

### 1) Install dependencies

```
pip install -r requirements.txt
pip install bandit
```

### 2) Start the API

```
python app.py
```

### 3) Initialize the database

```
curl http://127.0.0.1:5000/createdb
```

### 4) Run SAST (Bandit)

```
bandit -r . -x ./.git,./.venv,./venv -ll -f json -o bandit-report.json
```

### 5) Run DAST (ZAP Baseline)

```
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://host.docker.internal:5000 -I -r zap_report.html
```

## Notes

- VAmPI is intentionally vulnerable, so findings are expected.
- The workflow is configured to produce reports without failing the pipeline.
