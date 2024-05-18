import numpy as np
from flask import Flask, request, jsonify
import pickle   
import os
import pandas as pd
from collections import defaultdict

app = Flask(__name__)
csv_file_path = os.path.join(os.path.dirname(__file__), 'CopyofAccidentReports.csv')
data = pd.read_csv(csv_file_path)
from collections import defaultdict
unitname_counts = defaultdict(list)
for unitname in data['UNITNAME']:
    unitname_counts[unitname].append(1)
unitname_counts = {key: sum(value) for key, value in unitname_counts.items()}

top = []
for i in range(5):
    values = unitname_counts.values()
    a = max(values)
    for key, val in unitname_counts.items():
            if val == a:
                top.append(key)
                break
    unitname_counts.pop(key)

from flask import Flask, jsonify

app = Flask(__name__)

top_cities = []
for i in top:
    top_cities.append(i)

@app.route('/top-unit-names')
def top_unit_names():
    return jsonify({'top_unit_names': top_cities})

# Load models
models = {}
model_files = {
    "road_type": "Road_type.pkl",
    "road_surface": "road_surface.pkl",
    "weather": "weather.pkl",  
    "light_conditions": "light.pkl",
    "pedestrian": "pedestrain.pkl",
    "severity": "severity.pkl"
}

for feature, file in model_files.items():
    with open(file, "rb") as f:
        models[feature] = pickle.load(f)

@app.route("/")
def home():
    return "Flask Server is running."

@app.route("/predict_road_type", methods=["POST"])
def predict_road_type():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        prediction = models["road_type"].predict(features)
        road_types = {
        4: 'Highway',
        3: 'Main road',
        2: 'Secondary road',
        1: 'Residential road',
        5: 'Freeway',
        6: 'Expressway'}
        predicted_value = prediction[0]
        if predicted_value in road_types:
            predicted = road_types[predicted_value]
            value=predicted
        return jsonify(prediction_text = value)
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route("/predict_road_surface", methods=["POST"])
def predict_road_surface():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        prediction = models["road_surface"].predict(features)
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
        "Unknown or Not Applicable": "Road condition information not available."}
    
        predicted_value = prediction[0]
        if predicted_value in road_conditions:
            predicted = road_conditions[predicted_value]
            value=predicted
            if value in improvement_predictions:
                improve = improvement_predictions[value]
            return jsonify(prediction_text1= value,prediction_text11= improve)
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route("/predict_weather", methods=["POST"])
def predict_weather():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        prediction = models["weather"].predict(features)
        weather ={    
        1: "Clear sky",
        2: "Partly cloudy",
        3: "Cloudy",
        4: "Overcast",
        5: "Fog or mist",
        6: "Freezing fog",
        7: "Light rain shower",
        8: "Moderate or heavy rain shower",
        9: "Torrential rain shower",
        -1: "Unjudgeable"}

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
        "Unjudgeable": "Monitor weather closely and respond accordingly."}
        predicted_value = prediction[0]
        if predicted_value in weather:
            predicted = weather[predicted_value]
            value=predicted
            if value in improvement_predictions:
                improve = improvement_predictions[value]
        return jsonify(prediction_text2 = value,prediction_text21 = improve)
    except Exception as e:
        return jsonify(error=str(e)), 400
    
@app.route("/predict_light_conditions", methods=["POST"])
def predict_light_conditions():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        prediction = models["light_conditions"].predict(features)
        condition = {
        1: "Daylight: Street lights present",
        4: "Daylight: Street lights present and lit",
        7: "Darkness: Street lights present and lit",
        5: "Darkness: Street lights present but unlit",
        6: "Darkness: No street lighting" }

        improvement_predictions =  {
        1: "Install additional street lights for better visibility during daylight hours.",
        4: "Ensure all street lights are functioning properly during daylight hours.",
        7: "Maintain street lights to ensure they remain lit during darkness, improving visibility.",
        5: "Repair or replace unlit street lights to improve visibility during darkness.",
        6: "Install street lighting infrastructure to illuminate areas currently lacking lighting during darkness." }

        predict = prediction[0]
        if predict in condition:
            value = condition[predict]
            if predict in improvement_predictions:
                improve = improvement_predictions[predict]
            return jsonify(prediction_text3=value, prediction_text31= improve)
    except Exception as e:
        return jsonify(error=str(e)), 400
@app.route("/predict_pedestrian", methods=["POST"])
def predict_pedestrian():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        prediction = models["pedestrian"].predict(features)
        code=prediction[0]
        if code == 0:
            value= "Uncontrollable"
        elif code == 1:
            value = "Controlled by a human"
        elif code == 2:
            value = "Controlled by automatic signals"
        else:
            value =  "Unjudgeable"
        improvement_predictions = {
            0: "Upgrade infrastructure for better control",
            1: "Implement human intervention systems",
            2: "Invest in automated control systems",
            3: "Assess and improve infrastructure",
        }
        if code in improvement_predictions:
            improve = improvement_predictions[code]
        return jsonify(prediction_text4=value , prediction_text41=improve)
    except Exception as e:
        return jsonify(error=str(e)), 400
    
@app.route("/predict_severity", methods=["POST"])
def predict_severity():
    try:
        data = request.get_json()
        float_features = [float(x) for x in data.values()]
        features = np.array(float_features).reshape(1, -1)
        prediction = models["severity"].predict(features)
        severity= {
        1: "Minor",
        2: "Moderate",
        3: "Serious",
        -1: "Unjudgeable"}

        improvement_predictions = {
        "Minor": "Routine maintenance and repairs.",
        "Moderate": "Upgrades to infrastructure components to prevent potential issues.",
        "Serious": "Major overhaul or replacement of infrastructure components.",
        "Unjudgeable": "Further assessment needed to determine appropriate action." }

        predict = prediction[0]
        if predict in severity:
            value = severity[predict]
            if value in improvement_predictions:
                improve = improvement_predictions[value]
            return jsonify(prediction_text5 = value, prediction_text51 = improve)
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == "__main__":
    app.run(debug=True)
