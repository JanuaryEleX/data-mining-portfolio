import sqlite3
from pathlib import Path
import random
from datetime import datetime, timedelta

random.seed(42)
base = Path(__file__).resolve().parent
conn = sqlite3.connect(base / "operations.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS products;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    register_date TEXT,
    city TEXT,
    channel TEXT,
    age INTEGER
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    category TEXT,
    product_name TEXT,
    price REAL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    order_date TEXT,
    amount REAL,
    status TEXT
);

CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    event_date TEXT,
    event_type TEXT
);
""")

cities = ["Chengdu", "Suining", "Luzhou", "Chongqing", "Deyang"]
channels = ["Organic Search", "Paid Ads", "Xiaohongshu", "Douyin", "Referral"]
categories = ["Digital", "Beauty", "Food", "Fashion", "Home"]
products = []
for product_id in range(1, 21):
    category = random.choice(categories)
    products.append((product_id, category, f"{category}商品{product_id}", round(random.uniform(29, 899), 2)))
cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)

start = datetime(2025, 1, 1)
users = []
for user_id in range(10001, 10151):
    register_date = start + timedelta(days=random.randint(0, 80))
    users.append((user_id, register_date.strftime("%Y-%m-%d"), random.choice(cities), random.choice(channels), random.randint(18, 45)))
cur.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?)", users)

order_id = 1
event_id = 1
for user_id, register_date, *_ in users:
    reg = datetime.strptime(register_date, "%Y-%m-%d")
    active_days = sorted(random.sample(range(0, 90), random.randint(2, 18)))
    for d in active_days:
        event_date = reg + timedelta(days=d)
        if event_date > datetime(2025, 4, 30):
            continue
        for event_type in ["view"] * random.randint(1, 5):
            cur.execute("INSERT INTO events VALUES (?, ?, ?, ?)", (event_id, user_id, event_date.strftime("%Y-%m-%d"), event_type))
            event_id += 1
        if random.random() < 0.45:
            cur.execute("INSERT INTO events VALUES (?, ?, ?, ?)", (event_id, user_id, event_date.strftime("%Y-%m-%d"), "cart"))
            event_id += 1
        if random.random() < 0.32:
            product = random.choice(products)
            amount = round(product[3] * random.uniform(0.8, 1.2), 2)
            status = "paid" if random.random() > 0.08 else "refund"
            cur.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", (order_id, user_id, product[0], event_date.strftime("%Y-%m-%d"), amount, status))
            order_id += 1
            cur.execute("INSERT INTO events VALUES (?, ?, ?, ?)", (event_id, user_id, event_date.strftime("%Y-%m-%d"), "pay"))
            event_id += 1

conn.commit()
conn.close()
print("operations.db generated")
