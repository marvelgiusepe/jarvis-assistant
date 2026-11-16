"""
JARVIS Desktop API & Web Server
Serves the HUD dashboard on http://localhost:8765 and provides system control APIs.
Using http://localhost allows Chrome/Edge to permanently remember microphone permissions.
"""

import http.server
import socketserver
import json
import sys
import os
from typing import Dict, Any

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

from modules.system_operator import SystemOperator

PORT = 8765
op = SystemOperator()

class JarvisRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors()
        self.end_headers()

    def do_GET(self):
        # Serve HUD HTML for root or /hud.html
        if self.path in ["/", "/hud.html", "/index.html"]:
            hud_path = os.path.join(PROJECT_DIR, "hud.html")
            if os.path.exists(hud_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self._set_cors()
                self.end_headers()
                with open(hud_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.end_headers()
                return

        # Serve Icon Assets
        elif self.path in ["/jarvis.png", "/favicon.ico"]:
            icon_path = os.path.join(PROJECT_DIR, "jarvis.png")
            if os.path.exists(icon_path):
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self._set_cors()
                self.end_headers()
                with open(icon_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            self.send_response(404)
            self.end_headers()
            return

        elif self.path == "/jarvis.ico":
            icon_path = os.path.join(PROJECT_DIR, "jarvis.ico")
            if os.path.exists(icon_path):
                self.send_response(200)
                self.send_header("Content-Type", "image/x-icon")
                self._set_cors()
                self.end_headers()
                with open(icon_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            self.send_response(404)
            self.end_headers()
            return

        # API: Status
        elif self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._set_cors()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "online", "model": "JARVIS-Frontier"}).encode())

        # API: Telemetry
        elif self.path == "/api/telemetry":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._set_cors()
            self.end_headers()
            data = op.get_system_telemetry()
            self.wfile.write(json.dumps(data).encode())

        # API: Phone Configuration
        elif self.path == "/api/phone/config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._set_cors()
            self.end_headers()
            self.wfile.write(json.dumps(op.phone_caller.config).encode())

        # API: Schedules List
        elif self.path == "/api/schedules":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._set_cors()
            self.end_headers()
            self.wfile.write(json.dumps(op.get_schedules()).encode())

        # API: Safety Status
        elif self.path == "/api/safety/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._set_cors()
            self.end_headers()
            self.wfile.write(json.dumps(op.get_safety_status()).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode() if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if self.path == "/api/command":
            cmd = payload.get("command", "")
            try:
                res = op.parse_and_execute(cmd)
                if isinstance(res, dict):
                    reply_text = res.get("reply", "")
                    action = res.get("action", "none")
                    target = res.get("target", "")
                    target_type = res.get("target_type", "")
                    url = res.get("url", None)
                else:
                    reply_text = str(res)
                    action = "none"
                    target = ""
                    target_type = ""
                    url = None

                response_data = {
                    "status": "ok",
                    "reply": reply_text,
                    "action": action,
                    "target": target,
                    "target_type": target_type,
                    "url": url
                }
            except Exception as e:
                response_data = {
                    "status": "error",
                    "reply": f"An error occurred while executing directive: {e}",
                    "action": "none",
                    "target": "",
                    "target_type": "none",
                    "url": None
                }

            self._send_json(response_data)

        elif self.path == "/api/phone/config":
            op.phone_caller.save_config(payload)
            self._send_json({"status": "ok", "config": op.phone_caller.config})

        elif self.path == "/api/phone/call":
            to_num = payload.get("to")
            msg = payload.get("message")
            res = op.make_phone_call(to_num, msg)
            self._send_json(res)

        elif self.path == "/api/phone/whatsapp":
            to_num = payload.get("to")
            msg = payload.get("message")
            res = op.send_whatsapp(to_num, msg)
            self._send_json(res)

        elif self.path == "/api/schedules":
            time_str = payload.get("time", "20:00")
            label = payload.get("label", "Jadwal Belajar")
            res = op.add_schedule(time_str, label)
            self._send_json(res)

        elif self.path == "/api/safety/confirm":
            reply = op.confirm_safety()
            self._send_json({"status": "ok", "reply": reply})

        elif self.path == "/api/spawn-url":
            url = payload.get("url", "")
            if url:
                op.open_website(url, spawn_os=True)
            self._send_json({"status": "ok"})

        elif self.path == "/api/close-active-tab":
            op.close_active_tab()
            self._send_json({"status": "ok"})

        else:
            self.send_response(404)
            self.end_headers()

    def _send_json(self, data: Dict[str, Any], code: int = 200):
        try:
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self._set_cors()
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except Exception:
            pass

    def log_message(self, format, *args):
        return

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), JarvisRequestHandler) as httpd:
        print(f"[*] J.A.R.V.I.S. Core listening on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
