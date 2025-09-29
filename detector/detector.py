# detector/detector.py
"""
Detector Module
- Uses Isolation Forest for anomaly detection
"""

import logging
import joblib
from sklearn.ensemble import IsolationForest
import pandas as pd
import os

logger = logging.getLogger("ml_ids_detector")

class Detector:
    def __init__(self, model_path="detector_model.pkl"):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.trained = False
        self.model_path = model_path
        if os.path.exists(model_path):
            self.load_model()

    def train(self, X: pd.DataFrame):
        """
        Train the Isolation Forest model.
        X: DataFrame of numeric features representing normal behavior.
        """
        if X.empty:
            logger.error("Training data is empty. Cannot train model.")
            return

        self.model.fit(X)
        self.trained = True
        logger.info("✅ Model trained successfully.")
        self.save_model()

    def detect(self, X: pd.DataFrame):
        """
        Detect anomalies.
        Returns: array of predictions (-1 = anomaly, 1 = normal)
        """
        if not self.trained:
            logger.error("Model not trained yet!")
            raise ValueError("Model not trained yet!")
        if X.empty:
            logger.warning("Empty feature set passed to detector.")
            return [1]  # treat as normal
        return self.model.predict(X)

    def save_model(self):
        try:
            joblib.dump(self.model, self.model_path)
            logger.info(f"✅ Detector model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"❌ Failed to save model: {e}")

    def load_model(self):
        try:
            self.model = joblib.load(self.model_path)
            self.trained = True
            logger.info(f"✅ Detector model loaded from {self.model_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")

if __name__ == "__main__":
    import pandas as pd
    from collector.collector import DataCollector
    from features.features import FeatureExtractor

    logging.basicConfig(level=logging.INFO)

    # Simulate training data
    collector = DataCollector()
    extractor = FeatureExtractor()
    train_data = []

    for _ in range(20):
        logs = collector.collect_logs()
        metrics = collector.collect_metrics()
        features = {**extractor.extract_from_logs(logs), **extractor.extract_from_metrics(metrics)}
        train_data.append(features)

    train_df = pd.DataFrame(train_data)

    # Train the detector
    detector = Detector()
    detector.train(train_df)

    # Simulate detection
    test_logs = collector.collect_logs()
    test_metrics = collector.collect_metrics()
    test_features = {**extractor.extract_from_logs(test_logs), **extractor.extract_from_metrics(test_metrics)}
    test_df = pd.DataFrame([test_features])

    prediction = detector.detect(test_df)[0]
    print("Prediction:", "Anomaly" if prediction == -1 else "Normal")
