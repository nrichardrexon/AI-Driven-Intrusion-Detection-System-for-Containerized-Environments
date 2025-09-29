# features/features.py
"""
Feature Extraction Module
- Converts logs and metrics into numeric features
"""

import pandas as pd

class FeatureExtractor:
    def __init__(self):
        pass

    def extract_from_logs(self, logs: pd.DataFrame) -> dict:
        """
        Converts logs DataFrame into a feature dictionary.
        Example: {"login_fail": 3, "http_error": 1}
        """
        return logs.set_index("event")["count"].to_dict()

    def extract_from_metrics(self, metrics: pd.DataFrame) -> dict:
        """
        Converts metrics DataFrame into a feature dictionary.
        Example: {"cpu": 65.2, "memory": 70.1, "network_conn": 150}
        """
        return metrics.iloc[0].to_dict()


if __name__ == "__main__":
    from collector.collector import DataCollector

    collector = DataCollector()
    logs = collector.collect_logs()
    metrics = collector.collect_metrics()

    extractor = FeatureExtractor()
    features = {**extractor.extract_from_logs(logs), **extractor.extract_from_metrics(metrics)}

    print("Extracted Features:\n", features)
