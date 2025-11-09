from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load trained models
models = {
    'randomforest': joblib.load('models/randomforest.pkl'),
    'Xgb_model': joblib.load('models/Xgb_model.pkl'),
    'decision': joblib.load('models/decision.pkl')
}

# Feature names + units
feature_names = [
    'Cycle_Index',
    'Discharge Time (s)',
    'Decrement 3.6-3.4V (s)',
    'Max. Voltage Dischar. (V)',
    'Min. Voltage Charg. (V)',
    'Time at 4.15V (s)',
    'Time constant current (s)',
    'Charging time (s)'
]

@app.route('/')
def index():
    return render_template('index.html', models=models.keys(), feature_names=feature_names)

@app.route('/predict', methods=['POST'])
def predict():
    model_name = request.form['model_name']
    model = models[model_name]

    # Collect input values in same order
    input_values = [float(request.form[feature]) for feature in feature_names]

    # Convert to DataFrame
    input_df = pd.DataFrame([input_values], columns=feature_names)

    # Predict
    result = model.predict(input_df)[0]

    return render_template('index.html', models=models.keys(), feature_names=feature_names, prediction=result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
