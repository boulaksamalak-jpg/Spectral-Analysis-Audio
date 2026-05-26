# Comparative Framework for Parametric & Classical Spectral Analysis of Audio Signals

A cross-platform Digital Signal Processing (DSP) repository providing a side-by-side comparative evaluation of non-parametric (classical) and parametric (modern) spectral estimation methods. This project traces the entire pipeline from **MATLAB** to **Python (Pydroid 3 Compatible)** to analyze acoustic data and highlight the engineering tradeoffs of each methodology.

---

## 📌 Project Overview & Engineering Motivation
Classical Fourier analysis (FFT) is computationally efficient but suffers from fundamental limitations, namely **statistical variance** and **spectral leakage/blurring** dictated by the window length ($\Delta f \approx 1/N$). When analyzing short, noisy, or non-stationary acoustic signals (such as speech or transient musical notes), non-parametric methods often obscure closely spaced frequencies or introduce a destructive noise floor.

This project implements modern **Parametric Modeling** (Autoregressive - AR, and Autoregressive Moving-Average - ARMA) to overcome these limitations. Instead of transforming the raw data, these algorithms estimate the statistical parameters of an underlying linear system. 

To ensure open-source accessibility, the entire MATLAB processing pipeline was reverse-engineered into a mobile-ready, pure-Python script optimized for ARM environments like **Pydroid 3**.

---

## 🛠️ Implemented Architectural Methods

1. **Non-Parametric Base (Classical):**
   * **Fast Fourier Transform (FFT):** Computes raw Discrete Fourier Transform (DFT) grids to provide a baseline spectrum.
2. **Parametric AR Estimation (All-Pole Modeling, Order $p=10$):**
   * **Yule-Walker Method:** Solves the Yule-Walker matrix equations using biased autocorrelation sequences.
   * **Burg Method:** Minimizes forward and backward linear prediction errors simultaneously without data windowing, preventing spectral line splitting.
3. **Parametric ARMA Estimation (Pole-Zero Modeling, Orders $p=10, q=4$):**
   * **Frequency-Domain Rational Filter Fitting:** Employs a complex equation error formulation to compute both poles (resonances) and zeros (anti-resonances).
4. **Time-Frequency Localization:**
   * **Short-Time Analysis:** Implements windowed segmentation (`buffer` / block frames) to track time-varying spectral envelopes in non-stationary fields.

---

## 🐍 Python Cross-Platform Calibration (Pydroid 3 Workarounds)
Standard desktop Python environments rely on heavy, compiled C-libraries (such as `spectrum` or `statsmodels`) for parametric modeling. Because these libraries often fail to compile on mobile IDEs like **Pydroid 3** due to missing Fortran/C toolchains on Android, the algorithms in this repository were built **entirely from scratch using pure mathematical matrices**:

* **Mathematical Solvers:** The Yule-Walker equations were implemented utilizing `scipy.linalg.toeplitz` solvers, and Burg's lattice structures were calculated via raw Levinson-Durbin recursions.
* **Custom ARMA `invfreqz`:** To counter the depreciation and removal of `invfreqz` in modern `scipy.signal` packages, a custom **Linear Least Squares (LLS)** rational matrix fitter was engineered (`my_invfreqz`) to replicate MATLAB's exact behavior.
* **Bit-Depth Decoupling:** Raw data amplitudes from `scipy.io.wavfile` are mathematically normalized into standard float arrays bounded by $[-1, 1]$ to match MATLAB's `audioread` scale exactly, yielding perfectly overlapping decibel (dB) plots.

---

## 📊 Deep Algorithmic Comparison Matrix

Executing both scripts on a dual-tone or acoustic wav file highlights the distinct behaviors embedded within each mathematical model:

| Performance Metric | FFT (Classical) | AR Yule-Walker (Parametric) | AR Burg (Parametric) | ARMA (Parametric) |
| :--- | :--- | :--- | :--- | :--- |
| **Mathematical Structure** | Discrete Fourier Orthogonality | All-Pole ($1/A(z)$) via Autocorrelation | All-Pole ($1/A(z)$) via Lattice Prediction | Pole-Zero ($B(z)/A(z)$) Least Squares Fit |
| **Spectral Variance** | **High** (Noisy, fluctuating baseline floor) | **Zero** (Extremely smooth statistical envelope) | **Zero** (Smooth, ultra-clean noise floor) | **Zero** (Smooth curve mapping complex dynamics) |
| **Frequency Resolution** | Poor for short samples ($\approx 1/N$) | Moderate (Tends to introduce slight peak blurring) | **Exceptional** (Ultra-sharp, crisp resonant peaks) | High (Maintains sharp peaks while mapping notches) |
| **Dynamic Attenuation Range** | Limited by side-lobes & leakage | Moderate (Poor at resolving deep spectral valleys) | **Extremely High** (Drops cleanly into deep scales $\approx -170\text{ dB}$) | **Excellent** (Precisely maps deep drop notches) |
| **Primary Limitation** | Spectral leakage masks weak frequencies | Over-estimates peak bandwidths for short data | Can exhibit minor frequency shifts in high noise | High computational complexity during matrix inversion |

### Major Signal Processing Conclusions:
1. **The Variance vs. Resolution Paradox:** While the FFT captures every minor noise fluctuation, parametric models smooth out the stochastics, acting as optimal feature extractors that reveal only the true physical resonances.
2. **Burg's Edge Over Yule-Walker:** The Burg method exhibits sharper peaks and an enhanced dynamic range because it avoids windowing the finite data block, leaving boundary predictions undistorted.
3. **The Crucial Role of Zeros (ARMA):** Pure AR models can only track peaks (poles). The ARMA model's Moving Average component successfully introduces spectral nulls (zeros), allowing it to map anti-resonances (valleys) which are mathematically invisible to pure AR models.

---

## 💻 Code Repositories & Execution

### File Directory Layout
```text
├── MATLAB_Implementation.m   # Uses Signal Processing Toolbox
├── Python_Implementation.py   # Pure NumPy/SciPy (Mobile & Desktop ready)
└── my_audio.wav               # Your target acoustic validation file
## 🐍 Python Cross-Platform Validation (Pydroid 3 Compatible)
To validate the mathematical and numerical integrity of the implemented algorithms, a parallel, open-source **Python** implementation has been developed. 

This extension serves as a rigorous cross-platform benchmark, proving that the DSP equations yield identical physical results regardless of the proprietary environment.

### ⚙️ Engineering Workarounds for Mobile/Open-Source Constraints:
Since modern Python environments (and mobile IDEs like **Pydroid 3**) lack exact 1:1 built-in wrappers for advanced MATLAB Signal Processing Toolbox functions, the following custom solutions were engineered:

* **Pure Python AR Estimators:** Instead of relying on heavy, compiled external libraries (like `spectrum` or `statsmodels`) which often fail to compile on ARM-based Android architectures, **Yule-Walker** (via Toeplitz matrix solvers) and the **Burg Method** (via Levinson-Durbin and lattice filter reflection coefficients) were coded from scratch using pure `numpy` and `scipy`.
* **Custom ARMA `invfreqz` Fitting:** To bypass the removal of `invfreqz` in modern `scipy.signal` versions, a custom **Linear Least Squares (LLS)** rational transfer function fitter (`my_invfreqz`) was built. It perfectly mimics MATLAB's frequency-domain equation error method to resolve system poles and zeros.
* **Strict Signal Normalization:** Handled sample-rate preservation and bit-depth amplitude matching (`wavfile.read` amplitude casting to $[-1, 1]$) to guarantee that the absolute dB values on the Python spectral plots perfectly align with MATLAB's outputs.

---

---
*Practical project completed as part of the Advanced Signal Processing curriculum, Electronics Department.*
