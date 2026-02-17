# Quick Start - Jarvis Voice Automation

## ✅ Installation Complete!

Dependencies installed:
- ✅ SpeechRecognition (Voice commands)
- ✅ pygetwindow (Window management)
- ✅ PyAudioWPatch (Microphone access)
- ✅ pyttsx3 (Voice feedback)

## 🎯 How to Use

### 1. Configure Your Apps
Edit `jarvis_clap_automation.py` (lines 16-29) to set your paths:

```python
APP_CONFIG = {
    "work_suite": [
        r"C:\Path\To\MainApp.exe",       # Will go to LEFT HALF
        r"C:\Path\To\SecondaryApp.exe",  # Will go to TOP RIGHT
        r"C:\Path\To\TertiaryApp.exe",   # Will go to BOTTOM RIGHT
    ],
    ...
}
```

### 2. Run Jarvis
```powershell
python jarvis_clap_automation.py
```

### 3. Voice Commands
Wait for: *"I am listening."*

| Command | Action |
|---------|--------|
| **"Jarvis Go"** | Launches Work apps & arranges windows |
| **"Jarvis Play"** | Launches Entertainment apps |
| **"Jarvis Stop"** | Shuts down Jarvis |

## ⌨️ Managing Windows

- **Admin Apps**: If you use Discord/Steam/Task Manager, run the script as **Administrator** so it can move those windows.
- **Timing**: The script waits 3 seconds after launching apps before moving them. If your PC is slow, apps might miss the move command.

## 🎤 Microphone Tips

- First run will calibrate for 2 seconds (stay quiet!).
- If it doesn't hear you, check your default recording device in Windows Sound settings.
