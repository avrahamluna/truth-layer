# COUNTING_RULES.md — How to count people without lying to yourself

> Written after repeated population-mixing errors in production reporting.
> Read this before writing any report that counts people.

## Rule #1: ONE population, ONE method, the WHOLE report

Before writing a single query, define:

1. **What am I counting?** (people, charges, orders, sessions)
2. **From where?** (payments source, app source, both)
3. **With what filter?** (paid orders, succeeded charges, all leads)

That definition applies to **every** tab/section of the report. No exceptions.

## Common errors (all made, all fixed)

### ❌ Mixing populations between tabs

```
Tab 1: Gender → sessions      (1.87M sessions)
Tab 2: Age    → leads         (964K leads)
Tab 3: State  → paid customers (300K)
Tab 4: Reason → sessions, no DISTINCT (3.2M rows)
```

Each tab counts something different. The numbers are not comparable.

**Fix:** one CTE up front that defines the population:

```sql
WITH paid_customers AS (
  SELECT DISTINCT customer_id
  FROM orders
  WHERE status = 'paid'
)
-- the ENTIRE report joins back to this CTE
```

### ❌ `COUNT(*)` instead of `COUNT(DISTINCT customer_id)`

```sql
-- WRONG: counts sessions, not people
SELECT gender, COUNT(*) FROM sessions GROUP BY gender;
-- Female: 1,200,000  (sessions, not people)

-- RIGHT: counts unique people
SELECT gender, COUNT(DISTINCT customer_id) FROM sessions GROUP BY gender;
-- Female: 180,000  (real people)
```

**Rule:** if you are counting people, ALWAYS `DISTINCT customer_id` (or email).

### ❌ Counting orders/charges as if they were people

```sql
-- WRONG: one customer with 3 renewals counts 3 times
SELECT product, COUNT(*) FROM order_line_items GROUP BY product;

-- RIGHT: per unique person
SELECT product, COUNT(DISTINCT customer_id)
FROM order_line_items li JOIN orders o USING (order_id)
GROUP BY product;
```

**Alarm signal:** if the sum of your categories > total population, you are
counting transactions, not people.

### ❌ Trusting one source without cross-checking

Source A says 302K paid customers. Source B says 288K. The truth is the
**intersection** (verified in both), with the deltas explained — not whichever
number is bigger.

## The one-line version

> Define the population once, count distinct humans, and never let two
> definitions share a report.
