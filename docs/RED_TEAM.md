# RED_TEAM.md — Attack your own number before you sign it

Skepticism as a repeatable method, not a talent. Before any number leaves your
hands (into a dashboard, a report, a decision, a payment), run it through this.

## The one rule

> A number that flatters you is the one to attack first.

If a result makes the business look good (margin up, churn down, revenue
higher than expected), assume it's wrong until you've tried to break it.

## The checklist

**1. What am I actually counting?**
People, transactions, sessions, or rows? A customer with 3 renewals is one
person and three transactions. If the sum of categories exceeds the total,
you're counting transactions, not people.

**2. One population, one method?**
Does every section of the report join back to the *same* population
definition? Or did tab 3 quietly switch from "paid customers" to "all leads"?

**3. Snapshot or primary?**
Is this an aggregate/trend (snapshot is fine) or an existence/decision/payment
question (must hit the live primary source)? Absence from a snapshot is **not**
proof something doesn't exist.

**4. Does it reconcile across sources?**
If two systems disagree, the truth is the verified intersection with the deltas
*explained* — never whichever number is bigger.

**5. Sanity bounds.**
Is the result physically possible? Bigger than the total universe? A rate above
100%? A sudden 3x jump with no known cause? Those are red flags, not wins.

**6. Reproduce from scratch.**
Can someone else run it and get the same number? If it only works in your head
or your notebook, it isn't a number yet.

## Turn it into tests

Anything on this checklist that can be a test, *should* be a test — so a
regression fails CI instead of shipping a wrong number to leadership. See
`tests/test_counting_rules.py` for the pattern.
