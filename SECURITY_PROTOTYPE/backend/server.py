import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from backend.detector import detect_logs


class SecurityHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/check":
            self.send_error(404)
            return

        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)

        try:
            log = json.loads(body)
            alerts = detect_logs(log)

            response = {
                "status": "ALERT" if alerts else "OK",
                "user": log.get("user"),
                "alerts": alerts,
            }

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(
                json.dumps(response).encode()
            )

        except (json.JSONDecodeError, TypeError, KeyError):
            self.send_error(400, "Invalid JSON")


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), SecurityHandler)

    print("Security API running on http://localhost:8080")

    server.serve_forever()
