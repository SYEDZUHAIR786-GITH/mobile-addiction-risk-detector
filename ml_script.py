# ===============================
# Mobile Addiction ML Script
# ===============================

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# -------------------------------
# 1. Create dataset
# -------------------------------
data = {
    "screen_time": [2, 4, 6, 8, 9, 5, 7, 3, 10, 1],
    "social_media": [1, 2, 4, 6, 7, 3, 5, 1, 8, 0],
    "sleep_hours": [8, 7, 6, 5, 4, 7, 5, 8, 4, 9],
    "pickups": [30, 50, 90, 150, 180, 70, 130, 40, 200, 20],
    "risk": ["Low", "Low", "Medium", "High", "High",
             "Medium", "High", "Low", "High", "Low"]
}

df = pd.DataFrame(data)

# -------------------------------
# 2. Split input & output
# -------------------------------
X = df[["screen_time", "social_media", "sleep_hours", "pickups"]]
y = df["risk"]

# -------------------------------
# 3. Train ML model
# -------------------------------
model = DecisionTreeClassifier()
model.fit(X, y)

# -------------------------------
# 4. Take user input
# -------------------------------
print("\n📱 Mobile Addiction Risk Check 📱\n")

screen_time = int(input("Daily screen time (hours): "))
social_media = int(input("Social media usage (hours): "))
sleep_hours = int(input("Sleep hours per day: "))
pickups = int(input("Phone pickups per day: "))

# -------------------------------
# 5. Predict
# -------------------------------
prediction = model.predict([[screen_time, social_media, sleep_hours, pickups]])

print("\nPredicted Addiction Risk:", prediction[0])
