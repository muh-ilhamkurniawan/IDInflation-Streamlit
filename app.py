import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prediction import predict_inflation

st.set_page_config(layout="wide")

# Set the title of the app
st.title('Visualisasi Data Inflasi Indonesia')

# Load the dataset from a CSV file
df = pd.read_csv('data_inflasi_indonesia_clean.csv')

# Convert 'periode_inflasi' to datetime format
df['periode_inflasi'] = pd.to_datetime(df['periode_inflasi'], format='%m/%d/%Y')

# Extract year and month for filtering
df['year'] = df['periode_inflasi'].dt.year
df['month'] = df['periode_inflasi'].dt.month

# Clean 'data_inflasi' to remove '%' and convert to float
df['data_inflasi'] = df['data_inflasi'].str.rstrip('%').astype(float)

# Define month names in Indonesian
month_names = {
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni',
    7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
}

# Map month numbers to month names
df['month_name'] = df['month'].map(month_names)

# Sidebar for year filter
st.sidebar.header('Filter Data')
selected_year = st.sidebar.selectbox('Pilih Tahun', options=df['year'].unique())

st.sidebar.header("Inflation Prediction")

# Input for month
month = st.sidebar.selectbox(
    'Select Month',
    ['January', 'February', 'March', 'April', 'May', 'June', 
     'July', 'August', 'September', 'October', 'November', 'December']
)

# Convert month name to number
month_to_num = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}
month_num = month_to_num[month]

# Input for year
year = st.sidebar.number_input('Enter Year', min_value=1900, max_value=2100, step=1, value=2024)

if st.sidebar.button('Predict Inflation'):
    predicted_inflation = predict_inflation(year, month_num)
    st.sidebar.write("Predicted inflation for")
    st.sidebar.write(f"{month} - {year}: {predicted_inflation:.2f}%")

# Filter dataset based on selected year
filtered_df = df[df['year'] == selected_year]

# Sort the filtered dataset by 'periode_inflasi' from earliest to latest
filtered_df = filtered_df.sort_values(by='periode_inflasi')

# Create two columns for layout
col1, col2 = st.columns([2,3])

with col1:
    # Display the dataset with month names
    st.subheader('Data Inflasi')
    # st.table(filtered_df[['month_name', 'data_inflasi']])
    # st.dataframe(filtered_df[['month_name', 'data_inflasi']], hide_index=True)
    st.markdown(filtered_df[['month_name', 'data_inflasi']].style.hide(axis="index").to_html(), unsafe_allow_html=True)

with col2:
    # Display a line chart for data_inflasi over time
    st.subheader('Grafik Data Inflasi')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=filtered_df, x='month_name', y='data_inflasi', ax=ax)
    ax.set(title='Inflasi dari Waktu ke Waktu', xlabel='Bulan', ylabel='Inflasi (%)')
    st.pyplot(fig)

# Display a bar chart for average inflation by year
st.subheader('Inflasi Rata-rata per Tahun')
average_inflation_per_year = df.groupby('year')['data_inflasi'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=average_inflation_per_year, x='year', y='data_inflasi', ax=ax)
ax.set(title='Inflasi Rata-rata per Tahun', xlabel='Tahun', ylabel='Inflasi (%)')
st.pyplot(fig)
