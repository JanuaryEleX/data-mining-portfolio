import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

base = Path(__file__).resolve().parent
conn = sqlite3.connect(base / "operations.db")

plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid")

queries = {
    "monthly_gmv": """
        SELECT strftime('%Y-%m', order_date) AS month,
               ROUND(SUM(amount), 2) AS gmv,
               COUNT(*) AS paid_orders,
               COUNT(DISTINCT user_id) AS paid_users,
               ROUND(SUM(amount) / COUNT(*), 2) AS avg_order_value
        FROM orders
        WHERE status = 'paid'
        GROUP BY month
        ORDER BY month
    """,
    "channel_conversion": """
        SELECT u.channel,
               COUNT(DISTINCT u.user_id) AS registered_users,
               COUNT(DISTINCT o.user_id) AS paid_users,
               ROUND(COUNT(DISTINCT o.user_id) * 100.0 / COUNT(DISTINCT u.user_id), 2) AS paid_conversion_rate
        FROM users u
        LEFT JOIN orders o ON u.user_id = o.user_id AND o.status = 'paid'
        GROUP BY u.channel
        ORDER BY paid_conversion_rate DESC
    """,
    "category_gmv": """
        SELECT p.category,
               COUNT(*) AS orders,
               ROUND(SUM(o.amount), 2) AS gmv,
               ROUND(SUM(o.amount) * 100.0 / (SELECT SUM(amount) FROM orders WHERE status = 'paid'), 2) AS gmv_share
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.status = 'paid'
        GROUP BY p.category
        ORDER BY gmv DESC
    """,
    "funnel": """
        SELECT COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END) AS view_users,
               COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_id END) AS cart_users,
               COUNT(DISTINCT CASE WHEN event_type = 'pay' THEN user_id END) AS pay_users,
               ROUND(COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_id END) * 100.0 / COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END), 2) AS view_to_cart_rate,
               ROUND(COUNT(DISTINCT CASE WHEN event_type = 'pay' THEN user_id END) * 100.0 / COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_id END), 2) AS cart_to_pay_rate
        FROM events
    """,
    "retention": """
        WITH first_active AS (
            SELECT user_id, MIN(event_date) AS first_date
            FROM events
            GROUP BY user_id
        ), retention AS (
            SELECT f.user_id,
                   MAX(CASE WHEN julianday(e.event_date) - julianday(f.first_date) BETWEEN 1 AND 7 THEN 1 ELSE 0 END) AS retained_7d
            FROM first_active f
            LEFT JOIN events e ON f.user_id = e.user_id
            GROUP BY f.user_id
        )
        SELECT COUNT(*) AS active_users,
               SUM(retained_7d) AS retained_7d_users,
               ROUND(SUM(retained_7d) * 100.0 / COUNT(*), 2) AS retention_7d_rate
        FROM retention
    """,
    "repurchase": """
        WITH user_order_cnt AS (
            SELECT user_id, COUNT(*) AS order_cnt
            FROM orders
            WHERE status = 'paid'
            GROUP BY user_id
        )
        SELECT COUNT(*) AS paid_users,
               SUM(CASE WHEN order_cnt >= 2 THEN 1 ELSE 0 END) AS repurchase_users,
               ROUND(SUM(CASE WHEN order_cnt >= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS repurchase_rate
        FROM user_order_cnt
    """,
}

results = {name: pd.read_sql_query(sql, conn) for name, sql in queries.items()}
for name, df in results.items():
    df.to_csv(base / f"{name}.csv", index=False, encoding="utf-8-sig")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
monthly = results["monthly_gmv"]
sns.lineplot(data=monthly, x="month", y="gmv", marker="o", ax=axes[0, 0], color="#2563eb")
axes[0, 0].set_title("Monthly GMV Trend")
axes[0, 0].set_xlabel("")
axes[0, 0].set_ylabel("GMV")

channel = results["channel_conversion"]
sns.barplot(data=channel, x="paid_conversion_rate", y="channel", ax=axes[0, 1], palette="Blues_r")
axes[0, 1].set_title("Paid Conversion Rate by Channel")
axes[0, 1].set_xlabel("Conversion Rate (%)")
axes[0, 1].set_ylabel("")

category = results["category_gmv"]
sns.barplot(data=category, x="gmv", y="category", ax=axes[1, 0], palette="Greens_r")
axes[1, 0].set_title("GMV Contribution by Category")
axes[1, 0].set_xlabel("GMV")
axes[1, 0].set_ylabel("")

funnel = results["funnel"].iloc[0]
stages = ["View", "Cart", "Pay"]
values = [funnel["view_users"], funnel["cart_users"], funnel["pay_users"]]
sns.barplot(x=stages, y=values, ax=axes[1, 1], palette="Oranges_r")
axes[1, 1].set_title("User Conversion Funnel")
axes[1, 1].set_ylabel("Users")
for idx, value in enumerate(values):
    axes[1, 1].text(idx, value + 1, str(int(value)), ha="center")

plt.tight_layout()
plt.savefig(base / "sql_business_dashboard.png", dpi=180, bbox_inches="tight")

report = f"""# SQL用户运营分析报告

## 项目背景

本项目模拟互联网电商平台用户、商品、订单、行为日志四张业务表，通过 SQL 分析 GMV、渠道转化、复购、留存、漏斗和品类贡献，贴近数据分析实习岗位的真实工作场景。

## 数据表设计

| 表名 | 说明 |
|---|---|
| users | 用户注册信息，含城市、渠道、年龄 |
| products | 商品信息，含品类、价格 |
| orders | 订单信息，含金额、状态 |
| events | 用户行为日志，含浏览、加购、支付 |

## 核心指标结果

### 月度GMV

{results['monthly_gmv'].to_markdown(index=False)}

### 渠道付费转化

{results['channel_conversion'].to_markdown(index=False)}

### 复购率

{results['repurchase'].to_markdown(index=False)}

### 7日留存

{results['retention'].to_markdown(index=False)}

### 转化漏斗

{results['funnel'].to_markdown(index=False)}

### TOP品类GMV贡献

{results['category_gmv'].to_markdown(index=False)}

## 业务结论

1. 可通过月度 GMV 和客单价判断平台营收走势与消费质量。
2. 渠道转化率差异明显，预算应向高转化渠道倾斜。
3. 复购率用于衡量用户粘性，是运营策略优化重点。
4. 漏斗中加购到支付阶段若流失较高，可通过优惠券、免邮、支付提醒优化。
5. TOP品类贡献可指导选品、库存和营销资源分配。
"""
(base / "分析报告.md").write_text(report, encoding="utf-8")
conn.close()
print("SQL分析完成，已生成结果CSV、图表和报告")
