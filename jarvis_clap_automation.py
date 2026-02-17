"""
Jarvis - Voice-Activated Application Launcher & Window Manager
Professional-grade automation script that listens for voice commands ("Jarvis Go")
and launches application suites with specific window layouts.

Author: Expert Python Developer
Version: 2.0 (Voice Edition)
"""

import sys
try:
    import pyaudiowpatch as pyaudio
    # Monkey-patch: make 'pyaudio' module available to SpeechRecognition
    sys.modules["pyaudio"] = pyaudio
except ImportError:
    print("[WARNING] PyAudioWPatch not found. Microphone access may fail.")

import time
import subprocess
import threading
import pyttsx3
import speech_recognition as sr
import pygetwindow as gw
from queue import Queue

# ==================== CONFIGURATION ====================
# Application paths (Windows)
APP_CONFIG = {
    "work_suite": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        r"C:\Users\ADITYA GAVANE\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Antigravity", # Example 3rd app
    ],
    "entertainment_suite": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        # r"C:\Program Files\Spotify\Spotify.exe",
    ],
    "entertainment_url": "https://www.youtube.com"
}

TRIGGER_PHRASE = "jarvis go"
ENTERTAINMENT_PHRASE = "jarvis play"
EXIT_PHRASES = ["jarvis stop", "exit", "shutdown"]

# ==================== UTIL: WINDOW MANAGER ====================
class WindowLayoutManager:
    """Manages window positioning and resizing"""
    
    @staticmethod
    def get_screen_size():
        """Get primary screen resolution"""
        try:
             import ctypes
             user32 = ctypes.windll.user32
             return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        except:
            return 1920, 1080

    @staticmethod
    def apply_work_layout():
        """
        Applies split screen layout:
        App 1: Left Half
        App 2: Top Right Quarter
        App 3: Bottom Right Quarter
        """
        width, height = WindowLayoutManager.get_screen_size()
        half_width = width // 2
        half_height = height // 2
        
        print("\n[LAYOUT] Applying layout...")
        
        # Wait for windows to appear
        time.sleep(3)
        
        # Get all visible windows
        windows = [w for w in gw.getAllWindows() if w.visible and w.title]
        
        # Try to find our target apps
        targets = []
        for app_path in APP_CONFIG["work_suite"]:
            name = app_path.split("\\")[-1].lower().replace(".exe", "")
            found = None
            for w in windows:
                title = w.title.lower()
                if name in title or \
                   ("chrome" in name and "google chrome" in title) or \
                   ("code" in name and "visual studio code" in title):
                    found = w
                    break
            if found:
                targets.append(found)
            else:
                print(f"  [WARNING] Window not found for {name}")

        # Layout definitions (x, y, w, h)
        layouts = [
            (0, 0, half_width, height),                         # Left Half
            (half_width, 0, half_width, half_height),           # Top Right
            (half_width, half_height, half_width, half_height)  # Bottom Right
        ]
        
        for i, window in enumerate(targets):
            if i >= len(layouts): break
            x, y, w, h = layouts[i]
            try:
                window.restore()
                window.moveTo(x, y)
                window.resizeTo(w, h)
                print(f"  Moved '{window.title[:20]}...' to ({x}, {y}, {w}, {h})")
            except Exception as e:
                print(f"  Failed to move {window.title}: {e}")

# ==================== JARVIS VOICE SYSTEM ====================
class JarvisVoice:
    """Text-to-Speech system for Jarvis using background thread"""
    
    def __init__(self):
        self.queue = Queue()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        time.sleep(0.5)
    
    def _run(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        voices = engine.getProperty('voices')
        for voice in voices:
            if "david" in voice.name.lower() or "male" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        while True:
            text = self.queue.get()
            if text is None: break
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"[WARNING] Speech error: {e}")
    
    def speak(self, text):
        print(f"[JARVIS]: {text}")
        self.queue.put(text)

# ==================== VOICE LISTENER ====================
class VoiceListener:
    """Handles speech recognition"""
    
    def __init__(self, jarvis):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        self.jarvis = jarvis
    
    def adapt_to_noise(self):
        """Calibrate for ambient noise"""
        print("\n[CALIBRATION] Measuring ambient noise... (please wait)")
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source, duration=2)
        print(f"[CALIBRATION] Complete. Energy threshold: {self.r.energy_threshold:.0f}")
        self.jarvis.speak("I am listening.")
    
    def listen(self):
        """Listen for a command"""
        with self.mic as source:
            print("Listening...", end='\r')
            try:
                # Listen with a timeout to keep the loop responsive
                audio = self.r.listen(source, timeout=1, phrase_time_limit=3)
                print("Processing... ", end='')
                text = self.r.recognize_google(audio).lower()
                print(f"\n[HEARD]: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                # Speech not recognized
                return None
            except sr.RequestError:
                print("\n[ERROR] Internet connection required for recognition.")
                return None
            except Exception as e:
                # print(f"\n[ERROR] {e}") # Suppress minor errors
                return None

# ==================== APPLICATION LAUNCHER ====================
class ApplicationLauncher:
    """Launches and manages apps"""
    
    @staticmethod
    def work_protocol(jarvis):
        print("\n" + "="*50)
        print("[WORK PROTOCOL INITIATED]")
        jarvis.speak("Work protocol initiated. Preparing your workspace.")
        
        for app_path in APP_CONFIG["work_suite"]:
            try:
                # Use os.startfile for Windows shortcuts and non-executables
                import os
                os.startfile(app_path)
                print(f"  Launched: {app_path}")
                time.sleep(1) 
            except FileNotFoundError:
                print(f"  [ERROR] Not found: {app_path}")
            except Exception as e:
                print(f"  [ERROR] Failed: {e}")
        
        jarvis.speak("Arranging windows.")
        WindowLayoutManager.apply_work_layout()
        print("="*50 + "\n")

    @staticmethod
    def entertainment_protocol(jarvis):
        print("\n" + "="*50)
        print("[ENTERTAINMENT PROTOCOL ENGAGED]")
        jarvis.speak("Entertainment protocol engaged. Enjoy.")
        
        chrome_path = APP_CONFIG["entertainment_suite"][0]
        url = APP_CONFIG["entertainment_url"]
        
        try:
            subprocess.Popen([chrome_path, url])
            print(f"  Launched: {chrome_path} -> {url}")
        except Exception as e:
            print(f"  [ERROR] Failed to launch browser: {e}")
            
        print("="*50 + "\n")

# ==================== MAIN SYSTEM ====================
def main():
    print("""
    ╔══════════════════════════════════════════════════╗
    ║         JARVIS VOICE AUTOMATION v2.0             ║
    ║   Say 'Jarvis Go' to start Work Protocol         ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    jarvis = JarvisVoice()
    
    try:
        listener = VoiceListener(jarvis)
        listener.adapt_to_noise()
    except OSError:
        print("[FATAL] No microphone found. Exiting.")
        return

    # Laucher Instance
    launcher = ApplicationLauncher()

    try:
        while True:
            command = listener.listen()
            
            if command:
                if TRIGGER_PHRASE in command:
                    launcher.work_protocol(jarvis)
                
                elif ENTERTAINMENT_PHRASE in command:
                    launcher.entertainment_protocol(jarvis)
                
                elif any(phrase in command for phrase in EXIT_PHRASES):
                    jarvis.speak("Shutting down. Goodbye.")
                    break
            
            # Use sleep to prevent CPU spiking in loop
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] User interrupted.")
    finally:
        print("[SHUTDOWN] Complete.")

if __name__ == "__main__":
    main()
