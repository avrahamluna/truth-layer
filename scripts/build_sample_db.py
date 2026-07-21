"""Build a small SQLite db to demonstrate the truth-layer rules.

All customers/orders/charges are generated at runtime.
"""
import sqlite3
import random
from pathlib import Path

random.seed(42)
DB = Path(__file__).resolve().parent.parent / "sample.db"


def build() -> None:
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.executescript(
        """
        CREATE TABLE customers (customer_id TEXT PRIMARY KEY, gender TEXT);
        CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id TEXT, status TEXT);
        CREATE TABLE charges (charge_id INTEGER PRIMARY KEY, customer_id TEXT, status TEXT);
        CREATE TABLE order_line_items (order_id INTEGER, customer_id TEXT, product TEXT);
        """
    )

    genders = ["female", "male", "unknown"]
    n = 1000
    customers = [(f"cust_{i}", random.choices(genders, weights=[81, 18, 1])[0]) for i in range(n)]
    cur.executemany("INSERT INTO customers VALUES (?,?)", customers)

    order_id = charge_id = 0
    for i in range(n):
        cid = f"cust_{i}"
        paid = random.random() < 0.85          # 85% have a paid order (app source)
        charged = random.random() < 0.88       # 88% have a succeeded charge (payments)
        if paid:
            order_id += 1
            cur.execute("INSERT INTO orders VALUES (?,?,?)", (order_id, cid, "paid"))
            # a customer can have several renewals -> multiple line items
            for _ in range(random.randint(1, 3)):
                product = random.choice(["A", "B", "C"])
                cur.execute("INSERT INTO order_line_items VALUES (?,?,?)", (order_id, cid, product))
        else:
            order_id += 1
            cur.execute("INSERT INTO orders VALUES (?,?,?)", (order_id, cid, "pending"))
        if charged:
            charge_id += 1
            cur.execute("INSERT INTO charges VALUES (?,?,?)", (charge_id, cid, "succeeded"))

    con.commit()
    con.close()
    print(f"built {DB}")


if __name__ == "__main__":
    build()
