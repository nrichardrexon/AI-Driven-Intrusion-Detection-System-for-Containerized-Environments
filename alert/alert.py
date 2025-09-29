# alert/alert.py
"""
Alert Module
- Logs anomaly alerts in JSON format
- Stores alerts for later retrieval
"""

import json
import time
import logging

logger = logging.getLogger("ml_ids_alert")


class AlertSystem:
    def __init__(self):
        self.alert_log = []  # Store alerts in memory

    def raise_alert(self, anomaly_data: dict):
        """
        Raises an anomaly alert.
        anomaly_data: Dictionary of feature values that triggered the alert.
        """
        alert = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "status": "ANOMALY_DETECTED",
            "data": anomaly_data
        }
        self.alert_log.append(alert)  # store alert
        print("🚨 ALERT:", json.dumps(alert, indent=2))
        logger.warning(f"Anomaly detected: {alert}")
        return alert

    def get_alerts(self):
        """
        Returns stored anomaly alerts.
        """
        return self.alert_log

    def save_alerts_to_file(self, filepath="alerts.json"):
        """
        Saves all alerts to a JSON file for persistence.
        """
        try:
            with open(filepath, "w") as f:
                json.dump(self.alert_log, f, indent=2)
            logger.info(f"✅ Alerts saved to {filepath}")
        except Exception as e:
            logger.error(f"❌ Failed to save alerts: {e}")


if __name__ == "__main__":
    # Example usage
    sample_alert = {"cpu": 98.5, "memory": 92.1, "network_conn": 180, "login_fail": 4}
    alerter = AlertSystem()
    alerter.raise_alert(sample_alert)
    print("Stored alerts:", alerter.get_alerts())
    alerter.save_alerts_to_file()
