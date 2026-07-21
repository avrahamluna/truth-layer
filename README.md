# truth-layer

A **single source of truth** layer for businesses whose data lives across
multiple systems (a payments processor, an internal app/CRM, an ad/affiliate
platform) and who no longer trust their own numbers.

> Generalized from a production system I designed and operated (2025–2026) that
> unified 3+ data sources into one reconciled, auditable layer. All names,
> unified 3+ data sources into one reconciled, auditable layer.

---

## The problem

Most companies with real traction already have data. What they *don't* have is
**one place they can trust**. The same question ("how many customers do we
have?") returns three different answers depending on who runs the query and
which table they hit.

Typical failure modes (all real, all seen in production):

- **Population mixing** — tab 1 counts sessions, tab 2 counts leads, tab 3
  counts paid customers. The numbers aren't comparable, but they're shown
  side by side.
- **`COUNT(*)` instead of `COUNT(DISTINCT ...)`** — transactions counted as
  people. A customer with 3 renewals counts as 3.
- **Snapshot treated as source of truth** — an aggregate snapshot is fast but
  lags reality; using it to answer "does this customer exist?" produces false
  negatives that cost money.

## The approach

1. **Contract first** (`docs/DATA_CONTRACT.md`) — one document that says which
   table answers which question, and which questions *must* hit the live
   primary source instead of the snapshot.
2. **One population, one method, whole report** (`docs/COUNTING_RULES.md`) —
   define the population in a single CTE and reuse it everywhere.
3. **Tests that enforce the rules** (`tests/`) — "no customer counted twice",
   "category totals never exceed the population", "populations never mixed".
4. **CI that runs the tests on every push** (`.github/workflows/ci.yml`) — the
   truth layer audits itself.

## Architecture

```
   ┌────────────┐   ┌────────────┐   ┌──────────────┐
   │  payments  │   │  app / CRM │   │ ad / affiliate│   sources
   └─────┬──────┘   └─────┬──────┘   └──────┬───────┘
         │                │                 │
         └────────┬───────┴────────┬────────┘
                  ▼                 ▼
          ┌───────────────────────────────┐
          │   reconciliation + contract    │   truth layer
          │   (one population, one method) │
          └───────────────┬───────────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        dashboards    reports     automated audits
```

See `docs/ARCHITECTURE.md` for the full diagram and reasoning.

## Layout

| Path | What |
|------|------|
| `docs/DATA_CONTRACT.md` | Which source answers which question (snapshot vs primary) |
| `docs/COUNTING_RULES.md` | How to count people without double-counting or mixing populations |
| `docs/ARCHITECTURE.md`   | System diagram and design decisions |
| `models/`                | Example SQL models |
| `tests/`                 | Data-quality tests that enforce the rules |
| `.github/workflows/`     | CI that runs the tests on every push |

## Run the tests

```bash
pip install -r requirements.txt
pytest -q
```

## Note on data

This repo demonstrates the *methodology* and *engineering practices* of a real
*engineering practices* of a real production system without exposing any
customer data, credentials, or business-specific figures.
