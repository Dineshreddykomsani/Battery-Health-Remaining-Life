import pandas as pd
import joblib
import os
from django.shortcuts import render

BASE_DIR = os.path.dirname(__file__)

# Load models
models = {
    'decision': joblib.load(os.path.join(BASE_DIR, 'decision.pkl')),
    'randomforest': joblib.load(os.path.join(BASE_DIR, 'randomforest.pkl')),
    'xgboost': joblib.load(os.path.join(BASE_DIR, 'xgboost.pkl')),
}

# Features
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

def index(request):
    return render(request, 'index.html', {
        'feature_names': feature_names,
        'models': models.keys()
    })

def predict(request):
    if request.method == "POST":
        try:
            model_name = request.POST.get('model_name')
            model = models[model_name]

            input_values = [float(request.POST.get(f)) for f in feature_names]
            input_df = pd.DataFrame([input_values], columns=feature_names)

            prediction = model.predict(input_df)[0]

            return render(request, 'index.html', {
                'feature_names': feature_names,
                'models': models.keys(),
                'prediction': round(float(prediction), 2),
                'selected_model': model_name
            })

        except Exception as e:
            return render(request, 'index.html', {
                'feature_names': feature_names,
                'models': models.keys(),
                'error': str(e)
            })

    return render(request, 'index.html')