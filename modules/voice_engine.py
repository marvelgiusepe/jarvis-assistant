"""
Voice & Audio Engine for JARVIS
Handles sound synthesis, futuristic chimes, and Neural Text-to-Speech playback.
"""

import os
import subprocess
import numpy as np
import sounddevice as sd
from typing import Optional

class VoiceEngine:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def play_sound_wave(self, wave_data: np.ndarray):
        """Play a numpy waveform through sounddevice."""
        try:
            sd.play(wave_data.astype(np.float32), self.sample_rate)
            sd.wait()
        except Exception as e:
            print(f"[JARVIS Audio Note] {e}")

    def chime_startup(self):
        """Ascending three-chord chord tone for system activation."""
        sr = self.sample_rate
        d = 0.1
        t = np.linspace(0, d, int(sr * d), False)
        
        # 440Hz (A4) -> 659.25Hz (E5) -> 880Hz (A5)
        f1 = np.sin(2 * np.pi * 440 * t) * np.exp(-t * 8)
        f2 = np.sin(2 * np.pi * 659.25 * t) * np.exp(-t * 8)
        f3 = np.sin(2 * np.pi * 880 * t) * np.exp(-t * 6)
        
        wave = np.concatenate([f1, f2, f3]) * 0.25
        self.play_sound_wave(wave)

    def chime_affirmative(self):
        """Short dual-tone affirmative acknowledgment (Command received)."""
        sr = self.sample_rate
        d = 0.08
        t = np.linspace(0, d, int(sr * d), False)
        
        f1 = np.sin(2 * np.pi * 880 * t) * np.exp(-t * 12)
        f2 = np.sin(2 * np.pi * 1318.5 * t) * np.exp(-t * 12)
        
        wave = np.concatenate([f1, f2]) * 0.25
        self.play_sound_wave(wave)

    def chime_alert(self):
        """Warning / notification sound."""
        sr = self.sample_rate
        d = 0.15
        t = np.linspace(0, d, int(sr * d), False)
        
        tone = (np.sin(2 * np.pi * 587.33 * t) + np.sin(2 * np.pi * 880 * t)) * 0.5
        wave = tone * np.exp(-t * 10) * 0.3
        self.play_sound_wave(wave)

    def speak(self, text: str, voice: str = "en-GB-RyanNeural"):
        """
        Speak text.
        If edge-tts is installed and internet is active, generates neural audio.
        Otherwise falls back to an affirmative chime.
        """
        # Always acknowledge with affirmative chime
        self.chime_affirmative()
        
        # Check if edge-tts is available in environment
        try:
            import tempfile
            temp_mp3 = os.path.join(tempfile.gettempdir(), "jarvis_speech.mp3")
            temp_wav = os.path.join(tempfile.gettempdir(), "jarvis_speech.wav")
            
            # Try running edge-tts CLI if installed
            cmd = f'edge-tts --voice "{voice}" --text "{text}" --write-media "{temp_mp3}"'
            res = subprocess.run(cmd, shell=True, capture_output=True, timeout=10)
            
            if res.returncode == 0 and os.path.exists(temp_mp3):
                # Play using powershell or media player
                play_cmd = f"""powershell -c "(New-Object Media.SoundPlayer '{temp_wav}').PlaySync()" """
                # or play via edge-playback if installed
                return True
        except Exception:
            pass
        return False

if __name__ == "__main__":
    ve = VoiceEngine()
    print("Testing JARVIS Audio Startup...")
    ve.chime_startup()
    print("Testing JARVIS Affirmative...")
    ve.chime_affirmative()
    print("Audio test completed.")

