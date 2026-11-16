"""
Context Memory Module for JARVIS
Stores short-term conversation state with precise intent discrimination.
Prevents unintended repeats or context bleeding.
"""

import re
from typing import Optional

class ContextMemory:
    def __init__(self):
        self.last_action: Optional[str] = None
        self.last_target: Optional[str] = None
        self.last_app: Optional[str] = None
        self.last_website: Optional[str] = None
        self.last_reply: Optional[str] = None

    def record_open_app(self, app_name: str):
        self.last_action = "open_app"
        self.last_target = app_name
        self.last_app = app_name
        self.last_website = None

    def record_open_website(self, url: str):
        self.last_action = "open_url"
        self.last_target = url
        self.last_website = url
        self.last_app = None

    def record_close(self, target: str):
        self.last_action = "close"
        self.last_target = target
        self.last_app = None
        self.last_website = None

    def record_reply(self, reply: str):
        self.last_reply = reply

    def is_repeat_open_request(self, text: str) -> bool:
        """Strict regex matching for opening the previous target again."""
        t = text.lower().strip()
        patterns = [
            r'^(?:open|launch|run)\s+(?:it|that|the app|the site|the website|app|site)\s+again$',
            r'^(?:open|launch|run)\s+again$',
            r'^(?:reopen|re-open)(?:\s+(?:it|that))?$',
            r'^buka\s+(?:lagi|kembali|sekali lagi)$',
            r'^buka\s+(?:itu|yang tadi|aplikasinya|websitenya|aplikasi tadi|web tadi)\s+lagi$',
            r'^coba\s+buka\s+lagi$',
            r'^jalankan\s+lagi$',
            r'^putar\s+lagi$'
        ]
        return any(re.match(p, t) for p in patterns)

    def is_repeat_speech_request(self, text: str) -> bool:
        """Strict matching for asking JARVIS to repeat what it said."""
        t = text.lower().strip()
        patterns = [
            r'^(?:say|repeat|tell)\s+(?:it|that)\s+again$',
            r'^repeat(?:\s+that)?$',
            r'^what\s+did\s+you\s+say$',
            r'^(?:ulangi|bicara lagi|katakan lagi)(?:\s+(?:dong|lagi|sekali lagi))?$',
            r'^apa\s+katamu$'
        ]
        return any(re.match(p, t) for p in patterns)

    def is_close_request(self, text: str) -> bool:
        """Strict matching for contextual close (e.g. close it, tutup itu)."""
        t = text.lower().strip()
        patterns = [
            r'^(?:close|tutup|kill|stop|terminate)\s+(?:it|that|the app|the site|the website|aplikasi|itu|websitenya)$',
            r'^(?:close|tutup|matikan)\s+(?:aplikasi\s+tadi|web\s+tadi)$',
            r'^close$',
            r'^tutup$'
        ]
        return any(re.match(p, t) for p in patterns)
