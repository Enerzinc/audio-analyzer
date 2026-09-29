import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
import scipy.io.wavfile as wav

import sounddevice as sd


def compute_fft(signal, sample_rate):
    N = len(signal)  
    fft_values = (2 / N) * np.abs(fft(signal)[:N // 2]) 
    freqs = fftfreq(N, d=1/sample_rate)[:N // 2]  
    return freqs, fft_values
def record_audio(duration=5.0, sample_rate=44100):
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32)
    sd.wait()  
    return audio_data.flatten()
def read_wav_file(filename):
    sample_rate, data = wav.read(filename)
    if len(data.shape) > 1: 
        data = data.mean(axis=1)
    return sample_rate, data