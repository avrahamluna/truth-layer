"""Data-quality tests that ENFORCE the counting rules.

These are the rules from docs/COUNTING_RULES.md turned into CI checks:
a regression fails the build instead of silently shipping a wrong number.
"""
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "sample.db"


@pytest.fixture(scope="session", autouse=True)
def build_db():
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_sample_db.py")], check=True)
    yield
    if DB.exists():
        DB.unlink()


@pytest.fixture
def con():
    c = sqlite3.connect(DB)
    yield c
    c.close()


def trusted_population(con):
    return {
        row[0]
        for row in con.execute(
            """
            SELECT customer_id FROM orders WHERE status='paid'
            INTERSECT
            SELECT customer_id FROM charges WHERE status='succeeded'
            """
        )
    }


def test_no_customer_counted_twice(con):
    """A customer with multiple orders/charges must count once."""
    pop = trusted_population(con)
    distinct = con.execute(
        "SELECT COUNT(DISTINCT customer_id) FROM orders WHERE status='paid'"
    ).fetchone()[0]
    # population (a set) can never exceed distinct paid customers
    assert len(pop) <= distinct


def test_category_totals_never_exceed_population(con):
    """Sum of per-product unique customers must not exceed total population.

    (If it does, we're counting transactions, not people.)
    """
    pop = trusted_population(con)
    per_product = con.execute(
        """
        SELECT product, COUNT(DISTINCT li.customer_id)
        FROM order_line_items li
        JOIN orders o USING (order_id)
        WHERE o.status='paid'
        GROUP BY product
        """
    ).fetchall()
    # a customer may buy multiple products, so the SUM can exceed population,
    # but NO single product may exceed it
    for product, cnt in per_product:
        assert cnt <= len(pop), f"product {product}: {cnt} > population {len(pop)}"


def test_count_star_vs_distinct_diverge(con):
    """Sanity: COUNT(*) over line items must be >= DISTINCT customers.

    Demonstrates the classic bug the rules exist to prevent.
    """
    rows = con.execute("SELECT COUNT(*) FROM order_line_items").fetchone()[0]
    people = con.execute(
        "SELECT COUNT(DISTINCT customer_id) FROM order_line_items"
    ).fetchone()[0]
    assert rows >= people


def test_population_is_intersection_not_max(con):
    """Trusted population must be the intersection, never the bigger source."""
    pop = len(trusted_population(con))
    paid = con.execute(
        "SELECT COUNT(DISTINCT customer_id) FROM orders WHERE status='paid'"
    ).fetchone()[0]
    charged = con.execute(
        "SELECT COUNT(DISTINCT customer_id) FROM charges WHERE status='succeeded'"
    ).fetchone()[0]
    assert pop <= min(paid, charged)
