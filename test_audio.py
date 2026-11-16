import numpy as np
import sounddevice as sd
import time

def play_jarvis_chime():
    sr = 44100
    # Two-tone futuristic ascending chime
    duration = 0.12
    t = np.linspace(0, duration, int(sr * duration), False)
    
    # Frequencies for futuristic affirmative sound (e.g., 880 Hz -> 1760 Hz)
    tone1 = np.sin(2 * np.pi * 880 * t) * np.exp(-t * 15)
    tone2 = np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 15)
    
    combined = np.concatenate([tone1, tone2]) * 0.3
    try:
        sd.play(combined, sr)
        sd.wait()
        print("Chime played successfully.")
    except Exception as e:
        print(f"Audio playback note: {e}")

if __name__ == "__main__":
    play_jarvis_chime()

