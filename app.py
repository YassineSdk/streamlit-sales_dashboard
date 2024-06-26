import pandas as pd 
import plotly.express as px 
import streamlit as st



st.set_page_config(page_title="Sales Dashboard",
                   page_icon =":bar_chart:" ,
                   layout="wide")


df = pd.read_csv('supermarkt_sales.csv')

df["hour"] = pd.to_datetime(df['Time'],format="%H:%M").dt.hour


st.sidebar.header(" Please filter here :  ")
city = st.sidebar.multiselect(
    "select the City : ",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "select the customer type : ",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "select the  Gender  : ",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

product_line = st.sidebar.multiselect(
    "select the product line  : ",
    options=df["Product line"].unique(),
    default=df["Product line"].unique()
)

df_selection = df.query(
    "`City` == @city & `Customer_type` == @customer_type & `Gender` == @gender & `Product line` == @product_line"
)

st.markdown("---")

st.title(":bar_chart: Sales Dashboard")
st.markdown('#')

total_sales =int(df_selection["Total"].sum())
avrage_ranting = round(df_selection["Rating"].mean())
total_profit = int(df_selection["gross income"].sum())
star_rating =":star:" * int(round(avrage_ranting,0))

st.markdown("---")

left_column,middle_column,right_column = st.columns(3)

with left_column:
    st.subheader(" TOTAL SALES ")
    st.subheader(f"   {total_sales} $")

with middle_column:
    st.subheader(" AVERAGE RATING  ")
    st.subheader(f"   {avrage_ranting}{star_rating}")
with right_column:
    st.subheader(" TOTAL PROFIT ")
    st.subheader(f"   {total_profit} $")   

st.markdown("---")

sales_by_product = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

fig_products_sales = px.bar(
    sales_by_product,
    x="Total",
    y=sales_by_product.index,
    orientation="h",
    title="<b>Sales by Product Line </b>",
    color_discrete_sequence = ['#0083B8'] * len(sales_by_product),
    template="plotly_white",
)

fig_products_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

sales_customer = df_selection.groupby(by=["Customer_type"]).sum()[["Total"]].sort_values(by="Total")
color_sequence = px.colors.qualitative.Pastel
fig_customer_sales = px.pie(
    sales_customer,
    values="Total",
    names=sales_customer.index,
    title="<b>Sales by customer type </b> ",
    color_discrete_sequence=color_sequence,
    template="plotly_white",
)

sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b> hourly sales  </b>",
    color_discrete_sequence=color_sequence,
    template="plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig_hourly_sales)
st.markdown("---")
left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_products_sales,use_container_width=True)
right_column.plotly_chart(fig_customer_sales,use_container_width=True)
