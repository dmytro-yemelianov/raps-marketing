---
title: "RAPS 5.0: Multi-Agent Swarm Orchestration for Autodesk Platform Services"
description: "Major release introduces fault-tolerant API coordination with circuit breakers, rate budgets, checkpointing, and real-time TUI dashboard"
type: "release"
publishDate: 2026-03-01
status: "draft"
---

# FOR IMMEDIATE RELEASE

## RAPS 5.0: Multi-Agent Swarm Orchestration for Autodesk Platform Services

*Rust-based CLI tool adds production-grade swarm coordination kernel with circuit breakers, rate budgets, and real-time observability*

---

**Version Information**
- **Current Version**: 5.0.0
- **Previous Major**: 4.18.0
- **Architecture**: 10 Rust workspace crates + swarm orchestration kernel
- **License**: Apache-2.0 (open source)
- **Security**: ASVS L2 compliance at 100% (34/34 requirements met)

---

RAPS (Rust-based APS CLI) has reached version 5.0.0, its first major version bump since 4.0. This release introduces a swarm orchestration kernel that coordinates multiple API agents with production-grade resilience patterns.

### What's New in v5.0

**Swarm Orchestration Kernel**

Large BIM projects often require coordinating dozens of concurrent API calls — uploads, translations, issue syncs, and asset management. RAPS v5.0 provides the infrastructure to handle this reliably:

- **Circuit Breaker**: Automatically stops cascading failures when APS endpoints become degraded
- **Rate Budget**: Distributes API rate limits across concurrent agents to prevent 429 errors
- **Retry Policy**: Configurable exponential backoff with jitter for transient failures
- **Region Routing**: Directs requests to the optimal APS data center
- **Response Cache**: Deduplicates identical API calls across agents

**Observability**

- **API Metrics Collector**: Per-endpoint latency, error rate, and throughput tracking
- **Structured Audit Logger**: JSON audit trail for all swarm operations
- **Checkpoint Store**: Durable progress checkpointing with automatic resume for long-running operations

**TUI Swarm Dashboard (F8)**

A new tab in the k9s-style terminal dashboard provides real-time visibility into swarm state — circuit breaker states, rate budget utilization, cache hit rates, API metrics, and active checkpoints.

**Compound MCP Tools**

Five new MCP tools for AI assistants that combine multiple API operations:
- `bulk_upload` / `bulk_download` — batch file operations with progress
- `search_and_download` — find and retrieve objects in one step
- `upload_and_translate` / `translate_and_download` — end-to-end model conversion

**HTTP/2 Multiplexing**

All HTTP connections now use HTTP/2 with adaptive window sizing, connection pool tuning (90s idle timeout, 10 max idle per host), and TCP keepalive (30s) for improved throughput.

**Security**

ASVS L2 compliance has reached 100% (34/34 requirements met), covering path traversal protection, automatic log redaction, restricted directory permissions, and pipeline injection hardening.

### CLI Commands

```bash
# Check swarm status
raps swarm status

# Reset swarm state (circuit breakers, caches)
raps swarm reset

# Run a swarm workflow
raps swarm run workflow.yaml

# Open TUI dashboard and press F8 for swarm tab
raps dashboard
```

### Availability

RAPS 5.0.0 is available now via:
- **Cargo**: `cargo install raps-cli`
- **Homebrew**: `brew install raps`
- **npm**: `npx @niceyemelianov/raps`
- **GitHub**: github.com/dmytro-yemelianov/raps

---

**About RAPS**

RAPS is an open-source command-line interface for Autodesk Platform Services (APS), written in Rust. It provides 95+ commands across authentication, data management, model translation, design automation, construction cloud, webhooks, and account administration. RAPS also includes an MCP server with 105 tools for AI assistant integration.

**Contact**: Dmytro Yemelianov — github.com/dmytro-yemelianov/raps
