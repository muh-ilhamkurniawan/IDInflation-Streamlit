import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def show_testing() :
    # Membuat folder 'models' jika belum ada
    os.makedirs('models', exist_ok=True)

    # Load the dataset from a CSV file
    df = pd.read_csv('data_inflasi_indonesia_clean.csv')

    # Convert 'inflation_period' to datetime format
    df['inflation_period'] = pd.to_datetime(df['inflation_period'], format='%m/%d/%Y')

    # Extract year and month from 'inflation_period'
    df['year'] = df['inflation_period'].dt.year
    df['month'] = df['inflation_period'].dt.month

    # Clean 'inflation_data' to remove '%' and convert to float
    df['inflation_data'] = df['inflation_data'].str.rstrip('%').astype(float)

    # Update features and target
    X = df[['year', 'month']]
    y = df['inflation_data']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize models
    models = {
        'Linear Regression': LinearRegression(),
        'KNN': KNeighborsRegressor(),
        'Decision Tree': DecisionTreeRegressor(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(),
        'SVM': SVR()
    }

    # Train and evaluate models
    results = {}
    for name, model in models.items():
        # Train the model
        model.fit(X_train, y_train)
        
        # Predict on the test set
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        # Store results
        results[name] = {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'R²': r2
        }
        
        # Save model in 'models' folder
        model_filename = f'models/{name.lower().replace(" ", "_")}_model.pkl'
        joblib.dump(model, model_filename)

    # Display results in Streamlit
    st.title("Model Performance Comparison")

    st.write("### Metrics for Each Model:")
    for name, metrics in results.items():
        st.write(f"**{name}** - MAE: {metrics['MAE']:.4f}, MSE: {metrics['MSE']:.4f}, RMSE: {metrics['RMSE']:.4f}, R²: {metrics['R²']:.4f}")

    # Example usage of models
    def predict_inflation(model_name, year, month):
        model_filename = f'models/{model_name.lower().replace(" ", "_")}_model.pkl'
        model = joblib.load(model_filename)
        input_data = pd.DataFrame({'year': [year], 'month': [month]})
        prediction = model.predict(input_data)
        return prediction[0]

    # Example predictions
    year_to_predict = st.number_input("Select Year to Predict:", min_value=2000, max_value=2050, value=2024)
    month_to_predict = st.number_input("Select Month to Predict:", min_value=1, max_value=12, value=5)

    st.write("### Predicted Inflation:")
    for name in models.keys():
        predicted_inflation = predict_inflation(name, year_to_predict, month_to_predict)
        st.write(f"{name}: {predicted_inflation:.2f}%")

    # Plotting metrics
    labels = list(results.keys())
    mae_values = [results[label]['MAE'] for label in labels]
    mse_values = [results[label]['MSE'] for label in labels]
    rmse_values = [results[label]['RMSE'] for label in labels]
    r2_values = [results[label]['R²'] for label in labels]

    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width, mae_values, width, label='MAE')
    rects2 = ax.bar(x, mse_values, width, label='MSE')
    rects3 = ax.bar(x + width, rmse_values, width, label='RMSE')
    rects4 = ax.bar(x + 2*width, r2_values, width, label='R²')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Model')
    ax.set_ylabel('Scores')
    ax.set_title('Model Performance Comparison')
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    fig.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)
