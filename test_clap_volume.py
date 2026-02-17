"""
Jarvis Clap Volume Tester
Use this to test what volume your claps register as
"""

import pyaudiowpatch as pyaudio
import numpy as np
import time

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def calculate_rms(audio_data):
    """Calculate Root Mean Square (volume level)"""
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    rms = np.sqrt(np.mean(audio_np**2))
    return rms

print("""
╔══════════════════════════════════════════════════╗
║         JARVIS CLAP VOLUME TESTER                ║
║   Test your clap volume before running Jarvis    ║
╚══════════════════════════════════════════════════╝

Instructions:
1. Watch the real-time volume meter below
2. Try different actions:
   - Type on keyboard
   - Click mouse
   - Tap desk
   - CLAP YOUR HANDS
3. Note the peak volumes for each
4. Press Ctrl+C to exit

Starting in 2 seconds...
""")

time.sleep(2)

# Initialize audio
p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE
)

print("🎤 LISTENING... (Current threshold in Jarvis: 50 RMS)\n")

max_rms = 0
try:
    while True:
        audio_data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        rms = calculate_rms(audio_data)
        
        # Skip if RMS is invalid (NaN or infinite)
        if not np.isfinite(rms):
            continue
        
        # Track maximum
        if rms > max_rms:
            max_rms = rms
        
        # Create visual bar
        bar_length = int(min(rms / 5, 50))  # Scale for display
        bar = "█" * bar_length
        
        # Color coding based on threshold
        if rms < 30:
            status = "🔇 Too quiet"
        elif rms < 50:
            status = "⚠️  Close to threshold"
        elif rms < 100:
            status = "✅ Good clap!"
        else:
            status = "✅✅ PERFECT CLAP!"
        
        print(f"\rVolume: {rms:6.2f} RMS │ {bar:<50} │ {status} │ Peak: {max_rms:.2f}", end='')
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n\n" + "="*80)
    print(f"📊 SESSION SUMMARY:")
    print(f"   Peak Volume Detected: {max_rms:.2f} RMS")
    print(f"   Current Jarvis Threshold: 50.00 RMS")
    
    if max_rms < 50:
        print(f"\n⚠️  Your claps ({max_rms:.2f} RMS) are below the threshold!")
        print("   Solutions:")
        print("   1. Clap louder and sharper")
        print("   2. Increase microphone boost in Windows Sound Settings")
        print("   3. Lower threshold: Edit line 44 in jarvis_clap_automation.py")
        print("      Change: MINIMUM_CLAP_VOLUME = 30")
    else:
        print(f"\n✅ Your claps are loud enough! Jarvis should detect them.")
    
    print("="*80 + "\n")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
