from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load trained models (make sure 'models/' folder exists in repo)
models = {
    'randomforest': joblib.load('models/randomforest.pkl'),
    'Xgb_model': joblib.load('models/Xgb_model.pkl'),
    'decision': joblib.load('models/decision.pkl')
}

# This MUST be a dictionary (NOT list, NOT tuple)
feature_names = {
    'Cycle_Index': 'count',
    'Discharge Time (s)': 'seconds',
    'Decrement 3.6-3.4V (s)': 'seconds',
    'Max. Voltage Dischar. (V)': 'Volts',
    'Min. Voltage Charg. (V)': 'Volts',
    'Time at 4.15V (s)': 'seconds',
    'Time constant current (s)': 'seconds',
    'Charging time (s)': 'seconds'
}

@app.route('/')
def index():
    return render_template('index.html', models=list(models.keys()), feature_names=feature_names)

@app.route('/predict', methods=['POST'])
def predict():
    model_name = request.form['model_name']
    model = models[model_name]

    # Collect input values safely
    input_values = []
    for feature in feature_names.keys():
        input_values.append(float(request.form.get(feature)))

    # Convert into DataFrame
    input_df = pd.DataFrame([input_values], columns=feature_names.keys())

    prediction = model.predict(input_df)[0]

    return render_template('index.html', models=list(models.keys()), feature_names=feature_names, prediction=prediction)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # IMPORTANT for Render
    app.run(host='0.0.0.0', port=port)
