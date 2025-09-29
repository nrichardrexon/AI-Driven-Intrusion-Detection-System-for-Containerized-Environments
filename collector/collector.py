# collector/collector.py
"""
Collector Module
- Simulates container logs and metrics collection
"""

import random
import pandas as pd

class DataCollector:
    def __init__(self):
        pass

    def collect_logs(self) -> pd.DataFrame:
        """
        Simulate container log events.
        Returns a DataFrame with events and counts.
        """
        data = [
            {"event": "login_fail", "count": random.randint(0, 5)},
            {"event": "http_error", "count": random.randint(0, 3)},
        ]
        return pd.DataFrame(data)

    def collect_metrics(self) -> pd.DataFrame:
        """
        Simulate container metrics.
        Returns a DataFrame with CPU, memory, and network connection counts.
        """
        data = {
            "cpu": random.uniform(0, 100),
            "memory": random.uniform(0, 100),
            "network_conn": random.randint(50, 200),
        }
        return pd.DataFrame([data])
