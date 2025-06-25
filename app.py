
import pandas as pd
import streamlit as st
import plotly.express as px

# Load dataset
df = pd.read_csv("ecommerce_sales.csv", parse_dates=["Date"])

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide", page_icon="🛍️")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1170/1170678.png", width=80)
    st.title("🛒 Sales Insights")
    st.markdown("Analyze your e-commerce performance across time, regions, and categories.")
    st.markdown("---")
    region = st.multiselect("Filter by Region", df["CustomerRegion"].unique(), default=df["CustomerRegion"].unique())
    category = st.multiselect("Filter by Category", df["Category"].unique(), default=df["Category"].unique())

df = df[(df["CustomerRegion"].isin(region)) & (df["Category"].isin(category))]

# KPIs
total_sales = df["TotalSales"].sum()
total_orders = df["OrderID"].nunique()
top_category = df.groupby("Category")["TotalSales"].sum().idxmax()
monthly_sales = df.resample("M", on="Date")["TotalSales"].sum()
monthly_growth = monthly_sales.pct_change().iloc[-1] * 100 if len(monthly_sales) > 1 else 0

# Title Section
st.markdown("## 🧾 Business Sales Overview")
st.caption("Data Storytelling Dashboard | Powered by Python + Streamlit")

# KPI Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📦 Orders", total_orders)
col3.metric("🏆 Top Category", top_category)
col4.metric("📈 Monthly Growth", f"{monthly_growth:.1f}%" if monthly_sales.shape[0] > 1 else "N/A")

# Insights
with st.expander("🧠 Key Business Insight"):
    if monthly_sales.shape[0] > 1:
        peak_month = monthly_sales.idxmax().strftime("%B %Y")
        st.write(f"📌 Sales peaked in **{peak_month}** due to promotions or seasonal effects.")
    st.write("📌 Electronics and Furniture categories consistently lead revenue.")

# Charts
sales_over_time = df.groupby("Date")["TotalSales"].sum().reset_index()
fig_line = px.line(sales_over_time, x="Date", y="TotalSales", title="📈 Sales Over Time")

top_products = df.groupby("Product")["TotalSales"].sum().nlargest(10).reset_index()
fig_bar = px.bar(top_products, x="TotalSales", y="Product", orientation="h", title="🏅 Top 10 Products")

region_sales = df.groupby("CustomerRegion")["TotalSales"].sum().reset_index()
fig_pie = px.pie(region_sales, names="CustomerRegion", values="TotalSales", title="🌍 Sales by Region")

category_sales = df.groupby(["Category", "SubCategory"])["TotalSales"].sum().reset_index()
fig_cat = px.bar(category_sales, x="Category", y="TotalSales", color="SubCategory", title="📂 Category Sales Breakdown")

# Layout
st.plotly_chart(fig_line, use_container_width=True)
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_pie, use_container_width=True)
st.plotly_chart(fig_cat, use_container_width=True)
