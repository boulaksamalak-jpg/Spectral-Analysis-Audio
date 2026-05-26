# Parametric & Classical Spectral Analysis of Audio Signals

## Overview
This repository contains a complete MATLAB implementation evaluating and comparing classical and parametric spectral estimation methods applied to real-world acoustic data. The project focuses on addressing the resolution and leakage limitations of classical Fourier analysis when handling short, noisy, or non-stationary signals.

## Implemented Methods
- **Classical Approach:** Fast Fourier Transform (FFT) and global spectral analysis.
- **Parametric AR Estimation:** Auto-Regressive modeling using both **Yule-Walker** (`aryule`) and **Burg** (`arburg`) algorithms.
- **Parametric ARMA Estimation:** Combined Auto-Regressive Moving Average modeling using rational filter fitting (`invfreqz`).
- **Time-Frequency Localization:** Local temporal segmentation adapted specifically for analyzing non-stationary characteristics in audio signals.

## Dataset & Signal Source
The algorithms in this repository are validated using a real-world audio signal:
- **File:** `my_audio.wav`
- **Characteristics:** Contains time-varying acoustic features, making it an ideal candidate for evaluating both global stationary estimation and localized short-time analysis (e.g., speech/music processing).

## Key Insights & Results
- **Frequency Resolution:** Parametric methods (AR/ARMA) provide significantly higher frequency resolution and smoother Power Spectral Density (PSD) profiles compared to classical FFT, especially for shorter data windows.
- **Burg vs. Yule-Walker:** The Burg method exhibits greater stability, sharper peak resolution, and fewer frequency shifts because it minimizes both forward and backward prediction errors simultaneously.
- **Non-Stationarity Management:** Standard global FFT fails to capture temporal changes in spectral properties. Implementing local windowed segmentation is essential to accurately track frequency variations over time.

## Repository Structure
- `spectral_analysis.m`: The core, fully commented MATLAB script containing all processing steps (from audio acquisition to advanced modeling).
- `sample-1.wav`: The real audio signal used for testing and validation.

## Key MATLAB Functions Utilized
- **Signal Processing Toolbox:** `audioread`, `spectrogram`, `aryule`, `arburg`, `freqz`, `invfreqz`.

---
*Practical project completed as part of the Advanced Signal Processing curriculum, Electronics Department.*
