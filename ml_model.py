import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import xgboost as xgb
import joblib
import warnings
warnings.filterwarnings('ignore')

# Load the data
print("Loading the dataset...")
data = pd.read_csv('melb_data.csv')
print(f"Dataset loaded with {data.shape[0]} rows and {data.shape[1]} columns")

# Display basic information about the dataset
print("\nDataset Information:")
print(data.info())
print("\nFirst 5 rows of the dataset:")
print(data.head())
print("\nSummary statistics:")
print(data.describe())
print("\nMissing values per column:")
print(data.isnull().sum())

# Create a binary classification target (example: is house price above median?)
median_price = data['Price'].median()
data['target'] = (data['Price'] > median_price).astype(int)
print(f"\nCreated binary target variable: Whether price is above ${median_price}")
print(f"Target distribution: {data['target'].value_counts()}")

# Data preprocessing
print("\nPerforming data preprocessing...")

# Drop unnecessary columns
drop_cols = ['Address', 'SellerG', 'Date']  # Example columns to drop
data = data.drop(columns=drop_cols)

# Separate features and target
X = data.drop(columns=['target', 'Price'])  # Dropping the target and the original price
y = data['target']

# Identify categorical and numerical columns
categorical_features = X.select_dtypes(include=['object']).columns.tolist()
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"Categorical features: {categorical_features}")
print(f"Numerical features: {numerical_features}")

# Create preprocessor
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"Training set shape: {X_train.shape}, Test set shape: {X_test.shape}")

# Create XGBoost pipeline
xgb_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', xgb.XGBClassifier(random_state=42))
])

# Create parameter grid for hyperparameter tuning
param_grid = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [3, 5, 7],
    'classifier__learning_rate': [0.01, 0.1]
}

# Grid search for hyperparameter tuning
print("\nPerforming hyperparameter tuning (this may take a while)...")
grid_search = GridSearchCV(xgb_pipeline, param_grid, cv=5, scoring='f1')
grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_
print(f"Best parameters: {grid_search.best_params_}")

# Evaluate the model
print("\nEvaluating model performance...")
y_pred = best_model.predict(X_test)
y_pred_prob = best_model.predict_proba(X_test)[:, 1]

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_prob)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"ROC AUC: {roc_auc:.4f}")

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Plot ROC curve
plt.figure(figsize=(10, 6))
plt.title('Feature Importances')
sorted_idx = best_model.named_steps['classifier'].feature_importances_.argsort()
plt.barh(range(len(sorted_idx)), best_model.named_steps['classifier'].feature_importances_[sorted_idx])
plt.yticks(range(len(sorted_idx)), np.array(best_model.named_steps['preprocessor'].get_feature_names_out())[sorted_idx])
plt.tight_layout()
plt.savefig('feature_importance.png')
print("Feature importance plot saved.")

# Save the model
print("\nSaving the model...")
joblib.dump(best_model, 'house_price_model.joblib')
print("Model saved as 'house_price_model.joblib'")
