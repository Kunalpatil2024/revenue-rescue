import pandas as pd

orders = pd.read_csv (
    "data/olist_orders_dataset.csv")

customers = pd.read_csv(
    "data/olist_customers_dataset.csv"
)
items=pd.read_csv(
    "data/olist_order_items_dataset.csv"
)
products=pd.read_csv(
    "data/olist_products_dataset.csv"
)
reviews = pd.read_csv(
    "data/olist_order_reviews_dataset.csv"
)
print("data loaded successfully  ")

print ("\norders:")
print(orders.shape)

print("\ncustomers:")
print(customers.shape)

print("\nitems")
print(items.shape)

print ("\nproducts")
print(products.shape)

print("\nreviews")
print(reviews.shape)

print(
    orders.isnull().sum()

)

print (orders.dtypes
)
date_columns=[
 "order_purchase_timestamp",
 "order_approved_at",
 "order_delivered_carrier_date",
 "order_delivered_customer_date",
 "order_estimated_delivery_date"
]
for column in date_columns :
    orders[column]=pd.to_datetime(
        orders[column]
    
)
print(orders.dtypes)



orders["late_delivery"] = (
    orders["order_delivered_customer_date"]
    > orders["order_estimated_delivery_date"]
)

late_rate = (
    orders["late_delivery"].mean() * 100
)

print(
    f"Late delivery rate: {late_rate:.2f}%"
)
customer_orders = (
 orders
 .groupby("customer_id")
 ["order_id"]
 .nunique()
)