```markdown
# TECH_SPEC.md — cannabis-ops-sync

## 1. Overview

**cannabis-ops-sync** is an autonomous data pipeline and task orchestration engine for licensed cannabis operators. It ingests ERP events (orders, inventory, compliance logs), validates them against state seed-to-sale systems (Metrc, BioTrack, Leaf Data), and propagates approved changes into downstream POS, accounting, and compliance dashboards—eliminating duplicate entry and human error.

**Core Value Prop**
- **ERP → Compliance Sync**: Auto-push inventory adjustments, order statuses, and lab results to state traceability systems.
- **Task Automation**: Auto-create SOPs, batch manifests, manifest transfers, and manifest returns based on ERP triggers.
- **Audit Trail**: Immutable ledger of every state submission with cryptographic receipts for regulators.
- **Role-Based Access**: Granular permissions mapped to METRC roles (Owner, Manager, Agent, Lab Tech).

---

## 2. Architecture

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                                cannabis-ops-sync                              │
├───────────────────┬───────────────────┬───────────────────┬───────────────────┤
│   Ingestion       │   Validation      │   Orchestration   │   Propagation     │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┤
│  • ERP Webhooks   │  • State Schema   │  • Task Graph     │  • POS Sync       │
│  • CSV Uploads    │  • DQ Checks      │  • Retry Policies │  • Accounting     │
│  • API Polling    │  • License        │  • Idempotency    │  • Compliance     │
│  • SFTP Drop      │  • METRC API      │  • Dead Letter    │  • Dashboard      │
└───────────┬───────┴───────────┬───────┴───────────┬───────┴───────────┬───────┘
            │                   │                   │                   │
┌───────────▼───────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐
│  Ingestion Worker │ │  Validation Core  │ │  Task Orchestrator│ │  Propagation Core │
└───────────┬───────┘ └─────────┬─────────┘ └─────────┬─────────┘ └─────────┬─────────┘
            │                   │                   │                   │
┌───────────▼───────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐
│  Message Queue    │ │  State API Proxy │ │  Workflow Engine  │ │  Outbound Adapters│
│  (NATS JetStream) │ │  (REST/gRPC)     │ │  (Temporal)       │ │  (Kafka)         │
└───────────────────┘ └───────────────────┘ └───────────────────┘ └───────────────────┘
```

---

## 3. Components

### 3.1 Ingestion Layer

| Component | Responsibility | Tech | Dependencies |
|-----------|----------------|------|--------------|
| **Ingestion Worker** | Poll ERP APIs, consume webhooks, parse CSV/SFTP | Go 1.22 | NATS, ERP SDKs |
| **Schema Registry** | Normalize ERP payloads → canonical events | Protobuf | Schema Store (Postgres) |
| **Message Queue** | Buffer & route events; idempotent delivery | NATS JetStream | TLS 1.3, AuthN/Z |

**Event Contracts**
```protobuf
message ERPEvent {
  string id = 1;            // ERP UUID
  string type = 2;          // "inventory.adjustment", "order.fulfilled"
  google.protobuf.Timestamp ts = 3;
  bytes payload = 4;        // ERP-specific JSON
  string checksum = 5;      // SHA-256(payload)
}
```

---

### 3.2 Validation Core

| Component | Responsibility | Tech | Dependencies |
|-----------|----------------|------|--------------|
| **State Schema Validator** | Enforce METRC/BioTrack/Leaf schema | Rust | State SDKs |
| **License Validator** | Check operator license active & jurisdiction | Go | State API |
| **Data Quality Engine** | Reject negative inventory, invalid UIDs | Python | Pandas, Pydantic |
| **State API Proxy** | Rate-limit & retry state submissions | Go | Circuit Breaker |

**Validation Flow**
```
ERPEvent → Schema → License → DQ Checks → State API → Receipt
```

---

### 3.3 Orchestration Layer

| Component | Responsibility | Tech | Dependencies |
|-----------|----------------|------|--------------|
| **Task Graph** | Build dependency graph of tasks (e.g., "manifest → transfer → manifest return") | Temporal | Postgres |
| **Retry Policies** | Exponential backoff + jitter for state API failures | Go | Temporal SDK |
| **Idempotency Store** | Prevent duplicate state submissions | Redis | Lua scripts |
| **Dead Letter Queue** | Capture failed events for replay | NATS | Schema Store |

**Task Example**
```json
{
  "task_id": "manifest-123",
  "type": "manifest.transfer",
  "state_id": "WA-METRC-12345",
  "dependencies": ["inventory.adjustment-678"],
  "retry_policy": { "max_attempts": 5, "backoff": "exponential" }
}
```

---

### 3.4 Propagation Layer

| Component | Responsibility | Tech | Dependencies |
|-----------|----------------|------|--------------|
| **Outbound Adapters** | Push to POS, accounting, compliance dashboards | Kafka | ERP SDKs |
| **Audit Ledger** | Immutable log of every state submission | Postgres | pgcrypto |
| **Receipt Generator** | Produce cryptographic receipts (SHA-256 + timestamp) | Go | RFC 3161 |

**Receipt Example**
```json
{
  "receipt_id": "r-2024-05-08-12345",
  "state_id": "WA-METRC-12345",
  "checksum": "a1b2c3...",
  "timestamp": "2024-05-08T12:00:00Z",
  "signature": "MEUCIQ..."
}
```

---

## 4. Data Model

### 4.1 Canonical Events (Postgres)

```sql
CREATE TABLE events (
  id UUID PRIMARY KEY,
  type TEXT NOT NULL,          -- "inventory.adjustment", "order.fulfilled"
  erp_id TEXT NOT NULL,        -- ERP UUID
  payload JSONB NOT NULL,
  checksum TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(erp_id, type)
);

CREATE TABLE state_receipts (
  id UUID PRIMARY KEY,
  event_id UUID REFERENCES events(id),
  state_id TEXT NOT NULL,      -- "WA-METRC-12345"
  receipt JSONB NOT NULL,
  submitted_at TIMESTAMPTZ NOT NULL,
  response_code INT NOT NULL,
  error TEXT
);
```

### 4.2 Task State (Postgres)

```sql
CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  type TEXT NOT NULL,          -- "manifest.transfer", "inventory.adjustment"
  state_id TEXT NOT NULL,      -- METRC ID
  status TEXT NOT NULL,        -- "pending", "running", "completed", "failed"
  payload JSONB NOT NULL,
  retry_count INT DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_state_id ON tasks(state_id);
CREATE INDEX idx_tasks_status ON tasks(status);
```

---

## 5. Key APIs & Interfaces

### 5.1 Ingestion API

**Endpoint**: `POST /api/v1/events`
**Auth**: JWT (scope: `ingest:events`)
**Body**:
```json
{
  "type": "inventory.adjustment",
  "erp_id": "erp-123",
  "payload": { ... },
  "checksum": "sha256(...)"
}
```
**Response**:
```json
{ "id": "evt-123", "status": "accepted" }
```

### 5.2 State API Proxy

**Endpoint**: `POST /api/v1/state/{state_id}/submit`
**Auth**: JWT (scope: `state:submit`)
**Body**:
```json
{
  "type": "inventory.adjustment",
  "payload": { ... }
}
```
**Response**:
```json
{
  "receipt_id": "r-2024-05-08-12345",
  "state_id": "WA-METRC-12345",
  "response_code": 200
}
```

### 5.3 Task API

**Endpoint**: `POST /api/v1/tasks`
**Auth**: JWT (scope: `tasks:create`)
**Body**:
```json
{
  "type": "manifest.transfer",
  "state_id": "WA-METRC-12345",
  "payload": { ... }
}
```
**Response**:
```json
{ "id": "task-123", "status": "pending" }
```

---

## 6. Tech Stack

| Layer | Tech | Version | Rationale |
|-------|------|---------|-----------|
| **Language** | Go | 1.22 | Performance, concurrency, static typing |
| **Validation** | Rust | 1.78 | Safety, speed, state SDK bindings |
| **Orchestration** | Temporal | 1.22 | Durable workflows, retries, visibility |
| **Message Queue** | NATS JetStream | 2.10 | Low latency, persistence, idempotency |
| **Database** | Postgres | 16 | ACID, JSONB, full-text search |
| **Cache** | Redis | 7.2 | Idempotency, rate limiting |
| **Streaming** | Kafka | 3.7 | Outbound event propagation |
| **Auth** | Ory Hydra | 2.0 | OAuth2, JWT, RBAC |
| **Observability** | Prometheus + Grafana | 2.50 | Metrics, dashboards |
| **Logging** | Loki + Tempo | 2.9 | Structured logs, traces |
| **Deployment** | Kubernetes | 1.29 | Auto-scaling, rollbacks |
| **CI/CD** | GitHub Actions | latest | Reproducible builds |

---

## 7. Dependencies

### 7.1 Licensed Libraries

| Library | License | Usage |
|---------|---------|-------|
| NATS Server | Apache-2.0 | Message queue |
| Temporal | MIT | Workflow engine |
| Ory Hydra | Apache-2.0 | Auth/OAuth2 |
| Prometheus | Apache-2.0 | Metrics |
| Grafana | AGPL-3.0 | Dashboards |

### 7.2 State SDKs

| State | SDK | License | Notes |
|-------|-----|---------|-------|
| METRC | metrc-sdk-go | MIT | Official Go SDK |
| BioTrack | biotrack-sdk-py | Apache-2.0 | Python SDK |
| Leaf Data | leaf-sdk-rs | MIT | Rust SDK |

### 7.3 ERP SDKs

| ERP | SDK | License | Notes |
|-----|-----|---------|-------|
| Greenbits | greenbits-sdk | MIT | POS integration |
| BioTrack | biotrack-erp | Apache-2.0 | ERP sync |
| MJ Freeway | mjf-sdk | MIT | Legacy support |

---

## 8. Deployment

### 8.1 Kubernetes Manifests

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ingestion-worker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ingestion-worker
  template:
    metadata:
      labels:
        app: ingestion-worker
    spec:
      containers:
      - name: worker
        image: ghcr.io/axentx/cannabis-ops-sync/ingestion-worker:v0.1.0
        env:
        - name: NATS_URL
          value: "nats://nats:4222"
        - name: ERP_SDK_URL
          value: "https://erp.example.com"
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
```

### 8.2 Helm Chart

```yaml
# values.yaml
ingestion:
  replicas: 3
  resources:
    requests:
      cpu: "500m"
      memory: "256Mi"
validation:
  replicas: 2
  resources:
    requests:
      cpu: "250m"
      memory: "128Mi"
temporal:
  enabled: true
  server:
    replicas: 1
```

### 8.3 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NATS_URL` | NATS server URL | `nats://nats:4222` |
| `ERP_SDK_URL` | ERP API base URL | `https://erp.example.com` |
| `STATE_API_KEY` | State API key (encrypted) | `k8s://state-api-key` |
| `JWT_SECRET` | JWT signing key | `k8s://jwt-secret` |
| `REDIS_URL` | Redis connection string | `redis://redis:6379` |

---

## 9. Security

- **TLS 1.3** for all external traffic (NATS, Kafka, ERP APIs).
- **JWT** with short-lived tokens (15m) and scope-based RBAC.
- **Secrets** stored in Kubernetes Secrets (encrypted at rest).
- **Network Policies** restrict pod-to-pod communication.
- **Audit Logs** immutable via Postgres + pgcrypto.

---

## 10. Observability

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `ingestion_queue_depth` | NATS JetStream queue depth | >1000 → PagerDuty |
| `state_api_errors` | State API failure rate | >5% → Slack |
| `task_duration_seconds` | Task completion time | >30s → Grafana |
| `receipts_generated` | State receipts per hour | <100 → Alert |

---

## 11. Rollout Plan

| Phase | Milestone | Owner | ETA |
|-------|-----------|-------|-----|
| 1 | MVP (ERP → METRC sync) | PM/Arch | 4 weeks |
| 2 | Multi-state support (BioTrack, Leaf) | Dev | 6 weeks |
| 3 | Task automation (manifests, SOPs) | Dev | 8 weeks |
| 4 | Compliance dashboard & receipts | Dev | 10 weeks |
| 5 | Hard-gate validation (real pain + WTP) | Reviewer | 12 weeks |

---

## 12. Success Metrics

- **ERP → State Sync Latency**: <5s p95
- **Duplicate Entry Reduction**: 95% (measured via audit logs)
- **State API Error Rate**: <1%
- **Task Automation Coverage**: 80% of manual tasks
- **Regulator Acceptance**: 100% of receipts accepted by METRC

---
```
