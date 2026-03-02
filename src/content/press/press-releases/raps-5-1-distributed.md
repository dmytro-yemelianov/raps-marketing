---
title: "RAPS 5.1: Distributed Orchestration with Redis, Serverless, and Webhook Gateway"
description: "RAPS adds distribution layer: Redis-backed cache and job queue, Fly.io serverless dispatch, Cloudflare Workers webhook gateway, and Docker Compose deployment."
type: "release"
publishDate: 2026-03-02
status: "draft"
---

# FOR IMMEDIATE RELEASE

## RAPS 5.1: Distributed Orchestration with Redis, Serverless, and Webhook Gateway

*Open-source APS CLI extends swarm orchestration with distributed caching, serverless model translation, and edge webhook processing*

---

**Version Information**
- **Current Version**: 5.1.0
- **Previous Version**: 5.0.0 (Swarm Orchestration Kernel)
- **APS API Coverage**: Authentication v2, Data Management v1, Model Derivative v2, OSS v2, Design Automation v3, Construction Cloud v1, Webhooks, Account Admin
- **Architecture**: 10 Rust workspace crates + Cloudflare Worker
- **License**: Apache-2.0

---

Building on the swarm orchestration kernel introduced in v5.0, RAPS 5.1 adds a complete distribution layer. Teams can now run translation workloads across distributed Redis-backed workers, dispatch jobs to Fly.io serverless machines that scale to zero, and receive APS webhook events through a Cloudflare Workers gateway with Durable Objects persistence.

### What's New

#### Redis-Backed Cache and Job Queue

RAPS introduces a `CacheBackend` trait with pluggable implementations. The default `MemoryBackend` works for single-process deployments, while the feature-gated `RedisBackend` enables distributed caching with deadpool connection pooling.

The job queue uses Redis Streams with three priority levels (critical, normal, background) and a dead-letter queue for failed jobs. Workers coordinate via consumer groups for exactly-once processing.

```bash
raps swarm worker start --redis-url redis://localhost:6379 --concurrency 4
```

#### Fly.io Serverless Dispatch

The new `--serverless` flag on `raps translate start` dispatches jobs to Fly.io ephemeral machines instead of local workers. Machines scale to zero when idle, so you only pay for actual compute time.

```bash
raps translate start "urn:adsk..." --serverless --wait --notify
```

A new `raps job` command provides status, list, and cancel operations for managing serverless machine jobs.

#### Cloudflare Workers Webhook Gateway

A purpose-built Cloudflare Worker receives APS webhook events at the edge, validates HMAC-SHA256 signatures, and stores events in a Durable Object with automatic backpressure (1000-event backlog). Events can be drained via authenticated API or relayed to a callback URL in real-time.

```bash
raps webhook serve --serverless --webhook-secret $SECRET
raps webhook drain --gateway-url https://gateway.workers.dev --limit 50
```

#### Docker Compose Deployment

A production-ready Docker Compose stack deploys the full orchestration platform: Redis 7 with AOF persistence, 4 worker replicas, reverse proxy, webhook ingress, and monitoring dashboard.

#### CI/CD Pipeline Examples

Ready-to-use GitHub Actions and GitLab CI pipeline configurations for serverless model translation, complete with authentication, dispatch, and verification stages.

### Availability

RAPS 5.1.0 is available now:

```bash
curl -fsSL https://rapscli.xyz/install.sh | bash
```

Or via npm/pip:

```bash
npm install -g @nicolo-studio/raps-cli
pip install raps-cli
```

### About RAPS

RAPS is an open-source command-line interface for Autodesk Platform Services (APS), providing 100+ commands across all major APS APIs. Built in Rust for performance and reliability, RAPS supports interactive shell, MCP server, Docker, GitHub Actions, GitLab CI, and Python binding modes. Licensed under Apache-2.0.

GitHub: https://github.com/dmytro-yemelianov/raps
Website: https://rapscli.xyz
