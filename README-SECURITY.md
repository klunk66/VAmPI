# VAmPI — DevSecOps Security Pipeline (SAST + DAST)

This repository includes a simple, fully free DevSecOps workflow that runs:

- **SAST** (static application security testing) on the source code.
- **DAST** (dynamic application security testing) against the running API.

## Purpose

The goal of the security pipeline is to automatically detect vulnerabilities in both the application code and its runtime behavior. This is accomplished through:

1. **Static Analysis (SAST)** — Identifies coding issues, insecure patterns, and potential vulnerabilities before runtime by analyzing the source code directly.

2. **Dynamic Analysis (DAST)** — Tests the running API for security misconfigurations, authentication flaws, and behavioral vulnerabilities that only appear during execution.

This approach provides defense-in-depth by catching issues at multiple stages of the software development lifecycle, from code commit through deployment.

## Tools

- **SAST**: Bandit (Python security linter)
- **DAST**: OWASP ZAP Baseline Scan

## How the pipeline works

The GitHub Actions workflow runs on **push**, **pull request**, and **manual dispatch**.

### 1) SAST — Bandit

- Installs dependencies.
- Scans the repository with Bandit.
- Generates a JSON report.

### 2) DAST — OWASP ZAP Baseline

- Starts the API.
- Initializes the database by calling `/createdb`.
- Runs ZAP Baseline against the live API.
- Generates an HTML report.

## Reports (Artifacts)

Each workflow run uploads the following artifacts:

- **bandit-report.json** (SAST)
- **zap_report.html** (DAST)

## Workflow file

The workflow definition is located at:

- .github/workflows/security.yml