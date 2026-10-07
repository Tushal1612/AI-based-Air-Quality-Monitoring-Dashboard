import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

np.random.seed(42)

locations = ["Surat", "Ahmedabad", "Gandhinagar", "Vadodara", "Rajkot"]
rows = []

start = datetime.now() - timedelta(days=30)

for i in range(1500):
    timestamp = start + timedelta(minutes=30 * i)
    location = np.random.choice(locations)

    # Simulated environmental readings.
    # These are prototype/synthetic values, not measurements from real sensors.
    base = np.random.normal(55, 22)

    # Add a simple rush-hour effect.
    hour = timestamp.hour
    if 7 <= hour <= 10 or 17 <= hour <= 21:
        base += np.random.normal(18, 8)

    pm25 = max(5, base)
    pm10 = max(pm25 + np.random.normal(25, 12), pm25 + 5)
    co2 = max(350, 450 + pm25 * 4 + np.random.normal(0, 100))
    temperature = 27 + 5 * np.sin((hour - 6) / 24 * 2 * np.pi) + np.random.normal(0, 2)
    humidity = np.clip(65 - (temperature - 27) * 2 + np.random.normal(0, 8), 25, 95)

    # Project-defined classes for the ML demonstration.
    # In a real system, labels should come from an approved AQI/air-quality standard.
    if pm25 < 35:
        quality = "Good"
    elif pm25 < 75:
        quality = "Moderate"
    elif pm25 < 125:
        quality = "Poor"
    else:
        quality = "Very Poor"

    rows.append([
        timestamp, location, round(pm25, 2), round(pm10, 2),
        round(co2, 2), round(temperature, 2), round(humidity, 2), quality
    ])

df = pd.DataFrame(rows, columns=[
    "timestamp", "location", "PM2.5", "PM10", "CO2",
    "temperature", "humidity", "air_quality"
])

output = Path("data/air_quality.csv")
output.parent.mkdir(exist_ok=True)
df.to_csv(output, index=False)

print(f"Created {len(df)} records at {output}")
print(df.head())
