
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Revenue Rescue",
    page_icon="RR",
    layout="wide"
)

st.title("Revenue Rescue")
st.write("E-Commerce Revenue, Customer & Operations Intelligence")


# ============================================================
# LOAD DATA
# ============================================================

orders = pd.read_csv(
    "data/olist_orders_dataset.csv"
)

customers = pd.read_csv(
    "data/olist_customers_dataset.csv"
)

items = pd.read_csv(
    "data/olist_order_items_dataset.csv"
)

products = pd.read_csv(
    "data/olist_products_dataset.csv"
)

reviews = pd.read_csv(
    "data/olist_order_reviews_dataset.csv"
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

total_orders = orders["order_id"].nunique()

total_customers = customers["customer_id"].nunique()

delivered_orders = (
    orders["order_status"] == "delivered"
).sum()

delivery_rate = (
    delivered_orders / total_orders
) * 100

total_revenue = items["price"].sum()

average_order_value = (
    total_revenue / delivered_orders
)


st.header("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col2.metric(
    "Customers",
    f"{total_customers:,}"
)

col3.metric(
    "Revenue",
    f"R${total_revenue:,.0f}"
)

col4.metric(
    "Delivery Rate",
    f"{delivery_rate:.1f}%"
)


# ============================================================
# ORDERS BY STATUS
# ============================================================

status_data = (
    orders["order_status"]
    .value_counts()
    .reset_index()
)

status_data.columns = [
    "order_status",
    "count"
]

fig_status = px.bar(
    status_data,
    x="order_status",
    y="count",
    title="Orders by Status"
)

st.plotly_chart(
    fig_status,
    use_container_width=True
)


# ============================================================
# PRODUCT CATEGORY ANALYSIS
# ============================================================

items_products = items.merge(
    products[
        [
            "product_id",
            "product_category_name"
        ]
    ],
    on="product_id",
    how="left"
)

category_data = (
    items_products
    .groupby("product_category_name")
    .size()
    .reset_index(name="count")
    .sort_values(
        "count",
        ascending=False
    )
    .head(10)
)

# Remove missing category names
category_data = category_data.dropna(
    subset=["product_category_name"]
)

fig_category = px.bar(
    category_data,
    x="product_category_name",
    y="count",
    title="Top 10 Product Categories"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# ============================================================
# CUSTOMER INTELLIGENCE
# ============================================================

st.header("Customer Intelligence")

customer_orders = (
    orders
    .groupby("customer_id")["order_id"]
    .nunique()
)

repeat_customers = (
    customer_orders > 1
).sum()

one_time_customers = (
    customer_orders == 1
).sum()

repeat_rate = (
    repeat_customers /
    len(customer_orders)
) * 100


col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Customers",
    f"{len(customer_orders):,}"
)

col2.metric(
    "Repeat Customers",
    f"{repeat_customers:,}"
)

col3.metric(
    "Repeat Rate",
    f"{repeat_rate:.1f}%"
)


# ============================================================
# CUSTOMER RETENTION PROFILE
# ============================================================

customer_type = pd.DataFrame({
    "customer_type": [
        "One-time",
        "Repeat"
    ],
    "customers": [
        one_time_customers,
        repeat_customers
    ]
})


fig_customer = px.pie(
    customer_type,
    names="customer_type",
    values="customers",
    title="Customer Retention Profile"
)

st.plotly_chart(
    fig_customer,
    use_container_width=True
)


# ============================================================
# OPERATIONS INTELLIGENCE
# ============================================================

st.header("Operations Intelligence")


# Convert dates to datetime

date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )


# Calculate delivery time

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.days


# Calculate late delivery

orders["late_delivery"] = (
    orders["order_delivered_customer_date"]
    > orders["order_estimated_delivery_date"]
)


# Calculate late delivery rate

late_rate = (
    orders["late_delivery"].mean()
) * 100


# Operations KPIs

col1, col2 = st.columns(2)

col1.metric(
    "Late Delivery Rate",
    f"{late_rate:.1f}%"
)

col2.metric(
    "Average Delivery Time",
    f"{orders['delivery_days'].mean():.1f} days"
)


# ============================================================
# REVENUE LEAKAGE
# ============================================================

st.header("Revenue Leakage")

cancelled_orders = (
    orders["order_status"] == "canceled"
).sum()

unavailable_orders = (
    orders["order_status"] == "unavailable"
).sum()

late_orders = (
    orders["late_delivery"]
).sum()


col1, col2, col3 = st.columns(3)

col1.metric(
    "Cancelled Orders",
    f"{cancelled_orders:,}"
)

col2.metric(
    "Unavailable Orders",
    f"{unavailable_orders:,}"
)

col3.metric(
    "Late Orders",
    f"{late_orders:,}"
)


# ============================================================
# DELIVERY VS CUSTOMER REVIEWS
# ============================================================

st.header("Customer Experience")


order_reviews = orders.merge(
    reviews,
    on="order_id",
    how="inner"
)


review_delivery = (
    order_reviews
    .groupby("late_delivery")["review_score"]
    .mean()
    .reset_index()
)


review_delivery.columns = [
    "Late Delivery",
    "Average Review"
]


# Convert True / False to readable labels

review_delivery["Late Delivery"] = (
    review_delivery["Late Delivery"]
    .map({
        True: "Late",
        False: "On Time"
    })
)


fig_review = px.bar(
    review_delivery,
    x="Late Delivery",
    y="Average Review",
    title="Average Review Score: Late vs On-Time Orders"
)

st.plotly_chart(
    fig_review,
    use_container_width=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("Filters")


selected_status = st.sidebar.multiselect(
    "Order Status",
    options=orders["order_status"].dropna().unique(),
    default=orders["order_status"].dropna().unique()
)


filtered_orders = orders[
    orders["order_status"].isin(selected_status)
]


# ============================================================
# FILTERED ORDER SUMMARY
# ============================================================

st.header("Filtered Order Summary")

st.metric(
    "Filtered Orders",
    f"{len(filtered_orders):,}"
)


# ============================================================
# BUSINESS RECOMMENDATIONS
# ============================================================

st.header("Business Recommendations")

st.info(
    """
**1. Delivery:** Investigate categories and sellers
associated with higher late-delivery rates.

**2. Customer Retention:** Analyze one-time customers
and identify opportunities to increase repeat purchases.

**3. Revenue Protection:** Monitor cancelled and
unavailable orders as potential revenue leakage.

**4. Customer Experience:** Investigate the relationship
between delivery performance and review scores.
"""
)

