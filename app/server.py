import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = os.environ.get("APP_VERSION", "dev")


def greet(name: str) -> str:
    name = name.strip() or "world"
    return f"hello, {name}"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/healthz":
            self._send(200, {"status": "ok"})
        elif self.path == "/" or self.path.startswith("/?"):
            name = ""
            if "?name=" in self.path:
                name = self.path.split("?name=", 1)[1].split("&", 1)[0]
            self._send(200, {"message": greet(name), "version": VERSION})
        else:
            self._send(404, {"error": "not found"})

    def _send(self, code: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.address_string()} {fmt % args}", flush=True)


def main() -> None:
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"listening on :{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
