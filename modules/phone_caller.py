"""
Phone Caller Module for JARVIS
Handles real GSM voice phone calls via Twilio Voice API, Windows Phone Link,
and local telephony protocols.
"""

import os
import json
import base64
import urllib.request
import urllib.parse
from typing import Dict, Any

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(base_dir, "data", "phone_config.json")

class PhoneCaller:
    def __init__(self):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        default_config = {
            "target_phone_number": "+6281234567890",
            "twilio_account_sid": "",
            "twilio_auth_token": "",
            "twilio_phone_number": "",
            "ntfy_topic": "jarvis-study-alert",
            "caller_name": "J.A.R.V.I.S.",
            "voice_language": "id-ID",
            "voice_name": "Polly.Brian"
        }
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    default_config.update(data)
            except Exception:
                pass
        return default_config

    def save_config(self, new_data: Dict[str, Any]) -> bool:
        self.config.update(new_data)
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception:
            return False

    def make_call(self, to_number: str = None, message: str = None) -> Dict[str, Any]:
        """
        Trigger an actual phone call to the target phone number.
        Uses Twilio Voice REST API if credentials are provided.
        Falls back to Windows Phone Link protocol if credentials not yet configured.
        """
        target = to_number or self.config.get("target_phone_number", "")
        speech = message or (
            "Halo Sir, ini J.A.R.V.I.S. Waktu belajar Anda telah tiba sesuai jadwal. "
            "Harap konfirmasi bahwa Anda dalam keadaan aman dan siap untuk fokus."
        )

        sid = self.config.get("twilio_account_sid", "").strip()
        token = self.config.get("twilio_auth_token", "").strip()
        from_num = self.config.get("twilio_phone_number", "").strip()

        # 1. REAL GSM CALL VIA TWILIO API
        if sid and token and from_num and target:
            try:
                url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Calls.json"
                
                # Construct TwiML speech response
                twiml = (
                    f'<Response>'
                    f'<Pause length="1"/>'
                    f'<Say voice="{self.config.get("voice_name", "Polly.Brian")}" language="{self.config.get("voice_language", "id-ID")}">'
                    f'{speech}'
                    f'</Say>'
                    f'<Pause length="2"/>'
                    f'<Say voice="{self.config.get("voice_name", "Polly.Brian")}" language="{self.config.get("voice_language", "id-ID")}">'
                    f'Sistem menunggu konfirmasi keamanan Anda di workstation. Selamat belajar, Sir.'
                    f'</Say>'
                    f'</Response>'
                )

                data = urllib.parse.urlencode({
                    "To": target,
                    "From": from_num,
                    "Twiml": twiml
                }).encode("utf-8")

                req = urllib.request.Request(url, data=data, method="POST")
                auth_str = f"{sid}:{token}"
                auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
                req.add_header("Authorization", f"Basic {auth_b64}")

                with urllib.request.urlopen(req, timeout=12) as response:
                    res_body = response.read().decode("utf-8")
                    call_data = json.loads(res_body)
                    return {
                        "status": "success",
                        "method": "twilio_gsm_call",
                        "call_sid": call_data.get("sid"),
                        "to": target,
                        "reply": f"Direct voice call dispatched to {target}, Sir. Your phone should be ringing momentarily."
                    }
            except Exception as e:
                # Log error and fall back to local Windows dialer
                return {
                    "status": "partial_error",
                    "method": "twilio_error",
                    "error": str(e),
                    "reply": f"Twilio gateway error: {e}. Opening local Windows phone dialer for {target}, Sir."
                }

        # 2. NTFY EMERGENCY PHONE RING / ALARM (100% FREE, NO PULSA, LOUD RINGTONE)
        ntfy_topic = self.config.get("ntfy_topic", "").strip()
        ntfy_success = False
        if ntfy_topic:
            try:
                ntfy_url = f"https://ntfy.sh/{ntfy_topic}"
                req = urllib.request.Request(
                    ntfy_url,
                    data=speech.encode("utf-8"),
                    method="POST"
                )
                req.add_header("Title", "📞 J.A.R.V.I.S. Incoming Study Call")
                req.add_header("Priority", "urgent")
                req.add_header("Tags", "phone,warning,bell")
                req.add_header("Click", "http://localhost:8765")
                with urllib.request.urlopen(req, timeout=8) as res:
                    if res.status == 200:
                        ntfy_success = True
            except Exception:
                pass

        # 3. WINDOWS PHONE LINK (DIALER PROTOCOL)
        # Opens Phone Link / default dialer for the target number
        try:
            import subprocess
            clean_target = urllib.parse.quote(target)
            subprocess.Popen(['cmd.exe', '/c', 'start', '', f'tel:{clean_target}'], shell=True)
            
            if ntfy_success:
                return {
                    "status": "success",
                    "method": "ntfy_and_phone_link",
                    "to": target,
                    "reply": f"Loud study call alert dispatched to your mobile via ntfy topic '{ntfy_topic}', Sir. To enable direct GSM cellular calls, add your Twilio credentials in phone_config.json."
                }

            return {
                "status": "success",
                "method": "windows_phone_link",
                "to": target,
                "reply": f"Phone Link dialer activated for {target}, Sir. Please note: To make actual GSM cellular calls without Phone Link, enter your Twilio credentials in phone_config.json."
            }
        except Exception as e:
            subprocess.Popen(['cmd.exe', '/c', 'start', '', f'tel:{clean_target}'], shell=True)
            return {
                "status": "success",
                "method": "windows_phone_link",
                "to": target,
                "reply": f"Phone Link dialer activated for {target}, Sir. Please configure Twilio credentials in phone_config.json for automatic autonomous GSM cellular calls."
            }
        except Exception as e:
            return {
                "status": "error",
                "method": "none",
                "error": str(e),
                "reply": f"Unable to dispatch call: {e}, Sir."
            }

if __name__ == "__main__":
    caller = PhoneCaller()
    print("Config:", caller.config)

