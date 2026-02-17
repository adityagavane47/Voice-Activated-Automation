# Jarvis - AI-Powered Offline Automation Assistant

A professional-grade automation tool that uses local AI (Ollama) and offline speech recognition (Vosk) to understand natural language commands and manage your workspace.

## Features

- **Voice Activation**: "Jarvis" acts as the wake word.
- **AI Intelligence**: Uses Ollama (Phi-3) to understand intent from natural language (e.g., "I want to code" vs "Open VS Code").
- **Offline Privacy**: All speech processing and AI analysis happens locally on your machine.
- **Dynamic Profiles**: easy configuration via `profiles.json`.

## Prerequisites

1. **Python 3.8+**
2. **Ollama**: Download and install from [ollama.com](https://ollama.com).
3. **Vosk Model**: Download `vosk-model-small-en-us-0.15` from [alphacephei.com](https://alphacephei.com/vosk/models).

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
pip install ollama
```

*Note: Windows users may need `pip install pyaudiowpatch` for microphone access.*

### Step 2: Setup Ollama

Pull the Phi-3 model (lightweight and fast):
```bash
ollama run phi3
```

### Step 3: Configure Model Path

Ensure the Vosk model is extracted to a folder named `model` in the project directory, or update `VOSK_MODEL_PATH` in `jarvis_clap_automation.py`.

## Configuration

Edit `profiles.json` to create custom automation modes.

```json
{
  "coding": {
    "apps": [
      "C:\\Program Files\\Microsoft VS Code\\Code.exe"
    ],
    "urls": ["https://github.com"],
    "tts_response": "Happy coding."
  }
}
```

## Usage

1. Run the script:
   ```bash
   python jarvis_clap_automation.py
   ```
2. Wait for "System online".
3. Speak naturally:
   - "Jarvis, it's time to study."
   - "Jarvis, I am bored."
   - "Jarvis, open my coding tools."

## Troubleshooting

### "Microphone error"
Ensure your microphone is set as the Default Recording Device in Windows Sound settings.

### "Ollama not found"
Ensure the Ollama app is running in the background.

## License

Free to use and modify.

## Credits

Built by an Expert Python Developer.
