import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 8080

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        identity = self.headers.get("X-Lab-Identity", "unknown")
        token = self.headers.get("X-Lab-Token", "")

        if self.path == "/health":
            status = 200
            response = {"status": "healthy"}

        elif self.path == "/resource":
            expected = os.environ.get("LAB_AUTH_TOKEN", "")

            if expected and token == expected and identity == "application-api":
                status = 200
                response = {"result": "authorized", "data": "synthetic"}
            else:
                status = 403
                response = {"result": "denied"}

        else:
            status = 404
            response = {"error": "not found"}

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "internal-service",
            "identity": identity,
            "path": self.path,
            "status": status,
            "source_ip": self.client_address[0]
        }

        print(json.dumps(event), flush=True)

        body = json.dumps(response).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
