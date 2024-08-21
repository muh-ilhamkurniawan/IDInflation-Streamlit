from enum import auto
from tkinter import Button
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import webbrowser
from prediction import predict_inflation


def show_about() :
    col1, col2 = st.columns([4,1])
    with col1 :
        with st.container():
            st.subheader('About Dashboard')
        with st.container():
            st.subheader('Model Performance Comparison')
    with col2 :
        with st.container():
            st.subheader('About Me')
            st.write("Hi there 👋 I am Muhammad Ilham Kurniawan")
            if st.button('My Github', use_container_width=True):
                webbrowser.open_new_tab("https://github.com/muh-ilhamkurniawan")
        with st.container():
            st.subheader('Dataset')
            df = pd.read_csv('data_inflasi_indonesia_clean.csv')
            csv = df.to_csv(index=False)  # Convert DataFrame to CSV format
            st.download_button(
                label="Download Dataset",
                data=csv,
                file_name="data_inflasi_indonesia_clean.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.markdown("<h6 style='text-align: center; margin-top: -10px; margin-bottom: -10px;'>or</h6>", unsafe_allow_html=True)
            if st.button('Go to Kaggle Dataset', use_container_width=True):
                webbrowser.open_new_tab("https://www.kaggle.com/datasets/mikailnabiljordan/inflation-in-indonesia-from-2002-to-2024")