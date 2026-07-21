# ARCHITECTURE.md

## Goal

Turn three disconnected sources into one reconciled layer that a whole team
(and automated agents) can query without contradicting each other.

## Sources

- **Payments** — charges, refunds, disputes (money that actually moved).
- **App / CRM** — orders, products, plans, customer attributes (business context).
- **Ad / affiliate** — clicks and conversions (top and bottom of the funnel).

Each source has a different grain and a different notion of "a customer." The
truth layer's job is to reconcile them into **one population definition**.

## Layers

```
   sources ──▶ ingestion ──▶ reconciliation ──▶ contract'd models ──▶ consumers
                              (match tiers)      (snapshot + primary)   (dashboards,
                                                                         reports,
                                                                         audits)
```

1. **Ingestion** — pull each source, land raw.
2. **Reconciliation** — match records across sources into match tiers
   (exact id → email → fuzzy). Keep the intersection as the trusted population;
   log the deltas instead of hiding them.
3. **Contracted models** — expose a fast aggregate *snapshot* for exploration
   and a *primary* path for existence/decisions (see `DATA_CONTRACT.md`).
4. **Consumers** — dashboards, reports, and automated audit agents all read
   from the same contracted models.

## Key design decisions

- **Intersection over max.** When two sources disagree on customer count, the
  trusted number is the verified intersection, with deltas explained — never
  the bigger number.
- **Snapshot vs primary split.** Fast copy for aggregates; live source for
  anything that becomes a decision, a payment, or a legal statement.
- **Rules as tests, not docs.** The counting rules are enforced by CI tests, so
  a regression fails the build instead of silently shipping a wrong number.
- **Self-auditing.** Automated checks run on schedule and on every push, so the
  layer flags its own drift before a human notices.
