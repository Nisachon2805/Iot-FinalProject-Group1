"""
Consumer File
Listen to the subscribed topic, store data in the database, 
and feed streaming data to the real-time prediction algorithm.
"""

# Importing relevant modules
import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
import paho.mqtt.client as mqtt
import json
import requests

# Load environment variables from ".env"
load_dotenv()

# InfluxDB config
BUCKET = os.environ.get('INFLUXDB_BUCKET')
print("connecting to",os.environ.get('INFLUXDB_URL'))
client = InfluxDBClient(
    url=str(os.environ.get('INFLUXDB_URL')),
    token=str(os.environ.get('INFLUXDB_TOKEN')),
    org=os.environ.get('INFLUXDB_ORG')
)
write_api = client.write_api(write_options=ASYNCHRONOUS)
 
# MQTT broker config
MQTT_BROKER_URL = os.environ.get('MQTT_URL')
MQTT_PUBLISH_TOPIC = "@msg/data"
print("connecting to MQTT Broker", MQTT_BROKER_URL)
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.connect(MQTT_BROKER_URL,1883)

# REST API endpoint for predicting output
predict_url = os.environ.get('PREDICT_URL')
 
def on_connect(client, userdata, flags, rc, properties):
    """ The callback for when the client connects to the broker."""
    print("Connected with result code "+str(rc))
 
# Subscribe to a topic
mqttc.subscribe(MQTT_PUBLISH_TOPIC)
 
def on_message(client, userdata, msg):
    """ The callback for when a PUBLISH message is received from the server."""
    print(msg.topic+" "+str(msg.payload))

    # Write data in InfluxDB
    payload = json.loads(msg.payload)
    write_to_influxdb(payload)

    # POST data to predict the output label
    json_data = json.dumps(payload)
    post_to_predict(json_data)

# Function to post to real-time prediction endpoint
def post_to_predict(data):
    response = requests.post(predict_url, data=data)
    if response.status_code == 200:
        print("POST request successful")
    else:
        print("POST request failed!", response.status_code)

# Function to write data to InfluxDB
def write_to_influxdb(data):
    Temp = data["data"]["temp"]
    Humid = data["data"]["humid"]
    Pressure = data["data"]["pressure"]
    # format data
    point = Point("sensor_data")\
        .field("Temp", Temp)\
        .field("humid", Humid)\
        .field("pressure", Pressure)

    write_api.write(BUCKET, os.environ.get('INFLUXDB_ORG'), point)

## MQTT logic - Register callbacks and start MQTT client
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.loop_forever()
