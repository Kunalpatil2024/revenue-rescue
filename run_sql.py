import duckdb

result= duckdb.sql("""

SELECT 
  order_status,
 COUNT(*) AS total_orders
FROM read_csv_auto('data/olist_orders_dataset.csv')
GROUP BY order_status
ORDER BY total_orders DESC;


SELECT COUNT(*) AS delivered_orders
FROM read_csv_auto('data/olist_orders_dataset.csv')
WHERE order_status = 'delivered';

SELECT *
FROM read_csv_auto('data/olist_order_items_dataset.csv')
LIMIT 10;


SELECT 
 SUM(price) AS total_revenue
FROM read_csv_auto('data/olist_order_items_dataset.csv');

SELECT
    SUM(freight_value) AS total_freight
FROM read_csv_auto('data/olist_order_items_dataset.csv');

SELECT 
AVG(price) AS average_price
FROM read_csv_auto('data/olist_order_items_dataset.csv');

SELECT 
seller_id,
SUM (price) AS revenue
FROM read_csv_auto('data/olist_order_items_dataset.csv')
GROUP BY seller_id
ORDER BY revenue DESC
LIMIT 10;

SELECT 
o.order_id,
o.order_status,
oi.product_id,
oi.price
FROM read_csv_auto('data/olist_order_items_dataset.csv')o
JOIN read_csv_auto('data/olist_order_items_dataset.csv')oi
ON o.order_id =oi.order_id
LIMIT 20;

SELECT 
c.customer_state,
COUNT (DISTINCT o.order_id) AS orders
FROM read_csv_auto('data/olist_orders_dataset.csv') o
JOIN read_csv_auto('data/olist_customers_dataset.csv') c
    ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY orders DESC;




""")
print(result)
