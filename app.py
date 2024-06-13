# Begin code for Sprint 4 project
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.header('Sprint 4 Project - Vehicle Ads')

# Load and Pre-Process Data
@st.cache
def load_data(filepath):
	df_merc = df_vhs.query("price == 34900 and model == 'mercedes-benz benze sprinter 2500'")
    df_merc_2 = df_merc.query("index != 42")
    df_vhs = df_vhs.drop(index=df_merc_2.index)

	df_vhs['model_year'] = df_vhs.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median())) 
	df_vhs['odometer'] = df_vhs.groupby(['model','model_year'])['odometer'].transform(lambda x: x.fillna(x.median()))

	global_odo_median = df_vhs['odometer'].median()
	df_vhs['odometer'] = df_vhs['odometer'].fillna(global_odo_median)
	df_vhs['is_4wd'] = df_vhs['is_4wd'].fillna(0)
	df_vhs['paint_color'] = df_vhs['paint_color'].fillna('unknown')
	
	cols = ['model_year','is_4wd']
	for element in cols:
		df_vhs[element] = df_vhs[element].astype('int')

	df_vhs['date_posted'] = pd.to_datetime(df_vhs['date_posted'])
	
	df_vhs['manufacturer'] = df_vhs['model'].str.split().str[0]

	return df

# Create DF using function with all pre-processing
filepath = r'C:\Users\marlo\OneDrive\Desktop\Python_Work\Tripleten_Lessons\Sprint_4_Project\TT-Sprint_4_Project\vehicles_us.csv'
df_vhs = load_data(filepath)

# Count of models
count_of_models = df_vhs.pivot_table(index='model',
                                     values='model_year',
                                     aggfunc='count').reset_index()

count_of_models.columns = ['model','count_of_model']

# Histogram for Price across all vehicles
price_hist = px.histogram(df_vhs, x='price', title='Distribution of All Vehicle Prices')

# Box plot for price by manufacturer
price_manufacturer = px.box(df_vhs, x='manufacturer', y='price', title='Price by Manufacturer')

# Scatter of price vs mileage
scat_price_odo = px.scatter(df_vhs, x='odometer', y='price', color='condition', title='Scatterplot Distribution of Price vs Mileage by Condition')

st.plotly_chart(price_hist)
st.plotly_chart(price_manufacturer)
st.plotly_chart(scat_price_odo)
