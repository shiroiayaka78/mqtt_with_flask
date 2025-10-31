from flask import Flask, jsonify, send_from_directory
import paho.mqtt.client as mqtt
import json
from db_config import get_db_connection
import os

app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")

db = get_db_connection()
cursor = db.cursor()

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    query = "INSERT INTO sensor_data (id, sensor_type, value, timestamp) VALUES (%s, %s, %s, %s)"
    values = (data["id"], data["sensor_type"], data["value"], data["timestamp"])
    cursor.execute(query, values)
    db.commit()
    print("Data inserted:", values)

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883)
mqtt_client.subscribe("sensor/data")
mqtt_client.loop_start()


# Routing
@app.route('/')
def home():
    return send_from_directory('../frontend', 'index.html') # Automatically direct the page to index.html

# Grab data from db
@app.route('/data')
def get_data():
    cursor.execute("SELECT sensor_type, value, timestamp FROM sensor_data ORDER BY timestamp")
    rows = cursor.fetchall()
    result = [{"sensor_type": r[0], "value": r[1], "timestamp": r[2].strftime("%Y-%m-%d %H:%M:%S")} for r in rows]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
