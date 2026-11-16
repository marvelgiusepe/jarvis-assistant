"""
JARVIS Core Console Interface
Autonomous Assistant Controller for Windows
"""

import sys
import os
import json
import time

# Ensure modules folder is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.system_operator import SystemOperator
from modules.voice_engine import VoiceEngine

BANNER = r"""
   ╦╔═╗╦═╗╦  ╦╦╔═╗
   ║╠═╣╠╦╝╚╗╔╝║╚═╗
  ╚╝╩ ╩╩╚═ ╚╝ ╩╚═╝
  SYSTEM ONLINE // CO-PILOT ACTIVE
"""

class JarvisCore:
    def __init__(self):
        self.sys_op = SystemOperator()
        self.voice = VoiceEngine()

    def boot(self):
        print(BANNER)
        print("[*] Initializing subsystem protocols...")
        self.voice.chime_startup()
        print("[*] Performing initial diagnostic sweep...\n")
        self.show_status()
        print("\nJARVIS is ready. Type 'help' for command list, or 'exit' to quit.\n")

    def show_status(self):
        telemetry = self.sys_op.get_system_telemetry()
        print("+" + "-"*48 + "+")
        print(f"|  SYSTEM TELEMETRY REPORT                       |")
        print("+" + "-"*48 + "+")
        print(f"| CPU Cores      : {telemetry.get('CPU_Logical_Cores', 'N/A'):<29} |")
        print(f"| RAM Usage      : {telemetry.get('RAM_Percent', 'N/A')} ({telemetry.get('RAM_Used_GB', 0)}GB / {telemetry.get('RAM_Total_GB', 0)}GB){' ': <10} |")
        print(f"| Battery Status : {telemetry.get('Battery_Percent', 'N/A')} [{telemetry.get('Power_Line', 'N/A')}]{' ': <15} |")
        
        drives = telemetry.get('Drives', [])
        if isinstance(drives, list):
            for d in drives:
                drive_str = f"{d.get('Drive')} Free: {d.get('FreeGB')}GB / {d.get('TotalGB')}GB"
                print(f"| Drive Storage  : {drive_str:<29} |")
        print("+" + "-"*48 + "+")

    def execute_command(self, cmd_line: str):
        parts = cmd_line.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ["status", "stats", "telemetry"]:
            self.voice.chime_affirmative()
            self.show_status()

        elif cmd in ["open", "launch", "start"]:
            if not args:
                print("Usage: open <app_name> (e.g. chrome, vscode, notepad, spotify, calc)")
                return
            target = " ".join(args)
            self.voice.chime_affirmative()
            msg = self.sys_op.open_application(target)
            print(f"[JARVIS] {msg}")

        elif cmd in ["vol", "volume"]:
            if not args:
                print("Usage: vol <up|down|mute> [steps]")
                return
            action = args[0]
            steps = int(args[1]) if len(args) > 1 and args[1].isdigit() else 5
            self.voice.chime_affirmative()
            msg = self.sys_op.control_volume(action, steps)
            print(f"[JARVIS] {msg}")

        elif cmd in ["screenshot", "ss", "capture"]:
            self.voice.chime_affirmative()
            print("[JARVIS] Capturing primary display...")
            msg = self.sys_op.take_screenshot()
            print(f"[JARVIS] {msg}")

        elif cmd in ["lock", "lockscreen"]:
            self.voice.chime_affirmative()
            print("[JARVIS] Locking workstation...")
            self.sys_op.lock_workstation()

        elif cmd in ["chime", "ping"]:
            self.voice.chime_startup()
            print("[JARVIS] Audio synthesizer test positive.")

        elif cmd in ["help", "?"]:
            print("\nAvailable JARVIS Commands:")
            print("  status                   - Display CPU, RAM, Battery, and Disk diagnostics")
            print("  open <app>               - Launch app (chrome, code, spotify, notepad, etc.)")
            print("  vol <up|down|mute> [n]   - Adjust or mute master Windows volume")
            print("  screenshot               - Take instant screenshot and save to disk")
            print("  lock                     - Lock Windows screen immediately")
            print("  chime                    - Test futuristic audio synthesizer")
            print("  exit / quit              - Standby mode\n")

        else:
            print(f"[JARVIS] Command '{cmd}' unrecognized. Type 'help' for manual.")

def main():
    jarvis = JarvisCore()
    if len(sys.argv) > 1:
        # CLI direct mode
        jarvis.execute_command(" ".join(sys.argv[1:]))
    else:
        # Interactive mode
        jarvis.boot()
        while True:
            try:
                user_input = input("JARVIS >> ")
                if user_input.strip().lower() in ["exit", "quit", "q"]:
                    jarvis.voice.chime_alert()
                    print("[JARVIS] Entering standby mode. Good day, Sir.")
                    break
                jarvis.execute_command(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\n[JARVIS] Session terminated.")
                break

if __name__ == "__main__":
    main()

