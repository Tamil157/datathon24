from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

def save_plot(filename):
    plt.savefig(filename)

@app.route('/plot', methods=['POST'])
def plot_chart():
    try:
        # Get uploaded CSV file
        csv_file = request.files['csv_file']
        
        # Save CSV file temporarily
        csv_filename = 'temp.csv'
        csv_file.save(csv_filename)

        attribute1 = request.form['attribute1']
        attribute2 = request.form['attribute2']

        # Read the entire dataset
        data = pd.read_csv(csv_filename)
        
        if attribute1 == attribute2:
            return "Attribute 1 and Attribute 2 should be different"

        # Check if the attributes exist in the dataset
        if attribute1 not in data.columns:
            return f"Attribute '{attribute1}' not found in the dataset"

        if attribute2 not in data.columns:
            return f"Attribute '{attribute2}' not found in the dataset"

        # Use seaborn's countplot for counting occurrences of categories
        plt.figure(figsize=(18, 10))
        sns.countplot(data=data, x=attribute1, hue=attribute2)
        plt.xlabel(attribute1)
        plt.ylabel("Count of "+ attribute2)
        plt.title('Count of ' + attribute2 + ' for each ' + attribute1)
        plt.xticks(rotation=45)  # Rotate x-axis labels if needed
        plt.tight_layout()  # Adjust layout to prevent clipping of labels
        plt.legend(title=attribute2)
        
        # Save plot as image
        image_filename = 'plot.png'
        save_plot(image_filename)

        return jsonify({"plot_filename": image_filename})
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
