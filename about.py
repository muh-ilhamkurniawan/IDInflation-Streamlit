import streamlit as st
import pandas as pd
import webbrowser


def show_about() :
    col1, col2 = st.columns([4,1])
    with col1 :
        with st.container():
            st.subheader('About Dashboard')
        with st.container():
            st.subheader('Model Comparison')
        with st.container():
            st.subheader('Model Evaluation Methods')
            data = {
                "Metric": [
                    "Mean Absolute Error (MAE)",
                    "Mean Squared Error (MSE)",
                    "Root Mean Squared Error (RMSE)",
                    "R² (Koefisien Determinasi)"
                ],
                "Definition": [
                    "MAE mengukur rata-rata dari selisih absolut antara nilai yang diprediksi oleh model dan nilai aktual. MAE memberi tahu seberapa besar kesalahan rata-rata yang dibuat oleh model tanpa memperhatikan tanda (positif atau negatif).",
                    "MSE adalah rata-rata dari kuadrat selisih antara nilai yang diprediksi dan nilai aktual. MSE lebih sensitif terhadap outlier.",
                    "RMSE adalah akar kuadrat dari MSE, yang mengembalikan satuan kesalahan ke skala asli variabel target.",
                    "R² mengukur seberapa besar variasi nilai aktual yang dapat dijelaskan oleh model. Nilai R² berkisar dari 0 hingga 1."
                ],
                "Formula": [
                    r"$MAE = \frac{1}{n} \sum_{i=1}^{n} \left\| y_i - \hat{y}_i \right\|$",
                    r"$MSE = \frac{1}{n} \sum_{i=1}^{n} \left( y_i - \hat{y}_i \right)^2$",
                    r"$RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} \left( y_i - \hat{y}_i \right)^2}$",
                    r"$R^2 = 1 - \frac{\sum_{i=1}^{n} \left( y_i - \hat{y}_i \right)^2}{\sum_{i=1}^{n} \left( y_i - \bar{y} \right)^2}$"
                ],
                "Interpretation": [
                    "Nilai MAE yang lebih kecil menunjukkan prediksi yang lebih akurat.",
                    "MSE memperbesar pengaruh kesalahan besar. Nilai MSE yang lebih kecil menandakan model yang lebih baik.",
                    "RMSE lebih mudah dipahami karena satuannya sama dengan variabel target. RMSE yang lebih kecil berarti prediksi yang lebih baik.",
                    "R² mendekati 1 berarti model sangat baik dalam memprediksi data. Nilai negatif menunjukkan model lebih buruk dari prediksi rata-rata."
                ]
            }

            # Create a DataFrame
            df_metrics = pd.DataFrame(data)

            # Convert DataFrame to Markdown and display
            st.markdown(df_metrics.to_markdown(index=False), unsafe_allow_html=True)


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