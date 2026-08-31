from pathlib import Path

import joblib
import pandas as pd
from django.shortcuts import render
from django.views.decorators.http import require_POST


MODEL_DIR = Path(__file__).resolve().parent

# Original pre-trained artifacts: inference only, never retrained or modified here.
MODELS = {
    "decision": joblib.load(MODEL_DIR / "decision.pkl"),
    "randomforest": joblib.load(MODEL_DIR / "randomforest.pkl"),
    "xgboost": joblib.load(MODEL_DIR / "xgboost.pkl"),
}

FEATURE_NAMES = [
    "Cycle_Index",
    "Discharge Time (s)",
    "Decrement 3.6-3.4V (s)",
    "Max. Voltage Dischar. (V)",
    "Min. Voltage Charg. (V)",
    "Time at 4.15V (s)",
    "Time constant current (s)",
    "Charging time (s)",
]


def page_context(**extra):
    return {"feature_names": FEATURE_NAMES, "models": MODELS.keys(), **extra}


def index(request):
    return render(request, "predictor/index.html", page_context())


@require_POST
def predict(request):
    model_name = request.POST.get("model_name", "")
    if model_name not in MODELS:
        return render(
            request,
            "predictor/index.html",
            page_context(error="Please select a prediction model.", selected_model=model_name),
            status=400,
        )

    try:
        input_values = [float(request.POST[feature]) for feature in FEATURE_NAMES]
    except (KeyError, TypeError, ValueError):
        return render(
            request,
            "predictor/index.html",
            page_context(error="Enter a valid number for each battery input.", selected_model=model_name),
            status=400,
        )

    # Feature names and order exactly match the original training dataset.
    input_df = pd.DataFrame([input_values], columns=FEATURE_NAMES)
    prediction = MODELS[model_name].predict(input_df)[0]
    return render(
        request,
        "predictor/index.html",
        page_context(prediction=round(float(prediction), 2), selected_model=model_name),
    )
