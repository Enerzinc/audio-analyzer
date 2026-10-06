# Audio Analyzer

A desktop DSP tool that records or loads two audio signals, combines them into a composite signal, and displays them in the **time domain (oscilloscope)** or **frequency domain (spectrum analyzer)**.

## Purpose

This project was built for a Digital Signal Processing course to demonstrate core signal analysis concepts:

- **Recording / loading** two separate audio signals (44.1 kHz, 5 seconds each)
- **Signal mixing** — averaging two signals into one composite signal
- **Time-domain visualization** — plotting amplitude vs. time (oscilloscope view)
- **Frequency-domain visualization** — computing the FFT of each signal and plotting magnitude vs. frequency (spectrum analyzer view)
- **Comparing** individual signals against their composite result

## Features

- Record up to two 5-second clips directly from your microphone with a live countdown
- Upload exactly two `.wav` files instead of recording
- Switch between **Oscilloscope** and **Spectrum Analyzer** views
- Overlay Signal 1, Signal 2, and the composite signal on one plot
- Save any plot as `.jpg` or `.png`
- Clear the graph or restart the recordings
- Light / dark theme toggle

## Requirements

- Python 3.10+
- A working microphone (for recording mode)

Install the dependencies:

```bash
pip install customtkinter ttkbootstrap numpy matplotlib pillow sounddevice scipy
```

> `tkinter` ships with Python. On Linux you may need `sudo apt install python3-tk`.
> `sounddevice` needs PortAudio: `sudo apt install libportaudio2` (Linux) or `brew install portaudio` (macOS).

## How to Run

From the project directory:

```bash
python SignalAnalyzerGUI.py
```

> Run it from the project root — the app loads its icons from the `images/` folder using relative paths.

## How to Use

1. **Provide two signals** using either method:
   - **Record:** Click **Mic 1**, speak for 5 seconds, then click **Mic 2** and repeat. The countdown shows how much time is left.
   - **Upload:** Click the **Upload** button and select **exactly two** `.wav` files (e.g., the ones in `sample_audio/`).
2. **Pick a view** from the dropdown:
   - **Oscilloscope** — time-domain plot of Signal 1, Signal 2, and their composite.
   - **Spectrum Analyzer** — FFT spectrum of Signal 1, Signal 2, and the composite side by side.
3. Click the **Plot** button to generate the graph.
4. **Save** the plot to an image file, or **Clear** to reset the canvas.
5. **Restart** clears both recordings so you can start over.
6. Use the **Toggle Theme** switch to flip between light and dark mode.

## Project Structure

```
├── SignalAnalyzerGUI.py   # Main GUI application (CustomTkinter + Matplotlib)
├── SignalProcessor.py     # Signal helpers: FFT, WAV reading, audio recording
├── images/                # Button icons (light/dark variants)
├── sample_audio/          # Example WAV files for testing uploads
└── SIGNALS_IMAGES/        # Sample screenshots of generated plots
```

## How It Works

1. Both signals are padded/trimmed to exactly 5 seconds (5 × 44100 samples) so they align.
2. The composite signal is the element-wise average: `(signal1 + signal2) / 2`.
3. For the spectrum view, `compute_fft()` applies an N-point FFT and keeps the positive frequencies (first `N/2` bins), scaling the magnitude by `2/N`.
4. Plots are rendered with Matplotlib and embedded in the Tkinter window via `FigureCanvasTkAgg`.
