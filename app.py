from enum import auto
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prediction import predict_inflation

st.set_page_config(layout="wide", initial_sidebar_state = "expanded")

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
# Set the title of the app
st.title('Visualisasi Data Inflasi Indonesia')
col1, col2 = st.columns([3,1])
with col1 :
    with st.container(border=1):
        col11, col12 = st.columns([1,2])
        with col11 :
            # st.subheader('Inflasi per Tahun')
            selected_year = st.selectbox('Inflasi per Tahun', options=df['year'].unique())
                
        # Filter dataset based on selected year
        filtered_df = df[df['year'] == selected_year]

        # Sort the filtered dataset by 'periode_inflasi' from earliest to latest
        filtered_df = filtered_df.sort_values(by='periode_inflasi')
        col13, col14 = st.columns([1,2])
        with col13 :
            with st.container(border=1):
                st.subheader('Data Inflasi')
                st.table(filtered_df[['month_name', 'data_inflasi']])
        with col14 :
            with st.container(border=1):
                st.subheader('Grafik Data Inflasi')
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.lineplot(data=filtered_df, x='month_name', y='data_inflasi', ax=ax)
                ax.set(title='Inflasi dari Waktu ke Waktu', xlabel='Bulan', ylabel='Inflasi (%)')
                st.pyplot(fig)

    with st.container(border=1):
        st.subheader("Inflation Prediction")
        # Input for month
        month = st.selectbox(
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
        year = st.number_input('Enter Year', min_value=1900, max_value=2100, step=1, value=2024)

        if st.button('Predict Inflation'):
            predicted_inflation = predict_inflation(year, month_num)
            st.write("Predicted inflation for")
            st.write(f"{month} - {year}: {predicted_inflation:.2f}%")
    with st.container(border=1):
        # Display a bar chart for average inflation by year
        st.subheader('Inflasi Rata-rata per Tahun')
        average_inflation_per_year = df.groupby('year')['data_inflasi'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=average_inflation_per_year, x='year', y='data_inflasi', ax=ax)
        ax.set(title='Inflasi Rata-rata per Tahun', xlabel='Tahun', ylabel='Inflasi (%)')
        st.pyplot(fig)

        df = pd.DataFrame(average_inflation_per_year)

    # Function to add arrows and colors based on comparison with the previous column
    def add_arrows_and_colors(df):
        df_arrows = df.copy()
        for i, col in enumerate(df.columns[1:], start=1):
            for row in range(1, len(df)):
                diff = df.iloc[row, i] - df.iloc[row-1, i]
                value = df.iloc[row, i]  # Convert to percentage
                if diff > 0:
                    df_arrows.at[row, col] = f'<span style="color:green;">{value:.2f}% ↑</span>'
                elif diff < 0:
                    df_arrows.at[row, col] = f'<span style="color:red;">{value:.2f}% ↓</span>'
                else:
                    df_arrows.at[row, col] = f'<span style="color:gray;">{value:.2f}% →</span>'
        return df_arrows

    df_with_arrows = add_arrows_and_colors(df)

with col2 :
    with st.container(border=1):
        st.subheader("Data Inflasi per Tahun")

        # Use st.write to render HTML content without index
        st.write(df_with_arrows.to_html(escape=False, index=False), unsafe_allow_html=True)
