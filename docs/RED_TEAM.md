# Red Team: how to break your own number before someone else does

Most data errors don't get caught by better SQL. They get caught by **someone
refusing to trust the first answer** — including their own. This document is the
method I used, as the auditing/QA layer of a production data team, to stop wrong
numbers *before* they reached leadership.

It is not a linter. It is a discipline. The point is to attack your own output
with the same hostility a skeptical stakeholder will — but privately, first, so
the public answer is already bulletproof.

> The failure patterns below are real; the names, figures, and schemas have been
> real; the names, figures, and schemas are invented.

---

## The core idea

> A number you haven't tried to break is a number you don't understand yet.

Before any material figure ships, it passes three layers. If it fails a layer,
it doesn't ship — you go back and verify more.

---

## Layer 1 — The three mandatory questions

Ask these about **every** material number, out loud, before reporting it:

### 1. Did I classify by the right FIELD, or by a fragile shortcut?
The field always wins over a shortcut (an id prefix, a name substring, a
display string).

- ❌ `WHERE charge_id LIKE 'pi_%'` to mean "card payment"
- ✅ `WHERE transaction_type = 'charge' AND payment_method = 'card'`

**Real pattern caught:** a revenue figure was filtered by an id prefix as a
proxy for payment type. The prefix didn't mean what everyone assumed; the filter
silently dropped a large block of legitimate transactions. Classifying by the
actual type field restored them. *The shortcut was wrong in a way the total
looked fine — that's the danger.*

### 2. Did I verify against TWO independent sources, or just one?
One source lets you be confidently wrong. Two sources that disagree tell you
*where* the truth is.

- Internal app DB says X. Payments processor says Y. If X ≠ Y, **that gap is the
  finding**, not an annoyance to paper over.

**Real pattern caught:** a "failed payments" count from the internal DB was ~2x
off from the processor's. The instinct is to pick one. The correct move was to
discover *why* they differ (the internal DB never ingested certain decline
events) — which turned a number into an actual root-cause finding.

### 3. Did I spot-check at the ROW level, or trust the aggregate?
Aggregates hide mixtures. A clean-looking `SUM` can blend refunds, disputes,
authorizations-not-captured, and real revenue into one plausible-but-wrong total.

- Pull 3–5 individual rows behind the number. Trace each one end to end.

**Real pattern caught:** an aggregate "success rate" looked like ~65%. At the
row level it was two different stages mashed together (an authorization step and
a capture step). The single headline number was meaningless once you saw the
rows.

**If you can't pass all three, you don't ship. You keep verifying.**

---

## Layer 2 — Spawn an adversary

For anything going to leadership, run a dedicated pass whose *only* job is to
break the number. Give it one instruction:

> "Try to BREAK this figure. Look for: double counting, mixed types,
> authorization-not-captured, wrong date basis, single-source reliance,
> classification by shortcut, and **peras-con-manzanas** (numerator and
> denominator drawn from different populations). Report the single biggest hole."

If it finds a hole → fix it and re-run. If it finds nothing → *now* you ship.

### The failure this catches most often: population mixing
The most common way a "finding" collapses under review:

> You measured 10,000 cancellations from source A (one universe) and compared it
> to a dashboard tile showing 42,000 churned split across 5 categories (a
> different universe). Your "97% vs 9%" contradiction is **peras con manzanas** —
> the two numbers were never comparable. The dashboard wasn't wrong; your
> comparison was.

A red-team pass exists to catch exactly this *before* you claim the dashboard is
broken. Numerator and denominator must come from the **same population**.

---

## Layer 3 — The human is confirmation, not discovery

By the time a person asks *"are you sure?"*, the answer should already have
survived Layers 1 and 2. Their skepticism should **confirm** a vetted number —
not be the first time the error gets caught.

If a stakeholder's first question breaks your number, the process failed, not
just the number.

---

## The classification of every material figure

Before shipping, tag the number:

| Tag | Meaning | Ships to leadership? |
|-----|---------|----------------------|
| ✅ Reconciles | Matches independent source within tolerance (<1%) | Yes |
| ⚠️ Delta acceptable | 1–5% gap, explained | Yes, with the caveat stated |
| ❌ Material delta | >5% gap, unexplained | No — investigate first |
| 🔲 Not auditable | Can't be reproduced from available sources | No — say so explicitly |

"Not auditable" is a valid, honest verdict. Reporting a number you **cannot
reproduce** is worse than saying "this tile can't be verified from our data."

---

## What makes a finding *irrefutable* (worth escalating)

A finding survives review when it is:

1. **Classified by field**, not by shortcut.
2. **Confirmed in two independent sources**, row-level.
3. **Same population** in numerator and denominator (no peras-con-manzanas).
4. **Real captured value**, not authorizations or projections dressed as observed.
5. **Passed a hostile red-team pass** that tried and failed to break it.

A finding that fails any of these is *interesting*, not *shippable*. Know the
difference, and say which one you have.

---

## Anti-patterns (things that feel like findings but aren't)

- **"The number is wrong"** when the dashboard uses a documented internal mapping
  you didn't reconstruct. Get their formula before calling it broken.
- **"It doesn't reconcile"** when you're comparing a live snapshot to a
  point-in-time window. Snapshot ≠ window. Drift is expected.
- **A single source disagreeing with your expectation.** Expectation is not a
  source.
- **An orphan number** ("this $X doesn't tie to anything") — unreconciled is a
  question, not yet a bug.

---

## TL;DR

Attack your own number in private with three layers — right field, two sources,
row-level — then spawn an adversary to break it, and only let a human *confirm*
what already survived. The goal isn't to be right on the first try. It's to
never ship a number you haven't earned the right to trust.
