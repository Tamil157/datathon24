from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

model = None

def load_model():
    global model
    if model is None:
        model = joblib.load('path_to_your_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    load_model()
    data = request.json
    prediction = model.predict([data['features']])
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pickle

app = Flask(__name__)
CORS(app)  # Enable CORS
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return "Flask Server is running."

def save_plot(filename):
    plt.savefig(filename)
    plt.close()  # Close the plot to free up memory

@app.route('/plot', methods=['POST'])
def plot_chart():
    try:
        # Get uploaded CSV file
        csv_file = request.files['csv_file']
        
        # Save CSV file temporarily
        csv_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.csv')
        csv_file.save(csv_filename)

        attribute1 = request.form['attribute1']
        attribute2 = request.form['attribute2']

        # Read the dataset in chunks
        chunksize = 10000
        attribute1_exists, attribute2_exists = False, False
        for chunk in pd.read_csv(csv_filename, chunksize=chunksize):
            if attribute1 in chunk.columns:
                attribute1_exists = True
            if attribute2 in chunk.columns:
                attribute2_exists = True
            if attribute1_exists and attribute2_exists:
                break

        if not attribute1_exists:
            return f"Attribute '{attribute1}' not found in the dataset", 400

        if not attribute2_exists:
            return f"Attribute '{attribute2}' not found in the dataset", 400

        # Read the entire dataset
        data = pd.concat(pd.read_csv(csv_filename, chunksize=chunksize), ignore_index=True)

        if attribute1 == attribute2:
            return "Attribute 1 and Attribute 2 should be different", 400

        # Use seaborn's countplot for counting occurrences of categories
        plt.figure(figsize=(18, 10))
        sns.countplot(data=data, x=attribute1, hue=attribute2)
        plt.xlabel(attribute1)
        plt.ylabel("Count of " + attribute2)
        plt.title('Count of ' + attribute2 + ' for each ' + attribute1)
        plt.xticks(rotation=45)  # Rotate x-axis labels if needed
        plt.tight_layout()  # Adjust layout to prevent clipping of labels
        plt.legend(title=attribute2)
        
        # Save plot as image
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'plot.png')
        save_plot(image_filename)

        # Debug: Confirm file saving
        if os.path.exists(image_filename):
            print(f"Plot saved successfully at {image_filename}")

        # Remove the temporary CSV file
        os.remove(csv_filename)

        return jsonify({'plot_filename': 'plot.png'})
    except Exception as e:
        return str(e), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def get_top_unit_names(data, top_n=5):
    unitname_counts = data['UNITNAME'].value_counts().nlargest(top_n).index.tolist()
    return unitname_counts

# Data preparation for top-unit-names
csv_file_path = os.path.join(os.path.dirname(__file__), "Copy of AccidentReports.csv")
data = pd.read_csv(csv_file_path, usecols=['UNITNAME'])
top_cities = get_top_unit_names(data)

@app.route('/top-unit-names')
def top_unit_names():
    return jsonify({'top_unit_names': top_cities})

# Load models on demand
def load_model(feature):
    model_files = {
        "road_type": "road_type.pkl",
        "road_surface": "road_surface.pkl",
        "weather": "weather.pkl",  
        "light_conditions": "light.pkl",
        "pedestrian": "pedestrain.pkl",
        "severity": "severity.pkl"
    }
    with open(model_files[feature], "rb") as f:
        model = pickle.load(f)
    return model

@app.route("/predict_road_type", methods=["POST"])
def predict_road_type():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        model = load_model("road_type")
        prediction = model.predict(features)
        road_types = {
            4: 'Highway',
            3: 'Main road',
            2: 'Secondary road',
            1: 'Residential road',
            5: 'Freeway',
            6: 'Expressway'
        }
        predicted_value = prediction[0]
        if predicted_value in road_types:
            predicted = road_types[predicted_value]
            value = predicted
        return jsonify(prediction_text=value)
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route("/predict_road_surface", methods=["POST"])
def predict_road_surface():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        model = load_model("road_surface")
        prediction = model.predict(features)
        road_conditions = {
            5: "Excellent",
            4: "Very Good",
            3: "Good",
            2: "Fair",
            1: "Poor",
            -1: "Unknown or Not Applicable"
        }

        improvement_predictions = {
            "Excellent": "No immediate improvement needed. Regular maintenance recommended.",
            "Very Good": "Minimal improvements needed. Focus on preventative maintenance.",
            "Good": "Some improvements needed to maintain quality standards.",
            "Fair": "Significant improvements needed to enhance road quality.",
            "Poor": "Immediate action required to address road deterioration.",
            "Unknown or Not Applicable": "Road condition information not available."
        }

        predicted_value = prediction[0]
        if predicted_value in road_conditions:
            predicted = road_conditions[predicted_value]
            value = predicted
            if value in improvement_predictions:
                improve = improvement_predictions[value]
            return jsonify(prediction_text1=value, prediction_text11=improve)
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route("/predict_weather", methods=["POST"])
def predict_weather():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        model = load_model("weather")
        prediction = model.predict(features)
        weather = {
            1: "Clear sky",
            2: "Partly cloudy",
            3: "Cloudy",
            4: "Overcast",
            5: "Fog or mist",
            6: "Freezing fog",
            7: "Light rain shower",
            8: "Moderate or heavy rain shower",
            9: "Torrential rain shower",
            -1: "Unjudgeable"
        }

        improvement_predictions = {
            "Clear sky": "No specific infrastructure improvements needed.",
            "Partly cloudy": "Ensure proper drainage systems to handle potential rain.",
            "Cloudy": "Check and maintain road signage for visibility.",
            "Overcast": "Inspect and repair any weak structures that may be affected by wind.",
            "Fog or mist": "Install fog lights and improve road markings for visibility.",
            "Freezing fog": "Implement de-icing measures on roads and bridges.",
            "Light rain shower": "Improve road drainage and ensure proper friction on road surfaces.",
            "Moderate or heavy rain shower": "Upgrade drainage systems and reinforce flood-prone areas.",
            "Torrential rain shower": "Invest in flood prevention infrastructure and evacuation plans.",
            "Unjudgeable": "Monitor weather closely and respond accordingly."
        }
        predicted_value = prediction[0]
        if predicted_value in weather:
            predicted = weather[predicted_value]
            value = predicted
            if value in improvement_predictions:
                improve = improvement_predictions[value]
            return jsonify(prediction_text2=value, prediction_text21=improve)
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route("/predict_light_conditions", methods=["POST"])
def predict_light_conditions():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        model = load_model("light_conditions")
        prediction = model.predict(features)
        condition = {
            1: "Daylight: Street lights present",
            4: "Daylight: Street lights present and lit",
            7: "Darkness: Street lights present and lit",
            5: "Darkness: Street lights present but unlit",
            6: "Darkness: No street lighting"
        }

        improvement_predictions = {
            1: "Install additional street lights for better visibility during daylight hours.",
            4: "Ensure all street lights are functioning properly during daylight hours.",
            7: "Maintain street lights to ensure they remain lit during darkness, improving visibility.",
            5: "Repair or replace unlit street lights to improve visibility during darkness.",
            6: "Install street lighting infrastructure to illuminate areas currently lacking lighting during darkness."
        }

        predict = prediction[0]
        if predict in condition:
            value = condition[predict]
            if predict in improvement_predictions:
                improve = improvement_predictions[predict]
            return jsonify(prediction_text3=value, prediction_text31=improve)
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route("/predict_pedestrian", methods=["POST"])
def predict_pedestrian():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        model = load_model("pedestrian")
        prediction = model.predict(features)
        code = prediction[0]
        if code == 0:
            value = "Uncontrollable"
        elif code == 1:
            value = "Controlled by a human"
        elif code == 2:
            value = "Controlled by automatic signals"
        else:
            value = "Unjudgeable"
        improvement_predictions = {
            0: "Upgrade infrastructure for better control",
            1: "Implement human intervention systems",
            2: "Invest in automated control systems",
            3: "Assess and improve infrastructure"
        }
        if code in improvement_predictions:
            improve = improvement_predictions[code]
        return jsonify(prediction_text4=value, prediction_text41=improve)
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route("/predict_severity", methods=["POST"])
def predict_severity():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        model = load_model("severity")
        prediction = model.predict(features)
        severity = {
            1: "Minor",
            2: "Moderate",
            3: "Serious",
            -1: "Unjudgeable"
        }

        improvement_predictions = {
            "Minor": "Routine maintenance and repairs.",
            "Moderate": "Upgrades to infrastructure components to prevent potential issues.",
            "Serious": "Major overhaul or replacement of infrastructure components.",
            "Unjudgeable": "Further assessment needed to determine appropriate action."
        }

        predict = prediction[0]
        if predict in severity:
            value = severity[predict]
            if value in improvement_predictions:
                improve = improvement_predictions[value]
            return jsonify(prediction_text5=value, prediction_text51=improve)
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == "__main__":
    app.run(debug=True)