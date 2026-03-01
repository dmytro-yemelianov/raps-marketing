---
title: "RAPS 4.16: Pipeline v2 Engine and Official CI/CD Integrations"
description: "Advanced pipeline automation with retry, parallelism, conditionals, plus official GitHub Actions and GitLab CI templates"
type: "release"
publishDate: 2026-03-01
status: "draft"
---

# FOR IMMEDIATE RELEASE

## RAPS 4.16: Pipeline v2 Engine and Official CI/CD Integrations

*Advanced pipeline automation with retry, parallelism, conditionals, plus official GitHub Actions and GitLab CI templates*

---

**Release Information**
- **Version**: 4.16.0
- **Release Date**: March 1, 2026
- **License**: Apache-2.0 (open source)
- **Previous Version**: 4.15.0 (ASVS security hardening, npm fix)

---

RAPS 4.16.0 introduces the Pipeline v2 engine and official CI/CD integrations for GitHub Actions and GitLab CI. This release transforms RAPS from a command-line tool into a full pipeline automation platform for Autodesk Platform Services workflows.

### Pipeline v2 Engine

The Pipeline v2 engine is a ground-up rewrite of the RAPS pipeline system, designed for production-grade APS workflow automation. Pipelines are defined in YAML and support the following capabilities:

- **Retry Policies**: Configure per-step retry with max attempts, backoff strategy, and retryable error conditions. Failed steps are automatically retried without restarting the entire pipeline.
- **Timeouts**: Set per-step and per-pipeline timeouts to prevent runaway jobs and enforce SLAs.
- **If/Unless Conditionals**: Execute steps conditionally based on expressions evaluated at runtime. Skip steps that don't apply to the current context.
- **Parallel Steps**: Run independent steps concurrently with configurable concurrency limits. Upload multiple files, start multiple translations, or process multiple projects simultaneously.
- **For-Each Loops**: Iterate over lists of items (buckets, files, projects) and execute a step template for each. Combine with parallelism for high-throughput batch operations.
- **Expression Evaluation**: A built-in expression evaluator supports variable interpolation, step output references, environment variables, and conditional logic within pipeline definitions.

#### Example: Pipeline v2 YAML

```yaml
name: translate-and-export
version: 2

env:
  BUCKET: hospital-project-2026
  OUTPUT_FORMAT: svf2

steps:
  - name: upload-models
    command: object upload ${BUCKET} ${file}
    for-each:
      - model-arch.rvt
      - model-struct.rvt
      - model-mep.rvt
    parallel: 3
    retry:
      max-attempts: 3
      backoff: exponential
    timeout: 10m

  - name: translate-all
    command: translate start ${steps.upload-models.outputs[*].urn} --format ${OUTPUT_FORMAT} --wait
    parallel: 3
    timeout: 30m
    retry:
      max-attempts: 2
      backoff: fixed

  - name: export-properties
    command: translate properties ${steps.translate-all.outputs[*].urn} --format csv --output ./exports/
    if: steps.translate-all.status == 'success'
    timeout: 15m

  - name: notify-team
    command: webhook send ${WEBHOOK_URL} --payload '{"status": "complete", "files": ${steps.upload-models.outputs | length}}'
    unless: steps.translate-all.status == 'failed'
```

Run a pipeline with:

```bash
raps pipeline run translate-and-export.yaml
```

Validate pipeline syntax before running:

```bash
raps pipeline validate translate-and-export.yaml
```

### GitHub Actions Integration

RAPS now provides four official composite actions for GitHub Actions, published as `raps-actions/setup`, `raps-actions/pipeline`, `raps-actions/upload`, and `raps-actions/translate`. These actions handle authentication, caching, and error reporting out of the box.

#### Available Actions

| Action | Description |
|--------|-------------|
| `raps-actions/setup` | Install RAPS CLI and configure authentication |
| `raps-actions/pipeline` | Run a RAPS pipeline YAML file |
| `raps-actions/upload` | Upload files to an OSS bucket |
| `raps-actions/translate` | Start and monitor a Model Derivative translation |

#### Example: GitHub Actions Workflow

```yaml
name: APS Model Pipeline
on:
  push:
    paths: ['models/**']

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: raps-actions/setup@v1
        with:
          version: '4.16.0'
          client-id: ${{ secrets.APS_CLIENT_ID }}
          client-secret: ${{ secrets.APS_CLIENT_SECRET }}

      - uses: raps-actions/upload@v1
        id: upload
        with:
          bucket: my-project-bucket
          file: models/building.rvt

      - uses: raps-actions/translate@v1
        with:
          urn: ${{ steps.upload.outputs.urn }}
          format: svf2
          wait: true

      - uses: raps-actions/pipeline@v1
        with:
          file: pipelines/post-translate.yaml
```

### GitLab CI Integration

RAPS provides four include templates for GitLab CI/CD, available from the RAPS repository. These templates define reusable job configurations that can be included in any `.gitlab-ci.yml` file.

#### Available Templates

| Template | Description |
|----------|-------------|
| `.raps-setup` | Install RAPS CLI and configure authentication |
| `.raps-pipeline` | Run a RAPS pipeline YAML file |
| `.raps-upload` | Upload files to an OSS bucket |
| `.raps-translate` | Start and monitor a Model Derivative translation |

#### Example: GitLab CI Configuration

```yaml
include:
  - project: 'raps/raps-ci-templates'
    ref: v1.0.0
    file:
      - '/templates/.raps-setup.yml'
      - '/templates/.raps-pipeline.yml'
      - '/templates/.raps-upload.yml'
      - '/templates/.raps-translate.yml'

variables:
  APS_CLIENT_ID: $APS_CLIENT_ID
  APS_CLIENT_SECRET: $APS_CLIENT_SECRET
  RAPS_VERSION: "4.16.0"

stages:
  - setup
  - upload
  - translate
  - pipeline

install-raps:
  extends: .raps-setup
  stage: setup

upload-model:
  extends: .raps-upload
  stage: upload
  variables:
    BUCKET: my-project-bucket
    FILE: models/building.rvt

translate-model:
  extends: .raps-translate
  stage: translate
  variables:
    FORMAT: svf2
    WAIT: "true"

run-pipeline:
  extends: .raps-pipeline
  stage: pipeline
  variables:
    PIPELINE_FILE: pipelines/post-translate.yaml
```

### ASVS L2 Security Improvements

RAPS 4.15.0 (released February 28, 2026) introduced comprehensive security hardening aligned with OWASP Application Security Verification Standard (ASVS) Level 2. RAPS 4.16.0 carries forward these improvements:

- **82% ASVS L2 Compliance**: Verified against 286 ASVS controls with 234 passing.
- **Enhanced Token Handling**: Tokens are encrypted at rest, automatically rotated, and never logged or exposed in error messages.
- **Input Validation**: All user-supplied inputs (bucket names, URNs, file paths) are validated against strict patterns before API calls.
- **Secure Credential Storage**: Credentials are stored in OS-native keychains (macOS Keychain, Windows Credential Manager, Linux Secret Service) when available.
- **Audit Logging**: All authentication events, API calls, and pipeline executions are logged with timestamps and correlation IDs for forensic review.

### How to Get Started

#### Install RAPS

```bash
# Quick install (Linux/macOS)
curl -fsSL https://raw.githubusercontent.com/dmytro-yemelianov/raps/main/install.sh | bash

# npm
npm install -g @dmytro-yemelianov/raps-cli

# pip
pip install raps

# Homebrew
brew install dmytro-yemelianov/tap/raps

# Cargo
cargo install raps
```

#### Configure Authentication

```bash
raps config set client_id "your_client_id"
raps config set client_secret "your_client_secret"
raps auth test
```

#### Run Your First Pipeline

```bash
# Generate a sample pipeline
raps pipeline sample > my-pipeline.yaml

# Validate it
raps pipeline validate my-pipeline.yaml

# Run it
raps pipeline run my-pipeline.yaml
```

#### Set Up CI/CD

For GitHub Actions, add the workflow YAML to `.github/workflows/` in your repository. For GitLab CI, add the include directives to your `.gitlab-ci.yml`. Both integrations use environment secrets for APS credentials -- no credentials are committed to source control.

### About RAPS

RAPS is an open-source project developed by Dmytro Yemelianov. It is free to use under the Apache-2.0 license.

- **Website**: [rapscli.xyz](https://rapscli.xyz)
- **Source Code**: [github.com/dmytro-yemelianov/raps](https://github.com/dmytro-yemelianov/raps)
- **GitHub Actions**: [github.com/raps-actions](https://github.com/raps-actions)
- **Author**: Dmytro Yemelianov (dmytroyemelianov@icloud.com)

---

*RAPS is an independent open-source project. Autodesk, APS, Forge, and related marks are trademarks of Autodesk, Inc.*
