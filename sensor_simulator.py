"""
Optional IoT simulator.

This creates one new simulated sensor reading whenever you run it.
The dashboard itself can also simulate readings, so this file is optional.

If you later install an MQTT broker, this structure can be extended to publish
the JSON payload to a topic such as airquality/sensors/surat.
"""

import json
import random
from datetime import datetime

def generate_sensor_reading(location="Surat"):
    pm25 = round(random.uniform(10, 150), 2)
    pm10 = round(pm25 + random.uniform(10, 80), 2)
    co2 = round(random.uniform(450, 1200), 2)
    temperature = round(random.uniform(22, 38), 2)
    humidity = round(random.uniform(35, 90), 2)

    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "location": location,
        "PM2.5": pm25,
        "PM10": pm10,
        "CO2": co2,
        "temperature": temperature,
        "humidity": humidity
    }

    return payload

if __name__ == "__main__":
    print(json.dumps(generate_sensor_reading(), indent=2))
