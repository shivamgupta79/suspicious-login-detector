import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

# Load dataset
data_file = os.path.join('..','data','train.csv')  # place CSV in data folder
df = pd.read_csv(data_file)

# Features: customize according to your login schema
X = df[['failed_attempts', 'hour', 'is_new_device', 'time_since_last']].values

# Train IsolationForest
clf = IsolationForest(contamination=0.02, random_state=42)
clf.fit(X)

# Save model
os.makedirs('model', exist_ok=True)
joblib.dump(clf, 'model/isolation_forest.joblib')
print("Model trained and saved at model/isolation_forest.joblib")
