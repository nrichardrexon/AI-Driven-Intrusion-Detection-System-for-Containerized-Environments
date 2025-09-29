# app/app.py
"""
FastAPI Application
- Orchestrates Collector → Feature Extractor → Detector → Alerts
- Supports persistent model loading and alert logging
"""

import sys
import os
import logging
import atexit

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
import pandas as pd

from collector.collector import DataCollector
from features.features import FeatureExtractor
from detector.detector import Detector
from alert.alert import AlertSystem

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ml_ids_app")

app = FastAPI(title="Lightweight ML-IDS for Containers")

# Initialize components
collector = DataCollector()
extractor = FeatureExtractor()
detector = Detector(model_path="detector_model.pkl")  # Persistent model
alerter = AlertSystem()

# Store alerts in app state
app.state.alert_logs = []

@app.on_event("startup")
async def startup_event():
    """
    Run once at startup to train the detector if not already trained.
    """
    if not detector.trained:
        logger.info("Training anomaly detector on simulated data...")
        train_data = []
        for _ in range(20):
            logs = collector.collect_logs()
            metrics = collector.collect_metrics()
            features = {**extractor.extract_from_logs(logs), **extractor.extract_from_metrics(metrics)}
            train_data.append(features)

        train_df = pd.DataFrame(train_data)
        detector.train(train_df)
        logger.info("Detector training complete.")
    else:
        logger.info("Loaded existing trained detector model.")


@app.get("/")
def root():
    """
    Root endpoint to give a friendly message.
    """
    return {"message": "Lightweight ML-IDS is running. Use /detect or /health endpoints."}


@app.get("/detect")
def detect():
    """
    Run detection on collected logs and metrics.
    """
    logs = collector.collect_logs()
    metrics = collector.collect_metrics()
    features = {**extractor.extract_from_logs(logs), **extractor.extract_from_metrics(metrics)}

    df = pd.DataFrame([features])
    prediction = detector.detect(df)[0]

    if prediction == -1:
        alert = alerter.raise_alert(features)
        app.state.alert_logs.append(alert)
        logger.warning(f"Anomaly detected: {features}")
        return {"status": "anomaly", "features": features}

    logger.info(f"Normal behavior detected: {features}")
    return {"status": "normal", "features": features}


@app.get("/logs")
def get_logs():
    """
    Return stored alerts.
    """
    return {"alerts": app.state.alert_logs}


@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {"status": "running", "message": "IDS system is healthy."}


@app.on_event("shutdown")
def shutdown_event():
    """
    Save alerts and the trained model on shutdown.
    """
    logger.info("Saving alerts and model before shutdown...")
    alerter.save_alerts_to_file("alerts.json")
    detector.save_model()
    logger.info("Shutdown complete.")


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting IDS FastAPI service...")
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
