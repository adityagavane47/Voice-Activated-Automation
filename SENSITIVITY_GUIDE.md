# 🎤 Voice Recognition Troubleshooting

## Common Issues

### 1. "Internet connection required"
The script uses Google Speech Recognition which requires an internet connection.
- **Fix**: Check your wifi.

### 2. Jarvis doesn't hear me
- **Check Mic**: Ensure microphone is set as Default Device in Windows.
- **Calibration**: When starting, **stay quiet** for 2 seconds so it learns the background noise level.
- **Speak Clearly**: "Jarvis Go" (wait for "Processing..." in console).

### 3. Windows not moving to correct spots
- **Admin Rights**: Apps like Task Manager, RegEdit, or Games running as Admin cannot be moved by a normal script.
  - **Fix**: Right-click PowerShell/CMD -> **Run as Administrator**.
- **Slow Launch**: If apps take >3 seconds to open, they miss the layout command.
  - **Fix**: Edit line 66 in `jarvis_clap_automation.py` to increase `time.sleep(3)` to `time.sleep(5)`.

## Changing the Trigger Word

Edit `jarvis_clap_automation.py`:

```python
TRIGGER_PHRASE = "computer start"  # Change to whatever you want
```
