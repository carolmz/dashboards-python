import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=100),
    "Sales": np.random.randint(100, 500, size=100),
    "Region": np.random.choice(["North", "South", "East", "West"], size=100)
})

st.title("Sales Dashboard with Filters")

# Date filter widget
start_date, end_date = st.date_input("Select date range", [df['Date'].min(), df['Date'].max()])

# Region filter widget
regions = st.multiselect("Select regions", options=df["Region"].unique(), default=df["Region"].unique())

# Filter dataframe based on selections
filtered_df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]
filtered_df = filtered_df[filtered_df["Region"].isin(regions)]

# Create figure based on filtered data
fig = px.line(filtered_df, x="Date", y="Sales", color="Region", title="Sales Over Time by Region")

st.plotly_chart(fig)