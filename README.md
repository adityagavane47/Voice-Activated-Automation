# Jarvis - Voice-Activated Application Launcher & Window Manager

A professional-grade automation script that listens for voice commands and launches specific application suites with automatic window layout management.

## Features

✨ **Voice Activation**: "Jarvis Go" launches your workspace instantly.  
🖥️ **Window Management**: Automatically snaps apps to a split-screen layout (Left, Top-Right, Bottom-Right).  
🗣️ **Voice Feedback**: Jarvis provides verbal confirmations.  
🎯 **Dual Modes**: 
  - **Work**: Chrome (Left), VS Code (Top-Right)
  - **Entertainment**: Chrome (YouTube)

## How It Works

- **"Jarvis Go"** → Launches Work Protocol & Arranges Windows
- **"Jarvis Play"** → Launches Entertainment Protocol
- **"Jarvis Stop"** → Shuts down system

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

*Note: Requires `PyAudioWPatch` on Windows for microphone access.*

### Step 2: Configure Application Paths

Open `jarvis_clap_automation.py` and edit the `APP_CONFIG` dictionary:

```python
APP_CONFIG = {
    "work_suite": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe", # App 1 (Left Half)
        r"C:\Program Files\Microsoft VS Code\Code.exe",          # App 2 (Top Right)
        # Add 3rd app for Bottom Right
    ],
    ...
}
```

## Usage

1. Run the script:
   ```bash
   python jarvis_clap_automation.py
   ```
2. Wait for calibration: *"Calibrating background noise..."*
3. When Jarvis says **"I am listening"**, speak your command:
   - **"Jarvis Go"**

## Troubleshooting

### "Microphone error"
Ensure your microphone is set as the Default Information recording device in Windows Sound settings.

### Windows not moving?
Some apps (like Discord or Steam) run as Admin. You may need to run this script as Administrator to move them.


## License

Free to use and modify. Build something awesome! 🚀

## Credits

Built by an Expert Python Developer & Sound Engineer for seamless productivity automation.
