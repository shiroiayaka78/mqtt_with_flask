import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.loop_start()

sensor_types = ["temperature", "humidity", "pressure"]

for i in range(30):
    data = {
        "sensor_type": random.choice(sensor_types),
        "value": round(random.uniform(20.0, 100.0), 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    client.publish("sensor/data", json.dumps(data))
    print("📤 Published:", data)
    time.sleep(1)

client.loop_stop()
client.disconnect()