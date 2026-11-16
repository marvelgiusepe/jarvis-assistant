"""
WhatsApp Notifier Module for JARVIS
Dispatches automated WhatsApp messages via Twilio WhatsApp API or WhatsApp Web protocol.
"""

import os
import json
import base64
import urllib.request
import urllib.parse
import subprocess
from typing import Dict, Any

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(base_dir, "data", "phone_config.json")

class WhatsAppNotifier:
    def __init__(self):
        self.config_file = config_file

    def get_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def send_whatsapp(self, to_number: str = None, message: str = None) -> Dict[str, Any]:
        cfg = self.get_config()
        target = to_number or cfg.get("target_phone_number", "")
        # Clean target e.g. "+628123456" or "08123456" -> international format
        clean_num = target.replace(" ", "").replace("-", "")
        if clean_num.startswith("08"):
            clean_num = "+628" + clean_num[2:]
        elif not clean_num.startswith("+"):
            clean_num = "+" + clean_num

        text = message or (
            "🚨 *J.A.R.V.I.S. SAFETY & STUDY PROTOCOL*\n\n"
            "Selamat malam, Sir.\n"
            "Sesuai jadwal yang telah ditentukan, saat ini adalah waktu untuk memulai sesi belajar Anda.\n\n"
            "🛡️ *Status Keamanan*: Menunggu konfirmasi.\n"
            "Silakan balas pesan ini atau konfirmasi di workstation untuk menandakan bahwa Anda aman.\n\n"
            "— _J.A.R.V.I.S. Operating Intelligence_"
        )

        sid = cfg.get("twilio_account_sid", "").strip()
        token = cfg.get("twilio_auth_token", "").strip()
        from_num = cfg.get("twilio_whatsapp_number", "").strip() or cfg.get("twilio_phone_number", "").strip()

        # 1. DIRECT TWILIO WHATSAPP REST API (BACKGROUND DELIVERY)
        if sid and token and from_num:
            try:
                url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
                twilio_from = from_num if from_num.startswith("whatsapp:") else f"whatsapp:{from_num}"
                twilio_to = f"whatsapp:{clean_num}"

                data = urllib.parse.urlencode({
                    "From": twilio_from,
                    "To": twilio_to,
                    "Body": text
                }).encode("utf-8")

                req = urllib.request.Request(url, data=data, method="POST")
                auth_str = f"{sid}:{token}"
                auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
                req.add_header("Authorization", f"Basic {auth_b64}")

                with urllib.request.urlopen(req, timeout=12) as response:
                    res_body = response.read().decode("utf-8")
                    msg_data = json.loads(res_body)
                    return {
                        "status": "success",
                        "method": "twilio_whatsapp_api",
                        "sid": msg_data.get("sid"),
                        "to": clean_num,
                        "reply": f"WhatsApp notification successfully delivered to {clean_num}, Sir."
                    }
            except Exception as e:
                # If API errors, fallback to WhatsApp Web protocol
                pass

        # 2. WHATSAPP WEB / DESKTOP DISPATCHER
        try:
            encoded_text = urllib.parse.quote(text)
            clean_digits = clean_num.replace("+", "")
            web_url = f"https://web.whatsapp.com/send?phone={clean_digits}&text={encoded_text}"
            
            # Non-blocking launch in browser
            subprocess.Popen(['cmd.exe', '/c', 'start', '', web_url], shell=True)
            return {
                "status": "success",
                "method": "whatsapp_web",
                "to": clean_num,
                "url": web_url,
                "reply": f"WhatsApp Web notification dispatched for {clean_num}, Sir."
            }
        except Exception as e:
            return {
                "status": "error",
                "method": "none",
                "error": str(e),
                "reply": f"Failed to dispatch WhatsApp message: {e}, Sir."
            }

if __name__ == "__main__":
    wn = WhatsAppNotifier()
    print("WhatsApp config:", wn.get_config())

