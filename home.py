from enum import auto
from tkinter import Button
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prediction import predict_inflation


def show_home() :
    # Load the dataset from a CSV file
    df = pd.read_csv('data_inflasi_indonesia_clean.csv')

    # Convert 'inflation_period' column to datetime format
    df['inflation_period'] = pd.to_datetime(df['inflation_period'], format='%m/%d/%Y')

    # Extract year and month for filtering purposes
    df['year'] = df['inflation_period'].dt.year
    df['month'] = df['inflation_period'].dt.month

    # Clean 'inflation_data' column by removing '%' and converting to float
    df['inflation_data'] = df['inflation_data'].str.rstrip('%').astype(float)

    # Define month names in English for display purposes
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    # Map month numbers to month names
    df['month_name'] = df['month'].map(month_names)

    # Layout configuration with two columns
    col1, col2 = st.columns([4, 1])

    with col1:
        # First container for year selection and data display
        with st.container():
            col11, col12 = st.columns([1, 2])
            
            with col11:
                # Dropdown for selecting year
                st.markdown(
                    """
                    <style>
                    div[data-testid="stSelectbox"] > label {display: none;}  /* Menghilangkan label */
                    div[data-testid="stSelectbox"] > div {margin-top: -16px;} /* Mengurangi jarak atas */
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                selected_year = st.selectbox('', options=df['year'].unique())
            with col12:
                with st.popover("Inflation Prediction"):
                    # Third container for inflation prediction
                    with st.container():
                        st.subheader("Inflation Prediction")

                        # Input for selecting month
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

                        # Input for entering year
                        year = st.number_input('Enter Year', min_value=1900, max_value=2100, step=1, value=2024)

                        # Predict inflation based on the selected month and year
                        if st.button('Predict Inflation'):
                            predicted_inflation = predict_inflation(year, month_num)
                            st.write("Predicted inflation for")
                            st.write(f"{month} - {year}: {predicted_inflation:.2f}%")

                    
            # Filter dataset based on selected year
            filtered_df = df[df['year'] == selected_year]

            # Sort the filtered dataset by 'inflation_period' from earliest to latest
            filtered_df = filtered_df.sort_values(by='inflation_period')

            # Second container for displaying data and graph
            col13, col14 = st.columns([1, 3])
            
            with col13:
                # Display the filtered data in a table
                with st.container():
                    st.subheader('Data')
                    renamed_df = filtered_df[['month_name', 'inflation_data']].rename(columns={
                        'month_name': 'Month',
                        'inflation_data': 'Inflation Rate (%)'
                    })
                    renamed_df['Inflation Rate (%)'] = renamed_df['Inflation Rate (%)'].apply(lambda x: f"{x:.2f}")
                    st.table(renamed_df)
            
            with col14:
                # Display a line chart of the filtered data
                with st.container():
                    st.subheader('Visualization')
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.lineplot(data=filtered_df, x='month_name', y='inflation_data', ax=ax)
                    ax.set(title='Inflation Over Time', xlabel='Month', ylabel='Inflation (%)')
                    # Set rotation for x-axis labels
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                    st.pyplot(fig)


        # Fourth container for average inflation per year bar chart
        with st.container():
            st.subheader('Average Inflation per Year')

            # Calculate the average inflation per year
            average_inflation_per_year = df.groupby('year')['inflation_data'].mean().reset_index()

            # Display a bar chart for average inflation per year
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=average_inflation_per_year, x='year', y='inflation_data', ax=ax)
            ax.set(title='Average Inflation per Year', xlabel='Year', ylabel='Inflation (%)')

            # Set rotation for x-axis labels
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

            st.pyplot(fig)

            # Convert the DataFrame to display arrows and colors
            df = pd.DataFrame(average_inflation_per_year)

        # Function to add arrows and colors based on comparison with the previous column
        def add_arrows_and_colors(df):
            df_arrows = df.copy()
            for i, col in enumerate(df.columns[1:], start=1):
                for row in range(1, len(df)):
                    diff = df.iloc[row, i] - df.iloc[row-1, i]
                    value = df.iloc[row, i]
                    if diff > 0:
                        df_arrows.at[row, col] = f'<span style="color:red;">{value:.2f}% ↑</span>'
                    elif diff < 0:
                        df_arrows.at[row, col] = f'<span style="color:green;">{value:.2f}% ↓</span>'
                    else:
                        df_arrows.at[row, col] = f'<span style="color:gray;">{value:.2f}% →</span>'
            return df_arrows

        # Apply the arrow and color function to the DataFrame
        df_with_arrows = add_arrows_and_colors(df)

    with col2:
        # Container for displaying the formatted DataFrame with arrows
        with st.container():
            st.subheader("Inflation Data by Year")

            # Use st.write to render HTML content without index
            renamed_df_with_arrows = df_with_arrows[['year', 'inflation_data']].rename(columns={
                        'year': 'Year',
                        'inflation_data': 'Inflation Rate (%)'
                    })
            # Menambahkan gaya CSS untuk membuat tabel menjadi full-width
            st.markdown(
                """
                <style>
                table {
                    width: 100%;
                    text-align: center;
                }
                th {
                    text-align: center !important;
                }
                </style>
                """, unsafe_allow_html=True
            )

            # Menampilkan tabel dengan full-width
            st.write(renamed_df_with_arrows.to_html(escape=False, index=False), unsafe_allow_html=True)

