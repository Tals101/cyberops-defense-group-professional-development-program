import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVICE = "ticket011-reporting-api"


def response_for(path):
    path = path.split("?", 1)[0]

    if path == "/health":
        return 200, {
            "status": "ok",
            "service": SERVICE,
            "environment": "isolated-lab"
        }

    if path == "/report":
        return 200, {
            "service": SERVICE,
            "report_type": "synthetic",
            "records": 0,
            "contains_real_financial_data": False
        }

    return 404, {"error": "not_found"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, data = response_for(self.path)
        payload = json.dumps(data, sort_keys=True).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format_string, *args):
        print("LAB_HTTP_REQUEST", flush=True)


def self_test():
    status, health = response_for("/health")
    assert status == 200
    assert health["status"] == "ok"

    status, report = response_for("/report")
    assert status == 200
    assert report["report_type"] == "synthetic"
    assert report["contains_real_financial_data"] is False

    status, missing = response_for("/missing")
    assert status == 404
    assert missing["error"] == "not_found"

    print("SELF_TEST_PASS", flush=True)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        server = ThreadingHTTPServer(("0.0.0.0", 8080), Handler)
        print("LAB_REPORTING_API_READY", flush=True)
        server.serve_forever()
