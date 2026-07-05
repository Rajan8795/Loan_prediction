# ==========================================

# Loan Prediction Model Training

# Decision Tree Classifier

# ==========================================

import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# ==========================================

# Load Dataset

# ==========================================

df = pd.read_csv("loan_data.csv")

print("Dataset Loaded Successfully")
print(df.head())

# ==========================================

# Data Preprocessing

# ==========================================

print("\nMissing Values:")
print(df.isnull().sum())

df = df.dropna()

# ==========================================

# Features and Target

# ==========================================

X = df[['Age', 'Income', 'LoanAmount', 'CreditScore']]
y = df['Approved']

# ==========================================

# Train Test Split

# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.20,
random_state=42
)

# ==========================================

# Create Decision Tree Model

# ==========================================

model = DecisionTreeClassifier(
criterion="gini",
max_depth=5,
random_state=42
)

# ==========================================

# Train Model

# ==========================================

model.fit(X_train, y_train)

# ==========================================

# Evaluation

# ==========================================

y_pred = model.predict(X_test)

print("\nAccuracy Score:")
print(accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ==========================================

# Save Model

# ==========================================

pickle.dump(
model,
open("loan_model.pkl", "wb")
)

print("\nloan_model.pkl created successfully")
