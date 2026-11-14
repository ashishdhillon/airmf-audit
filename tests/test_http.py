import http.server
import json
import sys
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from airmf_audit.http_target import create_http_target


class MockLLMHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        req_json = json.loads(post_data.decode("utf-8"))

        auth_header = self.headers.get("Authorization", "")
        prompt = req_json["messages"][0]["content"]

        resp_payload = {
            "choices": [
                {
                    "message": {
                        "content": f"Echo: {prompt} (Auth: {auth_header != ''})"
                    }
                }
            ]
        }
        resp_bytes = json.dumps(resp_payload).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.end_headers()
        self.wfile.write(resp_bytes)

    def log_message(self, format, *args):
        # Suppress server logs during test
        pass


class TestHTTPTarget(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.HTTPServer(("127.0.0.1", 0), MockLLMHandler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_http_endpoint_call(self):
        endpoint = f"http://127.0.0.1:{self.port}/v1/chat/completions"
        target_fn = create_http_target(endpoint, model="llama3", api_key="secret-token-123")
        response = target_fn("Hello safety auditor")
        self.assertIn("Echo: Hello safety auditor", response)
        self.assertIn("Auth: True", response)


if __name__ == "__main__":
    unittest.main()
