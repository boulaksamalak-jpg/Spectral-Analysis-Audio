# Parametric & Classical Spectral Analysis of Audio Signals

A dual-platform Digital Signal Processing (DSP) framework evaluating and comparing classical and parametric spectral estimation methods. This project analyzes acoustic data using **MATLAB** for high-resolution exploration and tracks the validation pipeline via a parallel script optimized for **Python (Pydroid 3 Compatible)**.

---

## 📌 Project Overview
Classical Fourier analysis (FFT) is computationally efficient but suffers from limitations like statistical variance and spectral leakage dictated by the window length ($\Delta f \approx 1/N$). When handling short or noisy acoustic signals, classical methods can mask adjacent frequencies. 

This project implements **Parametric Modeling** (Autoregressive - AR, and Autoregressive Moving-Average - ARMA) to resolve these limits, producing smooth and highly accurate spectral envelopes.

---

## 🛠️ Implemented Architectural Methods
- **Classical Approach:** Fast Fourier Transform (FFT) and global spectral analysis.
- **Parametric AR Estimation:** Auto-Regressive modeling via **Yule-Walker** and **Burg** algorithms.
- **Parametric ARMA Estimation:** Combined Auto-Regressive Moving Average modeling using rational filter fitting.
- **Time-Frequency Localization:** Local temporal segmentation adapted specifically for tracking non-stationary characteristics in audio signals.

---

## 📊 Phase 1: Primary MATLAB Audio Exploration
The foundational exploration was executed in MATLAB, resolving the temporal and spectral trends of the acoustic signal:

### 1. Time-Frequency Localization (Spectrogram)
To track how the spectral energy shifts across non-stationary time frames, a Short-Time block analysis was generated:

![Time Evolution of AR Spectrum](1000024738.jpg)

### 2. Modern Resonant Envelope Extraction (Burg PSD)
Using parametric modeling, the underlying system poles were mapped to track cleanly up to the higher frequency bands:

![PSD Burg Method](1000024737.jpg)

---

## 🐍 Phase 2: Python Cross-Platform Calibration & Verification
To ensure open-source accessibility, a parallel validation code was engineered to bypass compiled C-library dependencies, making it fully operational on mobile setups like **Pydroid 3**:

* **Pure Python Matrix Solvers:** Re-coded Yule-Walker using Toeplitz matrices and the Burg algorithm via pure Levinson-Durbin recursions using only `numpy` and `scipy`.
* **Custom ARMA Fitter:** Replicated MATLAB's frequency-domain equation error method (`invfreqz`) from scratch using Linear Least Squares (`numpy.linalg.lstsq`).

### 📈 Cross-Platform Verification Plot:

![Comparison of Spectral Methods](1000024743.jpg)

---

## 🏁 Algorithmic Comparison Matrix & Insights

| Performance Metric | FFT (Classical) | AR Yule-Walker (Parametric) | AR Burg (Parametric) | ARMA (Parametric) |
| :--- | :--- | :--- | :--- | :--- |
| **Mathematical Base** | Discrete Fourier Transform | All-Pole ($1/A(z)$) Autocorrelation | All-Pole ($1/A(z)$) Lattice Prediction | Pole-Zero ($B(z)/A(z)$) Least Squares |
| **Spectral Variance** | **High** (Noisy baseline floor) | **Zero** (Extremely smooth envelope) | **Zero** (Ultra-clean noise floor) | **Zero** (Smooth dynamic curve) |
| **Frequency Resolution** | Poor for short samples ($\approx 1/N$) | Moderate (Minor peak blurring) | **Exceptional** (Ultra-sharp resonant peaks) | High (Maps both peaks and notches) |
| **Dynamic Range** | Limited by window sidelobes | Moderate (Underestimates deep valleys) | **Extremely High** (Drops near $-170\text{ dB}$) | **Excellent** (Maps precise drop notches) |

### Key Signal Processing Deductions:
1. **Variance Reduction:** The FFT (grey curve) displays rapid random noise fluctuations. Parametric models act as statistical smoothers, highlighting only the true physical resonances.
2. **Burg vs. Yule-Walker:** The Burg method (blue curve) yields sharper peaks and a cleaner dynamic range because it avoids windowing the finite data records, preserving boundary statistics.
3. **The Role of Zeros (ARMA):** While pure AR models only track peaks (poles), the ARMA model (green curve) introduces sharp drops in the spectrum (such as the notch near $750\text{ Hz}$). This is critical for capturing acoustic anti-resonances.

---

## 💻 Repository Directory Layout
As displayed in the repository interface, all operational scripts and evaluation assets are hosted directly within the root working directory:

```text
├── README.md               # Complete project documentation & comparison matrix
├── Python_Implementation.py # Pure NumPy/SciPy parallel validation pipeline
├── spectral_analysis.m     # Core MATLAB validation and exploration script
├── 1000024737.jpg          # MATLAB Burg PSD Plot
├── 1000024738.jpg          # MATLAB Spectrogram Plot
└── 1000024743.jpg          # Python Multi-Method Verification Plot
