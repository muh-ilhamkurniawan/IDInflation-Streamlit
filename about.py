from enum import auto
from tkinter import Button
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
        with st.container():
            st.subheader('Dataset')
            df = pd.read_csv('data_inflasi_indonesia_clean.csv')
            csv = df.to_csv(index=False)  # Convert DataFrame to CSV format
            st.download_button(
                label="Download Dataset",
                data=csv,
                file_name="data_inflasi_indonesia_clean.csv",
                mime="text/csv", use_container_width=True
            )