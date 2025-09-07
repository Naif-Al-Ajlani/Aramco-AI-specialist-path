# Simple Prometheus exporter that reads artifacts/metrics.json periodically
import time, json, os
from http.server import BaseHTTPRequestHandler, HTTPServer

METRICS_FILE = os.environ.get("METRICS_FILE","artifacts/metrics.json")
HOST = os.environ.get("HOST","0.0.0.0")
PORT = int(os.environ.get("PORT","9108"))

def read_metrics():
    try:
        with open(METRICS_FILE) as f:
            m = json.load(f)
    except Exception:
        m = {}
    return m

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/metrics":
            self.send_response(404); self.end_headers(); return
        m = read_metrics()
        body = ""
        mapping = {
            "FA_per_hour":"gasops_false_alarms_per_hour",
            "AUROC":"gasops_auroc",
            "AUPRC":"gasops_auprc"
        }
        for k, prom in mapping.items():
            if k in m:
                body += f"# TYPE {prom} gauge\n{prom} {m[k]}\n"
        self.send_response(200)
        self.send_header("Content-Type","text/plain; version=0.0.4")
        self.end_headers()
        self.wfile.write(body.encode())

if __name__=="__main__":
    httpd = HTTPServer((HOST, PORT), Handler)
    print(f"Exporter on {HOST}:{PORT}, reading {METRICS_FILE}")
    httpd.serve_forever()
