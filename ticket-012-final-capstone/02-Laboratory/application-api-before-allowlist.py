import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

PORT = 8080
INTERNAL_URL = os.environ.get(
    "INTERNAL_URL",
    "http://internal-service:8080/resource"
)
LAB_TOKEN = os.environ.get("LAB_AUTH_TOKEN", "")

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            status = 200
            response = {"status": "healthy"}

        elif self.path == "/call-internal":
            request = Request(
                INTERNAL_URL,
                headers={
                    "X-Lab-Identity": "application-api",
                    "X-Lab-Token": LAB_TOKEN
                }
            )

            try:
                with urlopen(request, timeout=5) as result:
                    status = result.status
                    response = json.loads(result.read())

            except HTTPError as error:
                status = error.code
                response = {"error": "internal service rejected request"}

            except URLError:
                status = 502
                response = {"error": "internal service unavailable"}

        else:
            status = 404
            response = {"error": "not found"}

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "application-api",
            "path": self.path,
            "status": status
        }

        print(json.dumps(event), flush=True)

        body = json.dumps(response).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
