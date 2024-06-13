# Begin code for Sprint 4 project
import streamlit as st
import pandas as pd
import plotly.express as px

st.header('Sprint 4 Project - Vehicle Ads')

# Load and Pre-Process Data
@st.cache_data
def load_data(filepath):
    df_vhs = pd.read_csv(filepath)
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
    
    df_high_price = df_vhs.query("price >= 300000") #only 1 result
    df_vhs = df_vhs.drop(index=df_high_price.index)

    return df_vhs

# Create DF using function with all pre-processing
filepath = r'C:\Users\marlo\OneDrive\Desktop\Python_Work\Tripleten_Lessons\Sprint_4_Project\TT-Sprint_4_Project\vehicles_us.csv'
df_vhs = load_data(filepath)

# Count of models
count_of_models = df_vhs.pivot_table(index='model',
                                     values='model_year',
                                     aggfunc='count').reset_index()

count_of_models.columns = ['model','count_of_model']

# Interactive Data Viewer - with checkboxes

st.sidebar.header('Filters for Raw Data:')
small_manus = st.sidebar.checkbox('Include manufacturers with less than 1000 ads')

if not small_manus:
	manu_counts = df_vhs['manufacturer'].value_counts()
	large_manus = manu_counts[manu_counts >= 1000].index #grabs manus
	df_vhs = df_vhs[df_vhs['manufacturer'].isin(large_manus)]

mileage_threshold = st.sidebar.number_input('Mileage threshold (enter value to filter for maximum mileage)', min_value=0, value=150000)
user_odos = st.sidebar.checkbox(f"Include only ads with with under {mileage_threshold} miles", value=False)

if user_odos:
	df_vhs = df_vhs[df_vhs['odometer'] < mileage_threshold]

st.subheader('Raw Data Viewer')
st.write(df_vhs)

# Histogram for Price across all vehicles
price_hist = px.histogram(df_vhs, x='price', title='Distribution of All Vehicle Prices')

# Box plot for price by manufacturer
price_manufacturer = px.box(df_vhs, x='manufacturer', y='price', title='Price by Manufacturer')

# Scatter of price vs mileage
scat_price_odo = px.scatter(df_vhs, x='odometer', y='price', color='condition', 
	title='Scatterplot Distribution of Price vs Mileage by Condition')

# Bar chart for vehicle types by manufacturers
vehicle_types = df_vhs['type'].unique().tolist() #lists the vehicle types
st.sidebar.header('Filter for Type Bar Chart:')
selected_types = st.sidebar.multiselect('Select Vehicle Types to Display', vehicle_types, default='sedan')

filtered_types = df_vhs[df_vhs['type'].isin(selected_types)]
counts_per_type = filtered_types.groupby(['manufacturer', 'type']).size().reset_index(name='count')
vehicle_type_bar = px.bar(counts_per_type, x='manufacturer', y='count', color='type', barmode='group', 
	title='Number of Ads per Vehicle Types by Manufacturer')

# Histogram for condition vs model year
conditions = df_vhs['condition'].unique().tolist()
st.sidebar.header('Filter for Condition Chart')
selected_condition = st.sidebar.selectbox('Select Vehicle Condition to Display',conditions, index=0)

	#Input to control the years shown - for fun
year_threshold = st.sidebar.number_input('Year threshold (enter the value to filter for max year)', 
	min_value=df_vhs['model_year'].min(), value=2000)
user_years = st.sidebar.checkbox(f"Implement selected maximum year to display",  value=False)

df_user_years = df_vhs.copy()
if user_years:
	df_user_years = df_user_years.query(f"model_year <= {year_threshold}")

cond_hist = px.histogram(df_user_years[df_user_years['condition'] == selected_condition], x='model_year', 
	title=f'Distribution of Model Year for Condition: {selected_condition}')


st.plotly_chart(price_hist)
st.plotly_chart(price_manufacturer)
st.plotly_chart(scat_price_odo)
st.plotly_chart(vehicle_type_bar)
st.plotly_chart(cond_hist)
