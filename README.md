# Melbourne Housing Price Classifier

This project builds a machine learning model to classify Melbourne houses as above or below the median price.

## Project Structure

- `ml_model.py`: Script for data preprocessing, model training, and evaluation
- `app.py`: FastAPI web service for deploying the model
- `templates/`: Directory containing HTML templates for the web interface
  - `index.html`: Form for inputting property data
  - `result.html`: Page displaying prediction results
- `house_price_model.joblib`: Trained model file (generated after running ml_model.py)
- `requirements.txt`: List of required Python packages

## Setup Instructions

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Train the model:
   ```
   python ml_model.py
   ```
   
   This will:
   - Load and preprocess the data
   - Create a binary classification target
   - Train an XGBoost model with hyperparameter tuning
   - Evaluate model performance with multiple metrics
   - Save the trained model as `house_price_model.joblib`

3. Run the web application:
   ```
   python app.py
   ```

4. Open your browser and go to http://127.0.0.1:8000 to access the web interface

## Model Details

- Model: XGBoost Classifier
- Target: Binary classification (above/below median house price)
- Features: Various property attributes like location, number of rooms, size, etc.
- Performance metrics: Accuracy, Precision, Recall, F1-score, ROC-AUC

## Web Interface

The web interface allows users to:
1. Input property details
2. Submit for prediction
3. View results showing if the property is likely above or below median price
4. View the probability of the prediction
