# ⚡ J.A.R.V.I.S. Autonomous Workstation Co-Pilot

<div align="center">


**An intelligent, futuristic autonomous desktop assistant with a full Iron Man-inspired HUD, voice synthesis, hardware telemetry, deep OS control, and automated telephony notifications.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)](#)
[![Interface](https://img.shields.io/badge/Interface-Sci--Fi%20Cyber%20HUD-FF4500?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](#)

</div>

---

## 🌟 Key Features

### 🖥️ 1. Sci-Fi Cyber HUD (Web Audio & Speech API)
- **Iron Man Holographic Visuals**: Real-time rotating Arc Reactor canvas, audio wave visualizer, system diagnostics panels, and live telemetry widgets.
- **Continuous Voice Interaction**: Integrated browser Web Speech recognition with auto-reconnect and acoustic audio confirmation chimes.
- **Standalone Window App**: Runs seamlessly in dedicated app window mode (borderless Chrome/Edge shell) without browser bars or URL clutter.

### ⚙️ 2. Deep OS & Hardware Control (`SystemOperator`)
- **Live System Telemetry**: Real-time monitoring of CPU usage & cores, RAM capacity, battery charge & power supply, and drive storage.
- **Smart App Indexer**: Automatically scans and indexes all installed Windows software and Start Menu shortcuts for instant voice-activated launch.
- **Hardware Toggles**: Control system volume, mute, display brightness, Bluetooth radios, and take instant screenshots.

### 🧠 3. Cognitive Brain & Context Memory
- **Intent Analysis**: Classifies multi-modal user prompts (system operations, math, scheduling, app launching, or casual conversation).
- **Persistent Context**: Maintains conversational history across sessions.
- **Scientific Math Engine**: Instant calculation of mathematical expressions, conversions, and equations.

### ⏰ 4. Scheduler & Safety Protocol
- **Autonomous Task Scheduling**: Set timed reminders, study sessions, and recurring tasks.
- **Safety Deadlines**: Check-in protocols with configurable timeout and emergency escalation.
- **Multi-Channel Alerts**: Automated voice calls via Twilio Voice API, WhatsApp alerts, and ntfy.sh instant mobile notifications.

---

## 📁 Project Architecture

```
jarvis-assistant/
│
├── data/                         # Persistent configs and data (indexes, schedules, safety state)
│   ├── installed_apps.json       # Indexed Windows applications
│   ├── phone_config.json         # Telephony & notification configuration
│   ├── safety_status.json        # Dead-man check-in and safety records
│   └── schedules.json            # Timed automation schedules
│
├── modules/                      # Modular backend engines
│   ├── app_indexer.py            # Windows app discovery and fuzzy search
│   ├── cognitive_brain.py        # Central decision and NLP engine
│   ├── context_memory.py         # Multi-turn conversation memory
│   ├── math_engine.py            # Computation and arithmetic solver
│   ├── phone_caller.py           # Twilio GSM telephony caller
│   ├── safety_protocol.py        # Safety monitoring & check-in triggers
│   ├── scheduler.py              # Background task scheduling daemon
│   ├── system_operator.py        # PowerShell & Windows API bridge
│   ├── voice_engine.py           # Pure-Python acoustic sound synthesis
│   └── whatsapp_notifier.py      # Automated WhatsApp messaging alerts
│
├── scripts/                      # OS automation helper scripts
│   └── toggle_bluetooth.ps1      # PowerShell Bluetooth state toggler
│
├── screenshots/                  # Saved screen captures
│
├── hud.html                      # Futuristic Cyberpunk / Iron Man HUD Interface
├── server.py                     # Local HTTP & API Bridge server (port 8765)
├── jarvis.py                     # CLI console interface fallback
├── JARVIS.bat                    # One-click standalone desktop launcher
├── JARVIS.vbs                    # Background daemon launcher (silent window)
├── start_jarvis.bat              # Debug launcher with visible console logs
├── Install_Desktop_Shortcut.bat  # Creates Desktop shortcut icon
├── jarvis.ico / jarvis.png       # Custom UI branding assets
├── requirements.txt              # Python package dependencies
└── README.md                     # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
1. **Windows 10 / 11**
2. **Python 3.10+** installed and added to `PATH`
3. **Google Chrome** or **Microsoft Edge**

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/<your-username>/jarvis-assistant.git
   cd jarvis-assistant
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Create Desktop Shortcut**:
   Double click `Install_Desktop_Shortcut.bat` to place a shiny **J.A.R.V.I.S.** icon directly on your Windows Desktop.

---

## 🎮 How to Run

### Method 1: Desktop Application (Recommended)
Double-click `JARVIS.bat` or the **J.A.R.V.I.S.** Desktop shortcut.
* Automatically spins up the background API server.
* Launches the standalone dedicated HUD application window.

### Method 2: Manual Terminal / Developer Mode
Run the local bridge in PowerShell or Command Prompt:
```powershell
python server.py
```
Then open your browser and navigate to:
```
http://localhost:8765
```

---

## 🎙️ Voice & Text Command Examples

| Category | Example Voice / Text Command |
|---|---|
| **System Diagnostics** | *"Jarvis, status"* or *"Telemetry report"* |
| **App Launching** | *"Open Spotify"*, *"Buka Chrome"*, *"Launch Visual Studio Code"* |
| **System Volume** | *"Set volume to 50%"*, *"Mute audio"*, *"Volume up"* |
| **Display & Screen** | *"Capture screen"*, *"Take a screenshot"*, *"Set brightness to 80%"* |
| **Calculations** | *"Berapa 250 dikali 48"*, *"Calculate sqrt(144) + 25"* |
| **Automation** | *"Schedule study session for 45 minutes"* |
| **Safety Check** | *"I am safe"*, *"Check safety status"* |

---

## ⚙️ Configuration

Configure phone calling, Twilio credentials, and notification channels in `data/phone_config.json`:

```json
{
  "target_phone_number": "+6281234567890",
  "twilio_account_sid": "YOUR_TWILIO_SID",
  "twilio_auth_token": "YOUR_TWILIO_AUTH_TOKEN",
  "twilio_phone_number": "YOUR_TWILIO_PHONE_NUMBER",
  "ntfy_topic": "jarvis-alerts",
  "caller_name": "J.A.R.V.I.S.",
  "voice_language": "id-ID"
}
```

---

## 🛡️ License

This project is licensed under the MIT License. Feel free to modify and expand for your personal co-pilot needs!
