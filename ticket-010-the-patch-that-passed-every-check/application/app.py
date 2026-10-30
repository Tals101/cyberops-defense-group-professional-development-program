from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class LedgerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            response = {
                "service": "ledger-api",
                "status": "healthy"
            }
            self.send_response(200)
        else:
            response = {
                "service": "ledger-api",
                "message": "Synthetic payment-processing lab"
            }
            self.send_response(200)

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), LedgerHandler)
    print("ledger-api listening on port 8080", flush=True)
    server.serve_forever()
