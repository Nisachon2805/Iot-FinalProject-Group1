"""
Real-Time prediction
Retrieve streaming data from the consumer and predict the number 
of people inside the room. Utilize Flask, a simple REST API server, 
as the endpoint for data feeding.
"""

# Importing relevant modules
import joblib
import pandas as pd
from flask import Flask, request, jsonify
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
import json

# Load the trained model
trained_model = joblib.load('trained_model.pkl')

# Get the values fron InfluxDB
INFLUXDB_USERNAME="heart0388"
INFLUXDB_PASSWORD="heart0388"
INFLUXDB_TOKEN="TzPh2XmRUCxtsayLqtD_D2zKubHT_66j7JQ_L6Cy0MbMSJkUEOCw7cBsEBSQR2Lwpj2Ymq552FDJXrPRoVPvZA=="
INFLUXDB_ORG="heart0388"          
INFLUXDB_BUCKET="model" 
INFLUXDB_URL="https://iot-group1-service1.iotcloudserve.net/"


# InfluxDB config
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
#Instantiate the client. The InfluxDBClient object takes three named parameters: url, org, and token. Pass in the named parameters.
#BUCKET = os.environ.get('INFLUXDB_BUCKET')
client = influxdb_client.InfluxDBClient(
   url=INFLUXDB_URL,
   token=INFLUXDB_TOKEN,
   org=INFLUXDB_ORG
)
write_api = client.write_api(write_options=ASYNCHRONOUS)
# Create simple REST API server
app = Flask(__name__)

# Default route: check if model is available.
@app.route('/')
def check_model():
    if trained_model:
        return "Model is ready for prediction"
    return "Server is running but something wrongs with the model"

# Initialize a buffer to store the last 5 data points
data_buffer = []

# Define a function to update the buffer with the latest data point
def update_buffer(data_point):
    data_buffer.append(data_point)
    if len(data_buffer) > 5:
        data_buffer.pop(0)

def is_numeric(value):
    """
    Check if a value is numeric.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

# Predict route: predict the output from streaming data
@app.route('/predict', methods=['POST'])
def predict():
    try:
        
        # Get JSON text from the request and decode it
        json_text = request.data.decode('utf-8')
        # Convert JSON text to JSON object
        json_data = json.loads(json_text)
        print('jsondata')
        print(json_data)

        # Update the buffer with the latest data point
        update_buffer(json_data["temp"])
        print('databuffer')
        print(data_buffer)
        if all(is_numeric(x) for x in data_buffer):
            # If we have collected 5 data points, proceed with prediction
            if len(data_buffer) == 5:
             # Create DataFrame from the last 5 data points
                feature_sample = pd.DataFrame(data_buffer)
                print('featuresample')
                print(feature_sample)

                column_names = ['temp_1', 'temp_2', 'temp_3', 'temp_4', 'temp_5']
                data_buffer_numeric = [float(x) for x in data_buffer]  # Assuming data_buffer contains floats
                # Create DataFrame from the last 5 data points
                feature_sample = pd.DataFrame([data_buffer_numeric], columns=column_names)
                print('featuresample')
                print(feature_sample)
                print('only5databuffer')
                print(data_buffer)
                predict_sample = trained_model.predict(feature_sample)
                print('predict_sample')
                print(predict_sample)
        # Assign the true label and predicted label into Point
                point = Point("predict_value")\
                    .field("feature_sample", feature_sample)\
                    .field("predict_sample", predict_sample[0])
        
        # Write that Point into database
        #write_api.write(INFLUXDB_BUCKET, os.environ.get('INFLUXDB_ORG'), point)
        #write_api.write(INFLUXDB_BUCKET,('INFLUXDB_ORG'), point)
                write_api.write(bucket =INFLUXDB_BUCKET,org='INFLUXDB_ORG', record= point)
                return jsonify({"feature_sample": feature_sample, "predict_sample": int(predict_sample[0])}), 200
            else:
                return "Insufficient data points for prediction", 400
        else:
            return "Data points are not numeric", 400
        
    
    #except:
        # Something error with data or model
        #return "Recheck the data", 400

    except KeyError as e:
        # Handle missing key error
        return jsonify({"error_message": f"Missing '{e.args[0]}' key in JSON data", "json_data": json_data}), 400
    
    except ValueError:
        # Handle value error (e.g., invalid JSON)
        return jsonify({"error_message": "Invalid JSON data", "json_data": json_data}), 400
    
    except Exception as e:
        # Catch any other exceptions
        return jsonify({"error_message": f"An error occurred: {str(e)}", "json_data": json_data}), 400
    
if __name__ == '__main__':
    app.run()