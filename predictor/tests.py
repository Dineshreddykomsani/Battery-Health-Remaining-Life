from django.test import TestCase
from django.urls import reverse

from .views import FEATURE_NAMES, MODELS


class PredictorTests(TestCase):
    def test_index_loads(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "predictor/index.html")

    def test_prediction_uses_existing_models(self):
        payload = {feature: "1" for feature in FEATURE_NAMES}
        payload["model_name"] = "decision"
        response = self.client.post(reverse("predict"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("prediction", response.context)

    def test_invalid_model_is_rejected(self):
        response = self.client.post(reverse("predict"), {"model_name": "unknown"})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Please select a prediction model.", status_code=400)

    def test_all_expected_model_artifacts_are_loaded(self):
        self.assertEqual(set(MODELS), {"decision", "randomforest", "xgboost"})
