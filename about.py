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