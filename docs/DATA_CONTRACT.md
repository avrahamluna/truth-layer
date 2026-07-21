# DATA_CONTRACT.md — Which source answers which question

## Rule #1: Don't re-pull data that already exists

Before pulling from any source (payments, app, ad platform):

1. Check this contract.
2. If the table exists → use it.
3. If you need data that isn't here → add it to the contract first, then pull.

## Rule #0 (most important): SNAPSHOT ≠ PRIMARY SOURCE

The local snapshot (`metrics.db`) is a **fast local copy**, not the live source
of truth.

| Your question is… | Use | Do NOT use |
|---|---|---|
| Aggregate / trend ("how much did we sell in X?") | 🟢 snapshot (fast) | — |
| Dashboard (read many times) | 🟢 snapshot | — |
| **Existence ("does this customer/sale exist?")** | 🔴 **live primary** | ❌ snapshot |
| **Reconciliation / money owed to a third party** | 🔴 **live primary** | ❌ snapshot |
| Anything feeding a **decision / payment / legal** | 🔴 **primary** | ❌ snapshot |

**One line:** snapshot to *explore and aggregate*; primary to *assert and decide*.

⚠️ **Never** treat "absent from the snapshot" as "doesn't exist." The snapshot
lags the cutoff and omits the newest records. Treating absence as non-existence
once produced a false "phantom $46K" reconciliation gap that didn't exist.

✅ For existence checks, use the official helper that goes only to primaries, so
it's impossible to get wrong:

```python
from lib.verify_against_primary import verify_customer_exists
res = verify_customer_exists("cust_123")   # {source_a, source_b, exists, ...}
```

## Available tables

### `charges_enriched` — aggregate snapshot of charges
- Valid for **aggregates** up to its cutoff date. NOT authoritative for
  existence or the latest records. For existence → use the primary helper.
- Columns: `charge_id, created_date, amount, customer_id, product_class,
  plan_class, is_new, refunded, disputed, match_tier`

### `conversions` — funnel bottom (event = 'Sale')
- Columns: `conversion_id, conversion_date, affiliate_id, payout, revenue, status`

### `clicks_monthly` — funnel top (raw traffic, NOT conversions)
- Columns: `month (PK), total_click, unique_click, invalid_click, gross_click`
- ⚠️ Caveat: at the offer-grouped level `unique_click == total_click` (not
  deduplicated by visitor). Treat both as click volume, not unique humans.
