from prometheus_client import Gauge, start_http_server
import json
import time
import os

METRICS_FILE = os.environ.get("METRICS_FILE", "artifacts/metrics.json")

# Define Prometheus gauges
ANOMALY_AUROC = Gauge("anomaly_auroc", "AUROC of the anomaly detector")
ANOMALY_AP = Gauge("anomaly_average_precision", "Average precision of the anomaly detector")
FALSE_ALARMS_PER_HOUR = Gauge("false_alarms_per_hour", "False alarms per hour")
ANOMALY_THRESHOLD = Gauge("anomaly_threshold", "Quantile threshold used for raising alarms")


def update_metrics():
    """
    Read metrics from the artifacts file and update Prometheus gauges.
    """
    if not os.path.exists(METRICS_FILE):
        return
    try:
        with open(METRICS_FILE) as f:
            data = json.load(f)
        auroc = data.get("auroc")
        ap = data.get("average_precision")
        fa = data.get("false_alarms_per_hour")
        thr = data.get("threshold")
        if auroc is not None:
            ANOMALY_AUROC.set(auroc)
        if ap is not None:
            ANOMALY_AP.set(ap)
        if fa is not None:
            FALSE_ALARMS_PER_HOUR.set(fa)
        if thr is not None:
            ANOMALY_THRESHOLD.set(thr)
    except Exception:
        pass


def main():
    """
    Start the Prometheus metrics server and periodically update gauges.
    """
    port = int(os.environ.get("METRICS_PORT", 9108))
    start_http_server(port)
    while True:
        update_metrics()
        time.sleep(30)


if __name__ == "__main__":
    main()