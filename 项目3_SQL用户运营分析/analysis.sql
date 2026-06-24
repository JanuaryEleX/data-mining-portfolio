-- SQL用户运营分析项目
-- 作者：何易
-- 目标：用 SQL 分析互联网电商业务核心指标：GMV、留存、复购、渠道质量、转化漏斗

-- 1. 每月 GMV、订单数、客单价
SELECT
    strftime('%Y-%m', order_date) AS month,
    ROUND(SUM(amount), 2) AS gmv,
    COUNT(*) AS paid_orders,
    COUNT(DISTINCT user_id) AS paid_users,
    ROUND(SUM(amount) / COUNT(*), 2) AS avg_order_value
FROM orders
WHERE status = 'paid'
GROUP BY month
ORDER BY month;

-- 2. 渠道拉新与付费转化
SELECT
    u.channel,
    COUNT(DISTINCT u.user_id) AS registered_users,
    COUNT(DISTINCT o.user_id) AS paid_users,
    ROUND(COUNT(DISTINCT o.user_id) * 100.0 / COUNT(DISTINCT u.user_id), 2) AS paid_conversion_rate
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id AND o.status = 'paid'
GROUP BY u.channel
ORDER BY paid_conversion_rate DESC;

-- 3. 用户复购率
WITH user_order_cnt AS (
    SELECT user_id, COUNT(*) AS order_cnt
    FROM orders
    WHERE status = 'paid'
    GROUP BY user_id
)
SELECT
    COUNT(*) AS paid_users,
    SUM(CASE WHEN order_cnt >= 2 THEN 1 ELSE 0 END) AS repurchase_users,
    ROUND(SUM(CASE WHEN order_cnt >= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS repurchase_rate
FROM user_order_cnt;

-- 4. 注册后7日留存
WITH first_active AS (
    SELECT user_id, MIN(event_date) AS first_date
    FROM events
    GROUP BY user_id
), retention AS (
    SELECT
        f.user_id,
        f.first_date,
        MAX(CASE WHEN julianday(e.event_date) - julianday(f.first_date) BETWEEN 1 AND 7 THEN 1 ELSE 0 END) AS retained_7d
    FROM first_active f
    LEFT JOIN events e ON f.user_id = e.user_id
    GROUP BY f.user_id, f.first_date
)
SELECT
    COUNT(*) AS active_users,
    SUM(retained_7d) AS retained_7d_users,
    ROUND(SUM(retained_7d) * 100.0 / COUNT(*), 2) AS retention_7d_rate
FROM retention;

-- 5. 漏斗转化：浏览 -> 加购 -> 支付
SELECT
    COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END) AS view_users,
    COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_id END) AS cart_users,
    COUNT(DISTINCT CASE WHEN event_type = 'pay' THEN user_id END) AS pay_users,
    ROUND(COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_id END) * 100.0 / COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END), 2) AS view_to_cart_rate,
    ROUND(COUNT(DISTINCT CASE WHEN event_type = 'pay' THEN user_id END) * 100.0 / COUNT(DISTINCT CASE WHEN event_type = 'cart' THEN user_id END), 2) AS cart_to_pay_rate
FROM events;

-- 6. TOP品类销售贡献
SELECT
    p.category,
    COUNT(*) AS orders,
    ROUND(SUM(o.amount), 2) AS gmv,
    ROUND(SUM(o.amount) * 100.0 / (SELECT SUM(amount) FROM orders WHERE status = 'paid'), 2) AS gmv_share
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'paid'
GROUP BY p.category
ORDER BY gmv DESC;
