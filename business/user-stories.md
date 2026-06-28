Generated `user-stories.md` — 12 stories across 4 epics for **cannabis-ops-sync**.

# cannabis-ops-sync — User Stories

> Format: Connextra (`As a <role>, I want <action>, so that <outcome>`)
> Complexity: **S** ≤3 dev-days · **M** 4–10 dev-days · **L** >10 dev-days / cross-cutting
> Roles: **Compliance Manager**, **Inventory Clerk**, **Cultivation/Floor Supervisor**, **Ops Director**, **MSO Executive**

---

## Epic 1 — Compliance & ERP Bi-Directional Sync
*The wedge: Metrc/BioTrack ↔ ERP/POS is the single largest source of manual re-keying and audit risk.*

### US-1.1 — Two-way Metrc sync `L`
**As a** Compliance Manager, **I want** packages, plants, harvests, and transfers to sync automatically between Metrc and our ERP, **so that** I stop double-entering every tag and avoid reconciliation drift.
- Pull on a configurable interval (≤15 min) via official API key per license.
- Push ERP-originated adjustments back to Metrc with idempotent retry.
- Field-level conflict detection instead of silent overwrite.
- Per-license rate-limit handling with backoff; no failed call drops a record.
- Full audit log of every synced field.

### US-1.2 — Pluggable traceability + ERP connectors `L`
**As an** Ops Director in a BioTrack state, **I want** the engine to work with my state system and ERP/POS (Dutchie, Flowhub, BioTrack, QuickBooks/NetSuite), **so that** I'm not locked into one vendor stack.
- Connector interface abstracts auth/pull/push/mapping; ≥2 traceability + ≥2 ERP/POS at GA.
- Config-driven field mapping — no code change to remap a field.
- Connector health view (last-success, last-error, lag).

### US-1.3 — License-scoped multi-state config `M`
**As an** MSO Executive, **I want** to register multiple licenses/states with their own credentials and rules, **so that** one account covers my footprint without cross-license data bleed.
- Per-license keys, ruleset, timezone; data hard-partitioned by license.
- Reports never mix licenses unless explicitly aggregated.
- Role permissions scopable to specific licenses.

---

## Epic 2 — Automated Data Entry & Error Reduction
*Where "reduce manual errors" becomes measurable.*

### US-2.1 — State-rule validation engine `M`
**As a** Compliance Manager, **I want** entries validated against state rules before they sync, **so that** I catch violations before the state does.
- Configurable per-state rules (limits, package size, manifests, lab-test gating).
- Blocking vs. warning severity; blocking entries can't sync until resolved.
- Each flag links to the rule + remediation hint.
- Versioned rule set reproduces the rule active on any date.

### US-2.2 — Bulk import with auto-mapping `M`
**As an** Inventory Clerk, **I want** to upload CSVs with auto-mapped columns, **so that** I onboard historical/vendor data without line-by-line entry.
- Header auto-detect; confirmed mapping saves as reusable template.
- Pre-import dry-run report (rows, errors, dupes, rejects).
- Partial-success import — bad rows export to a fixable error file.

### US-2.3 — Discrepancy & reconciliation alerts `M`
**As an** Ops Director, **I want** alerts when physical counts, ERP, and Metrc disagree, **so that** shrinkage is caught daily, not at audit.
- Scheduled three-source reconciliation per SKU/package.
- Variance threshold ($ and units); alerts via email/Slack/in-app.
- One-click drill-down to contributing records.

---

## Epic 3 — Task & Workflow Management
*Turns data-fix signals into assignable, trackable work.*

### US-3.1 — Auto-generated remediation tasks `M`
**As a** Floor Supervisor, **I want** validation failures and discrepancies to become assigned tasks automatically, **so that** every issue has an owner and due date.
- Each blocking error/discrepancy spawns a task with context, owner, due date.
- Tasks auto-close when the record passes validation/sync.
- Status board filterable by location and assignee.

### US-3.2 — Recurring compliance checklists `S`
**As a** Compliance Manager, **I want** recurring SOP checklists, **so that** routine compliance is enforced and timestamped.
- Templated recurring tasks with cadence + required-evidence fields.
- Overdue escalation to a configured manager.
- Completion history exportable as audit evidence.

### US-3.3 — Role-based queues & notifications `S`
**As a** Cultivation Supervisor, **I want** to see only role/room-relevant tasks, **so that** my team isn't buried in dispensary or finance noise.
- Per-role default views + saved custom filters.
- Notification prefs per channel and event type.
- Mobile-friendly task view for floor/grow staff.

---

## Epic 4 — Reporting, Audit & Cross-Site Oversight
*The renewal argument: fewer violations, faster audits, executive visibility.*

### US-4.1 — Audit-ready activity trail `M`
**As a** Compliance Manager, **I want** an immutable, exportable log of every change and sync, **so that** an audit takes hours, not weeks.
- Every change recorded with actor, source, before/after, timestamp.
- Filter by license, date, tag, user.
- Export to PDF/CSV with tamper-evident hash.

### US-4.2 — Cross-site operations dashboard `M`
**As an** MSO Executive, **I want** a roll-up of sync health, open issues, and shrinkage across licenses, **so that** I spot the riskiest location at a glance.
- KPI tiles per site (synced, violations, discrepancy $, overdue tasks).
- Drill company → license → record.
- Scheduled emailed digest.

### US-4.3 — ROI / error-reduction report `S`
**As an** Ops Director, **I want** a report of manual entries eliminated and errors prevented, **so that** I can justify cost at renewal.
- Tracks auto-synced records, blocked violations, reconciled variance vs. baseline.
- Trend charts by month and location.
- Exportable budget-review summary.

---

### Coverage summary
| Epic | Stories | S / M / L |
|---|---|---|
| 1 — Compliance & ERP Sync | 3 | 0 / 1 / 2 |
| 2 — Data Entry & Error Reduction | 3 | 0 / 3 / 0 |
| 3 — Task & Workflow Management | 3 | 2 / 1 / 0 |
| 4 — Reporting & Oversight | 3 | 1 / 2 / 0 |
| **Total** | **12** | **3 / 7 / 2** |

**MVP cut:** US-1.1, US-2.1, US-2.3, US-3.1 — sync Metrc↔ERP, validate against state rules pre-submission, alert on count/ERP/Metrc discrepancies, auto-spawn a fix task. The defensible wedge over a spreadsheet or generic ERP is **bi-directional state-traceability sync + a versioned compliance rule engine** — integration and per-state audit logic operators can't safely DIY.