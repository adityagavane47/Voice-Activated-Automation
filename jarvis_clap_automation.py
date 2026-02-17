"""
Jarvis - AI-Powered Offline Automation Assistant
Features: Vosk Offline Speech + Ollama Local Intelligence + Dynamic Profiles

Author: Expert Python Developer
Version: 4.0 (The AI Upgrade)
"""

import sys
import os
import json
import time
import threading
import subprocess
import pyttsx3
import pygetwindow as gw
from queue import Queue

# --- DEPENDENCIES CHECK ---
try:
    from vosk import Model, KaldiRecognizer
    import pyaudiowpatch as pyaudio # Try extended version first
except ImportError:
    try:
        import pyaudio # Fallback to standard
    except ImportError:
        print("[FATAL] Missing 'pyaudio'. Install via pip.")
        sys.exit(1)
    try:
        from vosk import Model, KaldiRecognizer
    except ImportError:
        print("[FATAL] Missing 'vosk'. Run: pip install vosk")
        sys.exit(1)

try:
    import ollama  # pip install ollama
except ImportError:
    print("[FATAL] Missing 'ollama'. Run: pip install ollama")
    sys.exit(1)


# ==================== CONFIGURATION ====================
# Path to your Vosk model folder. 
# If you renamed the folder to 'model', leave as is. 
# If you kept the long name, change this string to: r"model\vosk-model-small-en-us-0.15"
VOSK_MODEL_PATH = r"model\vosk-model-small-en-us-0.15" 

PROFILES_FILE = "profiles.json"
WAKE_WORD = "jarvis"       # The name it listens for
OLLAMA_MODEL = "phi3"      # Ensure you ran 'ollama run phi3' (or use 'llama3')


# ==================== UTIL: DYNAMIC CONFIG LOADER ====================
class ConfigManager:
    @staticmethod
    def load_profiles():
        """Loads profiles from JSON file"""
        if not os.path.exists(PROFILES_FILE):
            print(f"[ERROR] {PROFILES_FILE} not found! Please create it.")
            return {}
        try:
            with open(PROFILES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] JSON Error: {e}")
            return {}


# ==================== AI BRAIN (OLLAMA) ====================
class AIBrain:
    """Uses Local LLM to decide what the user wants"""
    
    def __init__(self):
        self.profiles = ConfigManager.load_profiles()
        self.available_modes = list(self.profiles.keys())
    
    def analyze_intent(self, user_text):
        """
        Sends user text to Ollama to determine the intent.
        Returns: (intent_name)
        """
        if not self.available_modes:
            return "none"

        print(f" [AI] Thinking about: '{user_text}'...")
        
        # System prompt to act as a strict classifier
        system_prompt = (
            f"You are an intent classifier for a computer automation system. "
            f"The available modes are: {self.available_modes}. "
            f"Based on the user's request, output ONLY the mode name. "
            f"If the request matches nothing, output 'none'. "
            f"Do not write sentences. Just the mode name."
        )

        try:
            response = ollama.chat(model=OLLAMA_MODEL, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_text},
            ])
            
            intent = response['message']['content'].strip().lower()
            
            # Clean up potential extra punctuation (like "coding.")
            import re
            intent = re.sub(r'[^\w]', '', intent)
            
            # Validation
            for mode in self.available_modes:
                if mode == intent:
                    return mode
            
            return "none"
            
        except Exception as e:
            print(f"[AI ERROR] Could not connect to Ollama: {e}")
            return "none"

    def get_profile(self, mode_name):
        return self.profiles.get(mode_name)


# ==================== JARVIS VOICE SYSTEM ====================
class JarvisVoice:
    def __init__(self):
        self.queue = Queue()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _run(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', 160) # Slightly faster speech
        
        # Try to select a good voice
        try:
            voices = engine.getProperty('voices')
            # Prefer a male voice if available (usually index 0 or look for names)
            engine.setProperty('voice', voices[0].id)
        except: pass
        
        while True:
            text = self.queue.get()
            if text is None: break
            try:
                engine.say(text)
                engine.runAndWait()
            except: pass

    def speak(self, text):
        print(f"[JARVIS]: {text}")
        self.queue.put(text)


# ==================== VOICE LISTENER (VOSK) ====================
class VoiceListener:
    def __init__(self, jarvis):
        self.jarvis = jarvis
        
        if not os.path.exists(VOSK_MODEL_PATH):
            print(f"\n[FATAL] Model folder '{VOSK_MODEL_PATH}' is missing!")
            print("1. Download 'vosk-model-small-en-us-0.15' from https://alphacephei.com/vosk/models")
            print("2. Unzip and rename the folder to 'model'")
            sys.exit(1)
            
        print("[INIT] Loading Vosk Model... (this takes a few seconds)")
        
        # Suppress Vosk/ALSA logs
        try:
            self.model = Model(VOSK_MODEL_PATH)
            self.rec = KaldiRecognizer(self.model, 16000)
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(
                format=pyaudio.paInt16, 
                channels=1, 
                rate=16000, 
                input=True, 
                frames_per_buffer=8000
            )
            self.stream.start_stream()
        except Exception as e:
            print(f"[ERROR] Audio initialization failed: {e}")
            sys.exit(1)

    def listen(self):
        """Returns text if a phrase is heard, else None"""
        try:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                text = result.get('text', '')
                if text:
                    return text
        except OSError:
            pass # Ignore input overflow
        return None


# ==================== AUTOMATION ENGINE ====================
class AutomationEngine:
    @staticmethod
    def execute_profile(profile, jarvis):
        if not profile: return
        
        # 1. Voice Feedback
        response = profile.get("tts_response", "Executing protocol.")
        jarvis.speak(response)
        
        # 2. Launch Apps
        apps = profile.get("apps", [])
        for app in apps:
            try:
                os.startfile(app)
                print(f"  > Launched: {app}")
            except Exception as e:
                print(f"  > Error launching {app}: {e}")
        
        # 3. Open URLs
        urls = profile.get("urls", [])
        for url in urls:
            try:
                # 'start' command handles default browser in Windows
                subprocess.Popen(f'start {url}', shell=True)
                print(f"  > Opened: {url}")
            except Exception as e:
                print(f"  > Error opening URL: {e}")


# ==================== MAIN LOOP ====================
def main():
    print("""
    ╔════════════════════════════════════════╗
    ║     JARVIS v4.0 (AI + OFFLINE)         ║
    ║  Say 'Jarvis' followed by a command    ║
    ╚════════════════════════════════════════╝
    """)

    jarvis = JarvisVoice()
    listener = VoiceListener(jarvis)
    brain = AIBrain()
    automator = AutomationEngine()

    jarvis.speak("System online. Waiting for commands.")

    try:
        while True:
            text = listener.listen()
            
            if text:
                print(f"\n[HEARD]: {text}")
                
                # Check for Wake Word
                if WAKE_WORD in text:
                    # Strip wake word to get the actual command
                    # e.g., "jarvis start coding" -> "start coding"
                    command = text.replace(WAKE_WORD, "").strip()
                    
                    if not command:
                        jarvis.speak("Yes?")
                        continue

                    # AI ANALYSIS
                    intent = brain.analyze_intent(command)
                    
                    if intent != "none":
                        print(f"[AI DECISION] Intent identified: {intent.upper()}")
                        profile = brain.get_profile(intent)
                        automator.execute_profile(profile, jarvis)
                    else:
                        print("[AI DECISION] No matching profile found.")
                        jarvis.speak("I'm not sure which mode you want.")
            
            # Tiny sleep to save CPU when no audio is processed
            # (Stream read blocks, so this is just for safety)
            time.sleep(0.01)
                        
    except KeyboardInterrupt:
        print("\n[EXIT] Goodbye.")

if __name__ == "__main__":
    main()