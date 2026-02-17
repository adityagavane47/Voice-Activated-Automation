# Alternative Installation Instructions for PyAudio Issues

## Problem
PyAudio fails to install on Windows because it requires PortAudio C headers which aren't available during compilation.

## Solution Options

### Option 1: Use pipwin (Recommended for Windows)
```powershell
# Install pipwin first
pip install pipwin

# Install PyAudio using pipwin (it downloads pre-compiled binaries)
pipwin install pyaudio

# Then install the remaining packages
pip install numpy pyttsx3
```

### Option 2: Download Pre-compiled Wheel File
1. Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Download the wheel for Python 3.14, 64-bit:
   - Look for: `PyAudio‑0.2.14‑cp314‑cp314‑win_amd64.whl`
3. Install it:
   ```powershell
   pip install path\to\PyAudio‑0.2.14‑cp314‑cp314‑win_amd64.whl
   pip install numpy pyttsx3
   ```

### Option 3: Use PyAudio Fork (pyaudio-wheels)
```powershell
# This is a maintained fork with pre-built wheels
pip install PyAudioWPatch
pip install numpy pyttsx3
```

Then modify the import in jarvis_clap_automation.py:
```python
# Change line 8 from:
import pyaudio
# To:
import pyaudiowpatch as pyaudio
```

### Option 4: Skip PyAudio (Use sounddevice instead)
If none of the above work, I can rewrite the script to use `sounddevice` library instead, which has better Windows support.

## Quick Fix for Most Users
Try Option 1 (pipwin) first - it's the easiest!
