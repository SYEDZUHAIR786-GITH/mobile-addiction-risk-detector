import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Dataset
data = {
    "screen_time": [2, 4, 6, 8, 9, 5, 7, 3, 10, 1],
    "social_media": [1, 2, 4, 6, 7, 3, 5, 1, 8, 0],
    "sleep_hours": [8, 7, 6, 5, 4, 7, 5, 8, 4, 9],
    "pickups": [30, 50, 90, 150, 180, 70, 130, 40, 200, 20],
    "risk": ["Low", "Low", "Medium", "High", "High",
             "Medium", "High", "Low", "High", "Low"]
}

df = pd.DataFrame(data)

X = df[["screen_time", "social_media", "sleep_hours", "pickups"]]
y = df["risk"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "addiction_model.pkl")

print("✅ Model trained and saved!")
