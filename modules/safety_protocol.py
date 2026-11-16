"""
Safety Protocol & Check-in Matrix for JARVIS
Monitors user safety window after study alerts are dispatched.
Ensures confirmation within 15 minutes, otherwise flags an alert state.
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, Any

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
status_file = os.path.join(base_dir, "data", "safety_status.json")

class SafetyProtocol:
    def __init__(self):
        self.status_file = status_file
        self.state = self.load_state()

    def load_state(self) -> Dict[str, Any]:
        default_state = {
            "status": "SECURE",
            "last_checkin_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pending_since": None,
            "deadline": None,
            "timeout_seconds": 900, # 15 minutes
            "alert_source": None
        }
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    default_state.update(data)
            except Exception:
                pass
        return default_state

    def save_state(self):
        os.makedirs(os.path.dirname(self.status_file), exist_ok=True)
        try:
            with open(self.status_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2)
        except Exception:
            pass

    def trigger_checkin(self, source_label: str = "Jadwal Belajar"):
        now = time.time()
        timeout = self.state.get("timeout_seconds", 900)
        self.state["status"] = "CHECKIN_PENDING"
        self.state["pending_since"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.state["deadline"] = now + timeout
        self.state["alert_source"] = source_label
        self.save_state()

    def confirm_safe(self, method: str = "voice") -> str:
        self.state["status"] = "SECURE"
        self.state["last_checkin_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.state["pending_since"] = None
        self.state["deadline"] = None
        self.save_state()
        return "Safety confirmed and logged into central matrix, Sir. All security parameters green."

    def get_status(self) -> Dict[str, Any]:
        # Check if overdue
        if self.state.get("status") == "CHECKIN_PENDING" and self.state.get("deadline"):
            if time.time() > self.state["deadline"]:
                self.state["status"] = "ALERT_OVERDUE"
                self.save_state()
        return self.state

if __name__ == "__main__":
    sp = SafetyProtocol()
    print("Safety State:", sp.get_status())

