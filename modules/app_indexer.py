"""
App Indexer Module for JARVIS
Dynamically indexes and resolves all applications installed on the Windows PC.
"""

import subprocess
import json
import os
from typing import Optional, Dict, List

class AppIndexer:
    def __init__(self, cache_file: str = None):
        if not cache_file:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cache_file = os.path.join(base_dir, "data", "installed_apps.json")
        self.cache_file = cache_file
        self.apps = []
        self.load_or_index_apps()

    def index_apps(self) -> List[Dict[str, str]]:
        """Fetch all installed applications using Windows Get-StartApps."""
        try:
            cmd = "Get-StartApps | Select-Object Name, AppID | ConvertTo-Json -Depth 2"
            res = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                capture_output=True,
                text=True,
                timeout=15
            )
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                if isinstance(data, list):
                    self.apps = data
                elif isinstance(data, dict):
                    self.apps = [data]
                
                # Save cache
                os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
                with open(self.cache_file, "w", encoding="utf-8") as f:
                    json.dump(self.apps, f, indent=2)
                return self.apps
        except Exception as e:
            print(f"[AppIndexer] Index error: {e}")
        return []

    def load_or_index_apps(self):
        """Load from cache file if exists, otherwise index fresh."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self.apps = json.load(f)
                if self.apps:
                    return
            except Exception:
                pass
        self.index_apps()

    def find_app(self, query: str) -> Optional[Dict[str, str]]:
        """Fuzzy match application name."""
        q = query.lower().strip()
        if not q or not self.apps:
            return None

        # 1. Exact match
        for app in self.apps:
            name = app.get("Name", "").lower()
            if name == q:
                return app

        # 2. Starts with match
        for app in self.apps:
            name = app.get("Name", "").lower()
            if name.startswith(q):
                return app

        # 3. Substring match
        for app in self.apps:
            name = app.get("Name", "").lower()
            if q in name:
                return app

        # 4. Word boundary / acronym match
        for app in self.apps:
            name = app.get("Name", "").lower()
            words = name.split()
            if any(w == q for w in words):
                return app

        return None

    def launch_app(self, app_entry: Dict[str, str]) -> bool:
        """Launch app instantly using non-blocking explorer shell:AppsFolder."""
        app_id = app_entry.get("AppID")
        if not app_id:
            return False
        
        try:
            # Ultra-fast non-blocking spawn (<10ms)
            subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app_id}"])
            return True
        except Exception:
            return False

if __name__ == "__main__":
    idx = AppIndexer()
    print(f"Total indexed apps: {len(idx.apps)}")
    for test in ["spotify", "word", "bluestacks", "arduino", "calculator"]:
        found = idx.find_app(test)
        print(f"Query '{test}' -> {found.get('Name') if found else 'Not found'}")

