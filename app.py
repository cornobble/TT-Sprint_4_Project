# Begin code for Sprint 4 project
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.header('Sprint 4 Project - Vehicle Ads')

# Histogram for Price across all vehicles
price_hist = px.histogram(df_vhs, x='price', title='Distribution of All Vehicle Prices')

# Box plot for price by manufacturer
price_manufacturer = px.box(df_vhs, x='manufacturer', y='price', title='Price by Manufacturer')

# Scatter of price vs mileage
scat_price_odo = px.scatter(df_vhs, x='odometer', y='price', color='condition', title='Scatterplot Distribution of Price vs Mileage by Condition')

st.plotly_chart(price_hist)
st.plotly_chart(price_manufacturer)
st.plotly_chart(scat_price_odo)
