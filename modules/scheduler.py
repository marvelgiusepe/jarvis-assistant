"""
Autonomous Background Scheduler for JARVIS
Schedules and triggers automated phone calls, WhatsApp notifications,
and study check-in routines at user-defined hours.
"""

import os
import sys
import json
import time
import threading
import re
from datetime import datetime
from typing import List, Dict, Any, Optional

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)
schedules_file = os.path.join(base_dir, "data", "schedules.json")

from modules.phone_caller import PhoneCaller
from modules.whatsapp_notifier import WhatsAppNotifier
from modules.safety_protocol import SafetyProtocol

class JarvisScheduler:
    def __init__(self):
        self.schedules_file = schedules_file
        self.phone_caller = PhoneCaller()
        self.whatsapp_notifier = WhatsAppNotifier()
        self.safety = SafetyProtocol()
        self.schedules = self.load_schedules()
        self._running = False
        self._thread = None

    def load_schedules(self) -> List[Dict[str, Any]]:
        default_schedules = [
            {
                "id": "study_reminder_1",
                "label": "Jadwal Belajar & Safety Check",
                "time": "20:00",
                "repeat": "daily",
                "actions": ["phone_call", "whatsapp_message"],
                "enabled": True,
                "last_triggered_date": None
            }
        ]
        if os.path.exists(self.schedules_file):
            try:
                with open(self.schedules_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            except Exception:
                pass
        self.save_schedules(default_schedules)
        return default_schedules

    def save_schedules(self, data: List[Dict[str, Any]] = None):
        if data is not None:
            self.schedules = data
        os.makedirs(os.path.dirname(self.schedules_file), exist_ok=True)
        try:
            with open(self.schedules_file, "w", encoding="utf-8") as f:
                json.dump(self.schedules, f, indent=2)
        except Exception:
            pass

    def add_schedule(self, time_str: str, label: str = "Jadwal Belajar", actions: List[str] = None) -> Dict[str, Any]:
        """Add or update a schedule with time in HH:MM format."""
        time_clean = self._normalize_time(time_str)
        if not time_clean:
            return {"status": "error", "message": "Format waktu tidak valid. Gunakan format seperti 20:00 atau 8 malam."}

        actions = actions or ["phone_call", "whatsapp_message"]
        sched_id = f"sched_{int(time.time())}"
        new_entry = {
            "id": sched_id,
            "label": label,
            "time": time_clean,
            "repeat": "daily",
            "actions": actions,
            "enabled": True,
            "last_triggered_date": None
        }
        self.schedules.append(new_entry)
        self.save_schedules()
        return {"status": "success", "schedule": new_entry}

    def remove_schedule(self, query: str) -> bool:
        initial_len = len(self.schedules)
        q = query.lower()
        self.schedules = [s for s in self.schedules if q not in s.get("label", "").lower() and q not in s.get("time", "")]
        if len(self.schedules) < initial_len:
            self.save_schedules()
            return True
        return False

    def get_schedules(self) -> List[Dict[str, Any]]:
        return self.schedules

    def _normalize_time(self, t_str: str) -> Optional[str]:
        t = t_str.lower().strip()
        
        # Check standard 24h format e.g. 20:00, 08:30
        m24 = re.search(r'(\d{1,2}):(\d{2})', t)
        if m24:
            hh = int(m24.group(1))
            mm = int(m24.group(2))
            if 0 <= hh <= 23 and 0 <= mm <= 59:
                return f"{hh:02d}:{mm:02d}"

        # Check natural language e.g. "8 malam", "7 pagi", "8 pm", "7 am"
        m_nat = re.search(r'(\d{1,2})(?:\s*(?:malam|sore|pm|pagi|siang|am))?', t)
        if m_nat:
            h = int(m_nat.group(1))
            if any(w in t for w in ["malam", "sore", "pm"]):
                if h < 12: h += 12
            elif any(w in t for w in ["pagi", "am"]):
                if h == 12: h = 0
            if 0 <= h <= 23:
                return f"{h:02d}:00"

        return None

    def trigger_now(self, schedule_entry: Dict[str, Any]):
        """Execute the actions specified in a schedule entry."""
        actions = schedule_entry.get("actions", ["phone_call", "whatsapp_message"])
        label = schedule_entry.get("label", "Jadwal Belajar")
        time_str = schedule_entry.get("time", "")

        call_msg = (
            f"Halo Sir, ini J.A.R.V.I.S. Waktu belajar Anda pukul {time_str} telah tiba. "
            f"Pastikan Anda dalam keadaan aman, tenang, dan siap fokus belajar. "
            f"Sistem pengaman workstation aktif menunggu konfirmasi Anda."
        )

        wa_msg = (
            f"🚨 *J.A.R.V.I.S. SAFETY & STUDY PROTOCOL*\n\n"
            f"Selamat malam, Sir.\n"
            f"Waktu menunjukkan pukul *{time_str}*, jadwal *{label}* Anda telah aktif.\n\n"
            f"🛡️ *Pemeriksaan Keamanan*: Status PENDING.\n"
            f"Harap pastikan Anda aman. Balas pesan ini atau klik 'Confirm Safe' di layar untuk mencatat status aman Anda.\n\n"
            f"— _J.A.R.V.I.S. Autonomous Intelligence_"
        )

        results = {}
        if "phone_call" in actions:
            res_call = self.phone_caller.make_call(message=call_msg)
            results["phone_call"] = res_call

        if "whatsapp_message" in actions:
            res_wa = self.whatsapp_notifier.send_whatsapp(message=wa_msg)
            results["whatsapp"] = res_wa

        self.safety.trigger_checkin(label)
        return results

    def _scheduler_loop(self):
        while self._running:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            today_date = now.strftime("%Y-%m-%d")

            for s in self.schedules:
                if s.get("enabled", True):
                    sched_time = s.get("time")
                    last_date = s.get("last_triggered_date")

                    if sched_time == current_time and last_date != today_date:
                        print(f"[*] [Scheduler] Triggering schedule: {s.get('label')} at {current_time}")
                        s["last_triggered_date"] = today_date
                        self.save_schedules()
                        try:
                            self.trigger_now(s)
                        except Exception as e:
                            print(f"[!] [Scheduler] Trigger error: {e}")

            time.sleep(10)

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._scheduler_loop, daemon=True)
            self._thread.start()
            print("[*] J.A.R.V.I.S. Autonomous Scheduler active.")

    def stop(self):
        self._running = False

if __name__ == "__main__":
    sched = JarvisScheduler()
    print("Schedules:", sched.get_schedules())
    print("Test parse 8 malam:", sched._normalize_time("8 malam"))
    print("Test parse 20:30:", sched._normalize_time("20:30"))
