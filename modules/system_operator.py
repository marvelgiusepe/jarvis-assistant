"""
JARVIS Autonomous System Operator
Universal Windows App Launcher, Universal Website Opener, Contextual Memory,
Advanced Math Engine, Real-Time Hardware Diagnostics, and Intelligent Knowledge Handler.
"""

import subprocess
import os
import sys
import json
import re
import urllib.parse
from datetime import datetime
from typing import Dict, Any, Optional, List

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

from modules.app_indexer import AppIndexer
from modules.math_engine import MathEngine
from modules.context_memory import ContextMemory
from modules.phone_caller import PhoneCaller
from modules.whatsapp_notifier import WhatsAppNotifier
from modules.safety_protocol import SafetyProtocol
from modules.scheduler import JarvisScheduler

class SystemOperator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.screenshots_dir = os.path.join(self.base_dir, "screenshots")
        self.scripts_dir = os.path.join(self.base_dir, "scripts")
        os.makedirs(self.screenshots_dir, exist_ok=True)
        os.makedirs(self.scripts_dir, exist_ok=True)

        self.app_indexer = AppIndexer()
        self.math_engine = MathEngine()
        self.context = ContextMemory()
        self.phone_caller = PhoneCaller()
        self.whatsapp_notifier = WhatsAppNotifier()
        self.safety = SafetyProtocol()
        self.scheduler = JarvisScheduler()
        self.scheduler.start()

        self.popular_sites = {
            "youtube": "https://www.youtube.com",
            "youtube.com": "https://www.youtube.com",
            "google": "https://www.google.com",
            "google.com": "https://www.google.com",
            "github": "https://www.github.com",
            "github.com": "https://www.github.com",
            "spotify": "https://open.spotify.com",
            "spotify.com": "https://open.spotify.com",
            "chatgpt": "https://chatgpt.com",
            "chatgpt.com": "https://chatgpt.com",
            "claude": "https://claude.ai",
            "reddit": "https://www.reddit.com",
            "reddit.com": "https://www.reddit.com",
            "twitter": "https://twitter.com",
            "twitter.com": "https://twitter.com",
            "x": "https://x.com",
            "x.com": "https://x.com",
            "instagram": "https://www.instagram.com",
            "instagram.com": "https://www.instagram.com",
            "facebook": "https://www.facebook.com",
            "facebook.com": "https://www.facebook.com",
            "netflix": "https://www.netflix.com",
            "netflix.com": "https://www.netflix.com",
            "wikipedia": "https://www.wikipedia.org",
            "wikipedia.org": "https://www.wikipedia.org",
            "amazon": "https://www.amazon.com",
            "amazon.com": "https://www.amazon.com",
            "tokopedia": "https://www.tokopedia.com",
            "tokopedia.com": "https://www.tokopedia.com",
            "shopee": "https://www.shopee.co.id",
            "shopee.co.id": "https://www.shopee.co.id",
            "kompas": "https://www.kompas.com",
            "kompas.com": "https://www.kompas.com",
            "detik": "https://www.detik.com",
            "detik.com": "https://www.detik.com",
            "tiktok": "https://www.tiktok.com",
            "tiktok.com": "https://www.tiktok.com",
            "twitch": "https://www.twitch.tv",
            "twitch.tv": "https://www.twitch.tv",
            "discord": "https://discord.com/app",
            "discord.com": "https://discord.com/app",
            "whatsapp": "https://web.whatsapp.com",
            "whatsapp.com": "https://web.whatsapp.com",
            "web.whatsapp.com": "https://web.whatsapp.com",
            "medium": "https://medium.com",
            "linkedin": "https://www.linkedin.com",
            "linkedin.com": "https://www.linkedin.com",
            "stackoverflow": "https://stackoverflow.com",
            "stackoverflow.com": "https://stackoverflow.com",
            "gemini": "https://gemini.google.com",
            "canva": "https://www.canva.com",
            "canva.com": "https://www.canva.com",
            "figma": "https://www.figma.com",
            "figma.com": "https://www.figma.com",
            "gmail": "https://mail.google.com",
            "drive": "https://drive.google.com",
            "maps": "https://maps.google.com",
            "roblox": "https://www.roblox.com",
            "roblox.com": "https://www.roblox.com",
            "chess": "https://www.chess.com",
            "chess.com": "https://www.chess.com"
        }

    def run_ps(self, cmd: str) -> str:
        """Execute a PowerShell command safely and return output."""
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                capture_output=True,
                text=True,
                timeout=15
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"

    def get_system_telemetry(self) -> Dict[str, Any]:
        """Fetch real-time CPU threads, RAM, Disks, and Battery status via .NET."""
        ps_script = """
        Add-Type -AssemblyName Microsoft.VisualBasic
        Add-Type -AssemblyName System.Windows.Forms

        $computer = New-Object Microsoft.VisualBasic.Devices.ComputerInfo
        $totalRamGB = [math]::Round($computer.TotalPhysicalMemory / 1GB, 2)
        $availRamGB = [math]::Round($computer.AvailablePhysicalMemory / 1GB, 2)
        $usedRamGB = [math]::Round($totalRamGB - $availRamGB, 2)
        $ramPercent = [math]::Round(($usedRamGB / $totalRamGB) * 100, 1)

        $power = [System.Windows.Forms.SystemInformation]::PowerStatus
        $batPercent = [math]::Round($power.BatteryLifePercent * 100)
        $powerStatus = $power.PowerLineStatus.ToString()

        $cpuCores = [System.Environment]::ProcessorCount

        $drives = [System.IO.DriveInfo]::GetDrives() | Where-Object { $_.IsReady } | ForEach-Object {
            [PSCustomObject]@{
                Drive = $_.Name
                TotalGB = [math]::Round($_.TotalSize / 1GB, 1)
                FreeGB = [math]::Round($_.TotalFreeSpace / 1GB, 1)
                UsedGB = [math]::Round(($_.TotalSize - $_.TotalFreeSpace) / 1GB, 1)
            }
        }

        [PSCustomObject]@{
            CPU_Logical_Cores = $cpuCores
            RAM_Used_GB = $usedRamGB
            RAM_Total_GB = $totalRamGB
            RAM_Percent = "$ramPercent%"
            Battery_Percent = "$batPercent%"
            Power_Line = $powerStatus
            Drives = $drives
            Timestamp = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
        } | ConvertTo-Json -Depth 3
        """
        raw = self.run_ps(ps_script)
        try:
            return json.loads(raw)
        except Exception:
            return {"error": "Failed to parse telemetry", "raw": raw}

    def is_website(self, text: str) -> Optional[str]:
        """Check if target string is a website name, domain, or known site."""
        t = text.lower().strip()
        t = re.sub(r'^(open site|open website|buka web|buka website|buka situs|go to|buka|open)\s+', '', t).strip()

        # Direct match in popular sites
        if t in self.popular_sites:
            return self.popular_sites[t]

        # Explicit website directive: "website kompas" -> "kompas"
        m_web_prefix = re.match(r'^(?:website|web|situs)\s+(.+)$', t)
        if m_web_prefix:
            domain_name = m_web_prefix.group(1).strip()
            if domain_name in self.popular_sites:
                return self.popular_sites[domain_name]
            if not "." in domain_name:
                return f"https://www.{domain_name}.com"
            return f"https://{domain_name}" if not domain_name.startswith("http") else domain_name

        # Domain extensions check (.com, .org, .net, .id, etc.)
        tld_pattern = r'^[a-zA-Z0-9\-\.]+\.(com|org|net|id|co\.id|io|co|ai|dev|app|edu|gov|xyz|tv|gg|me|info|biz|site)$'
        if re.search(tld_pattern, t):
            if not t.startswith("http"):
                return f"https://{t}"
            return t

        return None

    def open_website(self, url: str, spawn_os: bool = False) -> str:
        """
        Record context for opening web URL.
        By default spawn_os=False so client HUD opens the tab via window.open,
        preventing duplicate (2x) tabs from opening.
        """
        if not url.startswith("http"):
            url = f"https://{url}"

        if spawn_os:
            try:
                if hasattr(os, 'startfile'):
                    os.startfile(url)
                else:
                    subprocess.Popen(['cmd.exe', '/c', 'start', '', url], shell=True)
            except Exception:
                try:
                    subprocess.Popen(['cmd.exe', '/c', 'start', '', url], shell=True)
                except Exception:
                    self.run_ps(f'Start-Process "{url}"')

        self.context.record_open_website(url)
        domain = urllib.parse.urlparse(url).netloc or url
        return f"Opening {domain} in your browser, Sir."

    def open_spotify(self) -> str:
        """
        Launch or focus Spotify cleanly.
        If already running, activates its window to prevent
        'The Spotify application is not responding' mutex dialog.
        """
        import ctypes
        user32 = ctypes.windll.user32

        # Fast Win32 window check
        found_hwnd = [0]
        def enum_cb(hwnd, lparam):
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buf = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buf, length + 1)
                    title = buf.value.lower()
                    if "spotify" in title:
                        found_hwnd[0] = hwnd
                        return False
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        cb_func = WNDENUMPROC(enum_cb)
        user32.EnumWindows(cb_func, 0)

        if found_hwnd[0] != 0:
            SW_RESTORE = 9
            user32.ShowWindow(found_hwnd[0], SW_RESTORE)
            user32.SetForegroundWindow(found_hwnd[0])
            self.context.record_open_app("Spotify")
            return "Spotify is now active on your screen, Sir."

        # Otherwise launch fresh
        try:
            subprocess.Popen(["explorer.exe", "shell:AppsFolder\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify"])
        except Exception:
            self.run_ps('explorer.exe "shell:AppsFolder\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify"')

        self.context.record_open_app("Spotify")
        return "Launching Spotify on your desktop, Sir."

    def open_app(self, app_name: str) -> str:
        """Universal Windows App Launcher with fuzzy matching and safety checks."""
        target = app_name.strip()
        t_lower = target.lower()

        # 1. Check for pronoun / repeat requests (NEVER launch an app named 'it' or 'it again')
        pronoun_words = ["it", "that", "this", "it again", "again", "lagi", "tadi", "itu", "yang tadi", "aplikasi tadi"]
        if t_lower in pronoun_words:
            if self.context.last_target:
                if self.context.last_action == "open_url":
                    return self.open_website(self.context.last_target)
                elif self.context.last_action == "open_app":
                    return self.open_app(self.context.last_target)
            return "No prior application or website recorded in memory to reopen, Sir."

        # 2. Check if explicitly a domain extension (e.g. whatsapp.com, youtube.com, reddit.com)
        web_match = self.is_website(target)
        if web_match:
            return self.open_website(web_match)

        # 3. Check special case: Spotify
        if "spotify" in t_lower:
            return self.open_spotify()

        # 4. Search local desktop applications (243+ indexed Windows apps)
        app_entry = self.app_indexer.find_app(target)
        if app_entry:
            self.app_indexer.launch_app(app_entry)
            name = app_entry.get("Name", target)
            self.context.record_open_app(name)
            return f"Launching {name} on your desktop, Sir."

        # 5. If not a local app, check if it could be a known web platform or search
        # E.g. "buka roblox" -> opens roblox.com if not installed locally
        guessed_url = f"https://www.{re.sub(r'[^a-zA-Z0-9]', '', t_lower)}.com"
        try:
            if hasattr(os, 'startfile'):
                os.startfile(guessed_url)
            else:
                subprocess.Popen(['cmd.exe', '/c', 'start', '', guessed_url], shell=True)
            self.context.record_open_website(guessed_url)
            return f"No local application found for '{target}', Sir. Opening online portal at {guessed_url}."
        except Exception:
            pass

        return f"Unable to find application or destination '{target}', Sir."

    def toggle_bluetooth(self, action: str = "On") -> str:
        """Toggle Windows Bluetooth radio directly via WinRT script."""
        script_path = os.path.join(self.scripts_dir, "toggle_bluetooth.ps1")
        cmd = f'powershell -ExecutionPolicy Bypass -File "{script_path}" -Action "{action}"'
        self.run_ps(cmd)
        if "Off" in action:
            return "Bluetooth radio has been disabled, Sir."
        return "Bluetooth has been turned on and activated, Sir."

    def take_screenshot(self) -> str:
        """Capture screen using PowerShell/.NET and automatically open the result."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.screenshots_dir, f"screenshot_{ts}.png")

        ps_script = f"""
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
        $bitmap.Save('{output_path}', [System.Drawing.Imaging.ImageFormat]::Png)
        $graphics.Dispose()
        $bitmap.Dispose()
        Start-Process '{output_path}'
        """
        self.run_ps(ps_script)
        if os.path.exists(output_path):
            return "Screenshot captured and opened on your screen, Sir."
        return "Screenshot buffer was triggered, Sir."

    def control_volume(self, action: str, steps: int = 5) -> str:
        """Control master volume instantly via native Win32 ctypes keybd_event."""
        import ctypes
        action = action.lower()
        VK_VOLUME_MUTE = 0xAD
        VK_VOLUME_DOWN = 0xAE
        VK_VOLUME_UP = 0xAF

        if action == "mute":
            ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 2, 0)
            return "Audio muted/unmuted, Sir."
        elif action in ["up", "down"]:
            vk = VK_VOLUME_UP if action == "up" else VK_VOLUME_DOWN
            for _ in range(steps):
                ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
                ctypes.windll.user32.keybd_event(vk, 0, 2, 0)
            return f"Volume adjusted {action} by {steps} increments, Sir."
        return "Unknown volume action."

    def lock_workstation(self) -> str:
        """Lock the PC screen instantly via Win32 ctypes LockWorkStation."""
        import ctypes
        ctypes.windll.user32.LockWorkStation()
        return "Workstation secured and locked, Sir."

    def kill_app_process(self, app_name: str) -> bool:
        """
        Kill an application cleanly using exact executable mappings,
        taskkill, and PowerShell process inspection.
        Returns True if process was found and terminated, False otherwise.
        """
        target = app_name.lower().strip()

        # Known process executable mappings
        exe_map = {
            "spotify": ["Spotify.exe", "SpotifyLauncher.exe"],
            "word": ["WINWORD.EXE"],
            "ms word": ["WINWORD.EXE"],
            "microsoft word": ["WINWORD.EXE"],
            "excel": ["EXCEL.EXE"],
            "ms excel": ["EXCEL.EXE"],
            "powerpoint": ["POWERPNT.EXE"],
            "ppt": ["POWERPNT.EXE"],
            "notepad": ["notepad.exe"],
            "calculator": ["CalculatorApp.exe", "calc.exe", "Calculator.exe"],
            "calc": ["CalculatorApp.exe", "calc.exe"],
            "chrome": ["chrome.exe"],
            "google chrome": ["chrome.exe"],
            "edge": ["msedge.exe"],
            "microsoft edge": ["msedge.exe"],
            "bluestacks": ["HD-Player.exe", "BlueStacks.exe"],
            "vlc": ["vlc.exe"],
            "discord": ["Discord.exe"],
            "telegram": ["Telegram.exe"],
            "steam": ["steam.exe"],
            "task manager": ["Taskmgr.exe"],
            "taskmgr": ["Taskmgr.exe"],
            "cmd": ["cmd.exe"],
            "terminal": ["WindowsTerminal.exe", "wt.exe"],
            "powershell": ["powershell.exe"],
            "paint": ["mspaint.exe"],
            "7-zip": ["7zFM.exe"],
            "arduino": ["arduino.exe", "Arduino IDE.exe"]
        }

        # 1. Check mapped executables
        if target in exe_map:
            killed = False
            for exe in exe_map[target]:
                res = subprocess.run(
                    ["taskkill", "/F", "/IM", exe],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if res.returncode == 0:
                    killed = True
            if killed:
                return True

        # 2. Try indexed app matching
        app_entry = self.app_indexer.find_app(target)
        if app_entry:
            app_id = app_entry.get("AppID", "")
            if app_id.lower().endswith(".exe"):
                exe_name = os.path.basename(app_id)
                res = subprocess.run(
                    ["taskkill", "/F", "/IM", exe_name],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if res.returncode == 0:
                    return True

        # 3. Try direct name.exe
        res = subprocess.run(
            ["taskkill", "/F", "/IM", f"{target}.exe"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if res.returncode == 0:
            return True

        # 4. PowerShell fuzzy search by MainWindowTitle and ProcessName
        ps_script = f"""
        $procs = Get-Process | Where-Object {{
            $_.ProcessName -like "*{target}*" -or $_.MainWindowTitle -like "*{target}*"
        }}
        if ($procs) {{
            $procs | Stop-Process -Force
            Write-Output "TERMINATED"
        }}
        """
        raw = self.run_ps(ps_script)
        return "TERMINATED" in raw

    def close_active_tab(self) -> str:
        """Focus browser window and send Ctrl+W to close active browser tab."""
        import ctypes
        import time
        user32 = ctypes.windll.user32

        # Find visible browser window
        browser_hwnds = []
        def enum_cb(hwnd, lparam):
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buf = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buf, length + 1)
                    t = buf.value.lower()
                    if any(b in t for b in ["chrome", "edge", "brave", "firefox"]):
                        browser_hwnds.append(hwnd)
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        cb_func = WNDENUMPROC(enum_cb)
        user32.EnumWindows(cb_func, 0)

        if browser_hwnds:
            SW_RESTORE = 9
            user32.ShowWindow(browser_hwnds[0], SW_RESTORE)
            user32.SetForegroundWindow(browser_hwnds[0])
            time.sleep(0.05)

        VK_CONTROL = 0x11
        VK_W = 0x57
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        user32.keybd_event(VK_W, 0, 0, 0)
        user32.keybd_event(VK_W, 0, 2, 0)
        user32.keybd_event(VK_CONTROL, 0, 2, 0)
        return "Browser tab closed, Sir."

    def make_phone_call(self, to_number: str = None, message: str = None) -> Dict[str, Any]:
        """Trigger voice phone call to user's mobile."""
        return self.phone_caller.make_call(to_number, message)

    def send_whatsapp(self, to_number: str = None, message: str = None) -> Dict[str, Any]:
        """Send automated WhatsApp notification to user's mobile."""
        return self.whatsapp_notifier.send_whatsapp(to_number, message)

    def confirm_safety(self) -> str:
        """Confirm user is safe and clear alert window."""
        return self.safety.confirm_safe()

    def get_safety_status(self) -> Dict[str, Any]:
        return self.safety.get_status()

    def get_schedules(self) -> List[Dict[str, Any]]:
        return self.scheduler.get_schedules()

    def add_schedule(self, time_str: str, label: str = "Jadwal Belajar") -> Dict[str, Any]:
        return self.scheduler.add_schedule(time_str, label)

    def remove_schedule(self, query: str) -> bool:
        return self.scheduler.remove_schedule(query)

    def parse_and_execute(self, command_text: str) -> Dict[str, Any]:
        """Forward all natural language processing to the CognitiveBrain."""
        if not hasattr(self, 'brain'):
            from modules.cognitive_brain import CognitiveBrain
            self.brain = CognitiveBrain(self)
        return self.brain.analyze_and_execute(command_text)

if __name__ == "__main__":
    op = SystemOperator()
    print("Test Spotify:", op.parse_and_execute("open spotify"))
    print("Test Repeat Open:", op.parse_and_execute("open it again"))
    print("Test Close Spotify:", op.parse_and_execute("close spotify"))
    print("Test WhatsApp Web:", op.parse_and_execute("buka whatsapp.com"))
    print("Test Math:", op.parse_and_execute("500 times 8"))
