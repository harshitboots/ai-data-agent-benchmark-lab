WITH valid_orders AS (
    SELECT
        o.customer_id,
        p.category,
        o.quantity * o.unit_price AS line_total
    FROM orders o
    JOIN products p ON p.product_id = o.product_id
    JOIN customers c ON c.customer_id = o.customer_id
    WHERE o.status <> 'cancelled'
      AND c.is_test_customer = false
      AND o.order_date BETWEEN DATE '2023-06-01' AND DATE '2024-05-31'
),
customer_category_totals AS (
    SELECT
        category,
        customer_id,
        COUNT(*) AS order_count,
        SUM(line_total) AS total_spend
    FROM valid_orders
    GROUP BY category, customer_id
    HAVING COUNT(*) > 1
)
SELECT
    t.category,
    t.customer_id,
    c.name AS customer_name,
    t.order_count,
    t.total_spend
FROM customer_category_totals t
JOIN customers c ON c.customer_id = t.customer_id
ORDER BY t.category ASC, t.total_spend DESC;
