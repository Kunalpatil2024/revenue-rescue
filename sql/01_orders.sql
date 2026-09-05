select * from read_csv_auto('data/olist_orders_dataset.csv')
limit 10;
SELECT
    order_id,
    customer_id,
    order_status
FROM read_csv_auto('data/olist_orders_dataset.csv')
LIMIT 10;
SELECT COUNT(*) AS delivered_orders
FROM read_csv_auto('data/olist_orders_dataset.csv')
WHERE order_status = 'delivered';
