from pathlib import Path
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

DATA_FILE = Path("data/air_quality.csv")
MODEL_FILE = Path("model/air_quality_model.pkl")

df = pd.read_csv(DATA_FILE)

features = ["PM2.5", "PM10", "CO2", "temperature", "humidity"]
target = "air_quality"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    max_depth=10
)

model.fit(X_train, y_train)

pred = model.predict(X_test)
accuracy = accuracy_score(y_test, pred)

print(f"Model accuracy on the held-out test set: {accuracy:.2%}")
print("\nClassification report:")
print(classification_report(y_test, pred))

MODEL_FILE.parent.mkdir(exist_ok=True)
joblib.dump(model, MODEL_FILE)

print(f"\nSaved model to: {MODEL_FILE}")
