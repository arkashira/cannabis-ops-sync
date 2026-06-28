Generated `tech-spec.md` for **cannabis-ops-sync** (overwrote a stale `api-throttle` spec left in `/tmp`).

Key opinionated calls in this v1:
- **TS end-to-end / Fastify + BullMQ** — sync engine is the product, so I optimized for JSON Schema validation of every Metrc payload and rate-limit-aware polling.
- **Free-tier stack ≈ $0–25/mo at 5 orgs** (Railway + Neon + Upstash + R2), all **US-region-pinned** for cannabis data residency.
- **Compliance-first data model** — a canonical `records` table feeding a `discrepancies` engine that auto-spawns `tasks`, plus a 7-year immutable `audit_log`.
- **Security**: RLS + RBAC defense-in-depth, integration creds vaulted by reference (never in app DB), mandatory MFA for managers.

`tech-spec.md` written to `/tmp/tech-spec.md`.