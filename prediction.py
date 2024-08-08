import pandas as pd
import joblib

# Function to predict inflation based on year and month
def predict_inflation(year, month):
    # Load the model
    loaded_rf_model = joblib.load('random_forest_model.pkl')

    input_data = pd.DataFrame({'year': [year], 'month': [month]})
    prediction = loaded_rf_model.predict(input_data)
    return prediction[0]