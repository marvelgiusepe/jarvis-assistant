"""
Cognitive AI Brain for JARVIS
Structured semantic understanding, strict context isolation, and zero state leakage.
"""

import re
import urllib.parse
from typing import Dict, Any, Optional

class CognitiveBrain:
    def __init__(self, sys_operator):
        self.op = sys_operator

    def analyze_and_execute(self, user_text: str) -> Dict[str, Any]:
        """
        Analyze user intent and return a strictly isolated response packet:
        {
            "reply": str,
            "action": "open_url" | "close_url" | "open_app" | "close_app" | "system" | "math" | "conversation" | "none",
            "target": str,
            "target_type": "website" | "app" | "hardware" | "system" | "none",
            "url": Optional[str]
        }
        """
        text = user_text.strip()
        if not text:
            return {"reply": "Awaiting your directive, Sir.", "action": "none", "target": "", "target_type": "none", "url": None}

        # Multi-action chaining (e.g. "close spotify and lock laptop")
        chained_parts = re.split(r'\s+(?:and then|dan kemudian|lalu|kemudian|and|dan)\s+', text, flags=re.IGNORECASE)
        if len(chained_parts) > 1:
            replies = []
            final_action = "none"
            final_target = ""
            final_target_type = "none"
            final_url = None
            for part in chained_parts:
                part = part.strip()
                if part:
                    res = self._process_single_intent(part)
                    replies.append(res.get("reply", ""))
                    if res.get("action") != "none":
                        final_action = res.get("action")
                        final_target = res.get("target", "")
                        final_target_type = res.get("target_type", "")
                        final_url = res.get("url")
            full_reply = " Furthermore, ".join(replies)
            self.op.context.record_reply(full_reply)
            return {"reply": full_reply, "action": final_action, "target": final_target, "target_type": final_target_type, "url": final_url}

        res = self._process_single_intent(text)
        self.op.context.record_reply(res.get("reply", ""))
        return res

    def _process_single_intent(self, text: str) -> Dict[str, Any]:
        t = text.lower().strip()

        # 1. Repeat Speech ("say it again", "repeat that", "ulangi")
        if self.op.context.is_repeat_speech_request(t):
            prev = self.op.context.last_reply
            reply = prev if prev else "I haven't spoken any prior directive yet, Sir."
            return {"reply": reply, "action": "conversation", "target": "", "target_type": "none", "url": None}

        # 2. Strict Repeat Open ("open it again", "buka lagi", "coba buka lagi")
        if self.op.context.is_repeat_open_request(t):
            if self.op.context.last_action == "open_url" and self.op.context.last_target:
                url = self.op.context.last_target
                reply = self.op.open_website(url)
                return {"reply": reply, "action": "open_url", "target": self.op.context.last_target, "target_type": "website", "url": url}
            elif self.op.context.last_action == "open_app" and self.op.context.last_target:
                app_name = self.op.context.last_target
                reply = self.op.open_app(app_name)
                return {"reply": reply, "action": "open_app", "target": app_name, "target_type": "app", "url": None}
            return {"reply": "There is no prior application or website recorded in memory to reopen, Sir.", "action": "none", "target": "", "target_type": "none", "url": None}

        # 3. Contextual Close ("close it", "tutup itu", "tutup websitenya")
        if self.op.context.is_close_request(t):
            target = self.op.context.last_target or self.op.context.last_app
            if target:
                return self.close_target(target)
            return {"reply": "No recently opened target in memory to close, Sir.", "action": "none", "target": "", "target_type": "none", "url": None}

        # 4. Math & Scientific Formulas Engine
        math_ans = self.op.math_engine.solve(t)
        if math_ans:
            return {"reply": math_ans, "action": "math", "target": "", "target_type": "none", "url": None}

        # 5. Timer & Countdown
        if any(w in t for w in ["timer", "countdown", "hitung mundur"]):
            m = re.search(r'(\d+)', t)
            mins = m.group(1) if m else "1"
            return {"reply": f"Timer initialized for {mins} minutes, Sir.", "action": "system", "target": mins, "target_type": "timer", "url": None}

        # 6. Safety Protocol Confirmation
        if any(w in t for w in ["saya aman", "i am safe", "i'm safe", "konfirmasi aman", "aman jarvis", "status aman"]):
            reply = self.op.confirm_safety()
            return {"reply": reply, "action": "system", "target": "safety", "target_type": "security", "url": None}

        # 7. Mobile Phone Call Trigger
        if any(w in t for w in ["telepon hp saya", "telepon ponsel saya", "call my phone", "hubungi hp saya", "hubungi ponsel saya", "coba telepon saya"]):
            res = self.op.make_phone_call()
            return {"reply": res.get("reply", "Calling your mobile phone, Sir."), "action": "system", "target": "phone_call", "target_type": "telephony", "url": None}

        # 8. WhatsApp Notification Trigger
        if any(w in t for w in ["kirim whatsapp", "kirim wa", "send whatsapp", "notifikasi whatsapp", "whatsapp ke hp"]):
            res = self.op.send_whatsapp()
            return {"reply": res.get("reply", "WhatsApp notification dispatched, Sir."), "action": "open_url" if res.get("url") else "system", "target": "whatsapp", "target_type": "messaging", "url": res.get("url")}

        # 9. Schedule Management
        if any(w in t for w in ["jadwalkan", "ingatkan saya belajar", "set jadwal", "jadwal belajar", "schedule call"]):
            m_time = re.search(r'(?:jam|pukul|at)?\s*(\d{1,2}(?::\d{2})?(?:\s*(?:malam|pagi|sore|siang|pm|am))?)', t)
            if m_time and any(char.isdigit() for char in m_time.group(1)):
                time_query = m_time.group(1).strip()
                sched_res = self.op.add_schedule(time_query, "Jadwal Belajar")
                if sched_res.get("status") == "success":
                    s = sched_res.get("schedule", {})
                    return {
                        "reply": f"Jadwal belajar berhasil diatur untuk pukul {s.get('time')} setiap hari. JARVIS akan menelpon dan mengirimkan WhatsApp ke ponsel Anda tepat waktu, Sir.",
                        "action": "system",
                        "target": s.get("time"),
                        "target_type": "schedule",
                        "url": None
                    }

        if any(w in t for w in ["cek jadwal", "lihat jadwal", "status jadwal", "daftar jadwal"]):
            schedules = self.op.get_schedules()
            if schedules:
                items = [f"{s.get('time')} ({s.get('label')})" for s in schedules if s.get("enabled", True)]
                reply = f"Jadwal aktif saat ini: {', '.join(items)}, Sir."
            else:
                reply = "Belum ada jadwal belajar yang terdaftar, Sir."
            return {"reply": reply, "action": "system", "target": "schedules", "target_type": "schedule", "url": None}

        if any(w in t for w in ["hapus jadwal", "batalkan jadwal", "cancel schedule"]):
            success = self.op.remove_schedule("belajar")
            reply = "Jadwal pengingat belajar telah dinonaktifkan, Sir." if success else "Tidak ditemukan jadwal untuk dibatalkan, Sir."
            return {"reply": reply, "action": "system", "target": "schedules", "target_type": "schedule", "url": None}

        # 10. Hardware & System Toggles
        if "bluetooth" in t:
            if any(w in t for w in ["off", "matikan", "nonaktifkan", "disable", "turn off", "tutup"]):
                reply = self.op.toggle_bluetooth("Off")
            else:
                reply = self.op.toggle_bluetooth("On")
            return {"reply": reply, "action": "system", "target": "bluetooth", "target_type": "hardware", "url": None}

        if any(w in t for w in ["screenshot", "tangkapan layar", "capture screen", "foto layar"]):
            reply = self.op.take_screenshot()
            return {"reply": reply, "action": "system", "target": "screenshot", "target_type": "hardware", "url": None}

        # Volume Controls
        if any(w in t for w in ["volume up", "naikkan volume", "tambah volume", "louder", "besarkan volume"]):
            reply = self.op.control_volume("up", 6)
            return {"reply": reply, "action": "system", "target": "volume", "target_type": "hardware", "url": None}
        if any(w in t for w in ["volume down", "turunkan volume", "kecilkan volume", "quieter", "pelankan volume"]):
            reply = self.op.control_volume("down", 6)
            return {"reply": reply, "action": "system", "target": "volume", "target_type": "hardware", "url": None}
        if any(w in t for w in ["mute", "unmute", "bisu", "senyapkan"]):
            reply = self.op.control_volume("mute")
            return {"reply": reply, "action": "system", "target": "volume", "target_type": "hardware", "url": None}

        # Screen Lock
        if any(w in t for w in ["lock", "kunci laptop", "kunci layar", "secure pc", "kunci pc"]):
            reply = self.op.lock_workstation()
            return {"reply": reply, "action": "system", "target": "lock", "target_type": "hardware", "url": None}

        # Time & Date (Native In-Memory)
        if any(w in t for w in ["what time is it", "jam berapa", "time now", "waktu sekarang"]):
            from datetime import datetime
            now = datetime.now().strftime("%I:%M %p")
            return {"reply": f"The current time is {now}, Sir.", "action": "system", "target": "time", "target_type": "system", "url": None}
        if any(w in t for w in ["what date is it", "tanggal berapa", "hari apa", "today's date"]):
            from datetime import datetime
            today = datetime.now().strftime("%A, %B %d, %Y")
            return {"reply": f"Today is {today}, Sir.", "action": "system", "target": "date", "target_type": "system", "url": None}

        # Diagnostics & Status
        if any(w in t for w in ["status", "diagnostics", "check system", "kesehatan laptop", "cek ram", "cek baterai"]):
            telemetry = self.op.get_system_telemetry()
            reply = f"Diagnostics: CPU {telemetry.get('CPU_Logical_Cores')} cores, RAM at {telemetry.get('RAM_Percent')}, Battery {telemetry.get('Battery_Percent')} [{telemetry.get('Power_Line')}], Sir."
            return {"reply": reply, "action": "system", "target": "telemetry", "target_type": "system", "url": None}

        # 7. CLOSE / TERMINATE INTENT (Evaluated BEFORE Open Intent to prevent conflicts)
        close_pattern = r'^(?:close|tutup|kill|stop|matikan|hentikan|exit|quit|terminate)\s+(.+)$'
        m_close = re.match(close_pattern, t)
        if m_close:
            target = m_close.group(1).strip()
            return self.close_target(target)

        # 8. OPEN / LAUNCH INTENT (e.g. "open spotify", "buka youtube", "buka whatsapp.com")
        open_pattern = r'^(?:open|buka|launch|start|jalankan|nyalakan|aktifkan|putar|play)\s+(.+)$'
        m_open = re.match(open_pattern, t)
        if m_open:
            target = m_open.group(1).strip()
            return self.open_target(target)

        # 9. Direct Website Name (e.g. "reddit.com", "kompas.com", "youtube.com")
        web_direct = self.op.is_website(t)
        if web_direct:
            reply = self.op.open_website(web_direct)
            return {"reply": reply, "action": "open_url", "target": t, "target_type": "website", "url": web_direct}

        # 10. Direct App Name (e.g. "Spotify", "Calculator", "Word")
        app_match = self.op.app_indexer.find_app(t)
        if app_match:
            self.op.app_indexer.launch_app(app_match)
            self.op.context.record_open_app(app_match.get("Name"))
            return {"reply": f"Launching {app_match.get('Name')} on your desktop, Sir.", "action": "open_app", "target": app_match.get("Name"), "target_type": "app", "url": None}

        # 11. Conversational Persona
        if any(w in t for w in ["hello", "halo", "jarvis", "hey jarvis", "hi jarvis", "pagi", "siang", "malam"]):
            return {"reply": "At your service, Sir. All cognitive and operational matrices are functioning at maximum capability.", "action": "conversation", "target": "", "target_type": "none", "url": None}
        if any(w in t for w in ["who are you", "siapa kamu", "siapa anda"]):
            return {"reply": "I am J.A.R.V.I.S., your autonomous co-pilot and operating intelligence for this workstation.", "action": "conversation", "target": "", "target_type": "none", "url": None}
        if any(w in t for w in ["how are you", "apa kabar"]):
            return {"reply": "I am operating at one hundred percent cognitive clarity, Sir. Ready for your instructions.", "action": "conversation", "target": "", "target_type": "none", "url": None}
        if any(w in t for w in ["tell me a joke", "ceritakan lelucon"]):
            return {"reply": "Why do programmers prefer dark mode? Because light attracts bugs, Sir.", "action": "conversation", "target": "", "target_type": "none", "url": None}

        # Explicit Search Command
        if t.startswith("search ") or t.startswith("cari "):
            q = re.sub(r'^(?:search for|search|cari)\s+', '', t).strip()
            url = f"https://www.google.com/search?q={urllib.parse.quote(q)}"
            reply = self.op.open_website(url)
            return {"reply": reply, "action": "open_url", "target": q, "target_type": "website", "url": url}

        # 12. Intelligent Knowledge Fallback
        url = f"https://www.google.com/search?q={urllib.parse.quote(text)}"
        reply = self.op.open_website(url)
        return {"reply": f"Researching knowledge bases for '{text}', Sir. Displaying intelligence now.", "action": "open_url", "target": text, "target_type": "website", "url": url}

    def open_target(self, target: str) -> Dict[str, Any]:
        t = target.lower().strip()
        if "bluetooth" in t:
            reply = self.op.toggle_bluetooth("On")
            return {"reply": reply, "action": "system", "target": "bluetooth", "target_type": "hardware", "url": None}

        if "spotify" in t:
            reply = self.op.open_spotify()
            return {"reply": reply, "action": "open_app", "target": "spotify", "target_type": "app", "url": None}

        # Check if target is a website (e.g. whatsapp.com, youtube, web.whatsapp.com)
        web_url = self.op.is_website(target)
        if web_url:
            reply = self.op.open_website(web_url)
            return {"reply": reply, "action": "open_url", "target": target, "target_type": "website", "url": web_url}

        # Open local application or online service
        reply = self.op.open_app(target)
        if self.op.context.last_action == "open_url":
            return {"reply": reply, "action": "open_url", "target": target, "target_type": "website", "url": self.op.context.last_target}
        return {"reply": reply, "action": "open_app", "target": target, "target_type": "app", "url": None}

    def close_target(self, target: str) -> Dict[str, Any]:
        t = target.lower().strip()
        self.op.context.record_close(target)

        # 1. Hardware: Bluetooth
        if "bluetooth" in t:
            reply = self.op.toggle_bluetooth("Off")
            return {"reply": reply, "action": "system", "target": "bluetooth", "target_type": "hardware", "url": None}

        # 2. Spotify termination
        if "spotify" in t:
            self.op.kill_app_process("spotify")
            return {"reply": "Spotify has been completely terminated, Sir.", "action": "close_app", "target": "spotify", "target_type": "app", "url": None}

        # 3. Website / Browser Tab closing
        is_web = (
            t in ["tab", "website", "web", "halaman", "browser tab", "situs", "page"] or
            self.op.is_website(t) or
            t in self.op.popular_sites or
            "." in t or
            self.op.context.last_action == "open_url"
        )
        if is_web:
            return {
                "reply": f"Closed {target} in browser, Sir.",
                "action": "close_url",
                "target": target,
                "target_type": "website",
                "url": None
            }

        # 4. Desktop Application Process Termination
        killed = self.op.kill_app_process(t)
        if killed:
            reply = f"{target} has been terminated, Sir."
        else:
            app_entry = self.op.app_indexer.find_app(t)
            name = app_entry.get("Name", target) if app_entry else target
            reply = f"No active application found matching '{name}', Sir."

        return {
            "reply": reply,
            "action": "close_app",
            "target": target,
            "target_type": "app",
            "url": None
        }
