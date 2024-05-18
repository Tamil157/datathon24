import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle


# Create flask app
flask_app = Flask(__name__)

# Load models
models = {}
model_files = {
    "road_type": "Road_type.pkl",
    "road_surface": "road_surface.pkl",
    "weather": "whether.pkl",  
    "light_conditions": "light.pkl",
    "pedestrian": "pedestrain.pkl",
    "severity": "severity.pkl"
}

for feature, file in model_files.items():
    models[feature] = pickle.load(open(file, "rb"))

# Routes for home page and predictions
@flask_app.route("/")
def Home():
    return render_template("final.html")

@flask_app.route("/predict_road_type", methods=["POST"])
def predict_road_type():
    # Extracting float features from form inputs
    float_features = []
    for key in ['road_type1', 'road_type2', 'road_no1', 'road_no2', 'road_no3', 'road_no4']:
        value = request.form.get(key)
        
        if value is None or value == '':
            float_features.append(0.0)  # If the value is empty or not provided, replace it with 0.0
        else:
            try:
                float_features.append(float(value))  # Convert value to float
            except ValueError:
                return render_template("final.html", prediction_text="Invalid input: '{}' is not a valid number.".format(value))

    # Making prediction
    prediction = models["road_type"].predict([float_features])
    

    # Mapping prediction to road types
    road_types = {
        4: 'Highway',
        3: 'Main road',
        2: 'Secondary road',
        1: 'Residential road',
        5: 'Freeway',
        6: 'Expressway'
    }

    # Get the predicted road type
    predicted_road_type = road_types.get(prediction[0], "Unknown")
    
    # Rendering prediction
    return render_template("final.html", prediction_text="The predicted road type: {}".format( predicted_road_type))

@flask_app.route("/predict_road_surface", methods=["POST"])
def predict_road_surface():
    # Extracting float features from form inputs
    float_features = [float(request.form.get(feature)) for feature in ['road_texture', 'road_material', 'road_condition', 'potholes', 'cracks', 'urban_or_rural_area']]
    
    # Creating a numpy array from the float features
    features = np.array(float_features).reshape(1, -1)
    
    # Making prediction
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
    "Unknown or Not Applicable": "Road condition information not available."
}
    
    

    predicted_value = prediction[0]
    if predicted_value in road_conditions:
        predicted = road_conditions[predicted_value]
        value=predicted
        if value in improvement_predictions:
            improve = improvement_predictions[value]

       
    
    # Rendering prediction
    return render_template("final.html", prediction_text1="The predicted road surface: {}".format(value)+" Improvement to be done: {}".format(improve))

@flask_app.route("/predict_weather", methods=["POST"])
def predict_weather():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = models["weather"].predict(features)  # Corrected model key here
    weather= {
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
        value=predicted
        if value in improvement_predictions:
            improve = improvement_predictions[value]
        
    return render_template("final.html", prediction_text2="The predicted weather: {}".format(value)+" Improvement to be done: {}".format(improve))

@flask_app.route("/predict_light_conditions", methods=["POST"])
def predict_light_conditions():
    # Extracting values from the form and converting them to float
    float_features = [float(request.form['light_intensity']),
                      float(request.form['sun_visibility']),
                      float(request.form['street_lights']),
                      float(request.form['traffic_lights']),
                      float(request.form['time_of_day']),
                      float(request.form['additional_feature'])]  # Adjusted for the additional input field

    # Converting features to numpy array
    features = np.array(float_features).reshape(1, -1)  # Reshape for prediction

    # Making prediction
    prediction = models["light_conditions"].predict(features)
    condition= {
        1: "Daylight: Street lights present",
        4: "Daylight: Street lights present and lit",
        7: "Darkness: Street lights present and lit",
        5: "Darkness: Street lights present but unlit",
        6: "Darkness: No street lighting"
    }
    improvement_predictions =  {
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
        

    # Returning the prediction to the template
    return render_template("final.html", prediction_text3="The predicted light conditions: {}".format(value)+" Improvement to be done: {}".format(improve))


@flask_app.route("/predict_pedestrian", methods=["POST"])
def predict_pedestrian():
    # Extracting values from the form and converting them to float
    float_features = [float(request.form['road_condition']),
                      float(request.form['num_lanes']),
                      float(request.form['surface_type']),
                      float(request.form['road_markings']),
                      float(request.form['road_signs']),
                      float(request.form['urban_or_rural_area'])]

    # Converting features to numpy array
    features = np.array(float_features)

    # Making prediction
    prediction = models["pedestrian"].predict([features])
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

    # Returning the prediction to the template
    return render_template("final.html", prediction_text4="The predicted pedestrian: {}".format(value)+" Improvement to be done: {}".format(improve))




@flask_app.route("/predict_severity", methods=["POST"])
def predict_severity():
    float_features = [int(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = models["severity"].predict(features)
    severity= {
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
    


    return render_template("final.html", prediction_text5="The predicted severity: {}".format(value)+" Improvement to be done: {}".format(improve))

if __name__ == "__main__":
    flask_app.run(debug=True)




