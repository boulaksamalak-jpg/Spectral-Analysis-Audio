import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import freqz

# ============================================================================
# MATHEMATICAL FUNCTION: CUSTOM INVFREQZ (Least Squares ARMA Estimation)
# ============================================================================
def my_invfreqz(H, w, b_order, a_order):
    """
    Simulates MATLAB's invfreqz using Linear Least Squares.
    Fits a rational transfer function H(e^jw) = B(z)/A(z) to complex data.
    """
    m = len(w)
    A_matrix = np.zeros((m, b_order + 1 + a_order), dtype=complex)
    
    # Numerator (Zeros) matrix formulation
    for k in range(b_order + 1):
        A_matrix[:, k] = np.exp(-1j * k * w)
        
    # Denominator (Poles) matrix formulation
    for k in range(1, a_order + 1):
        A_matrix[:, b_order + k] = -H * np.exp(-1j * k * w)
        
    # Solve system using Linear Least Squares: A_matrix * c = H
    coefficients, _, _, _ = np.linalg.lstsq(A_matrix, H, rcond=None)
    
    b = coefficients[:b_order + 1]
    a = np.insert(coefficients[b_order + 1:], 0, 1.0) # a[0] = 1
    
    return np.real(b), np.real(a)

# ============================================================================
# MATHEMATICAL FUNCTION: PURE PYTHON YULE-WALKER
# ============================================================================
def pure_yule_walker(signal, order):
    """Computes AR coefficients using biased Autocorrelation method."""
    N = len(signal)
    r = np.correlate(signal, signal, mode='full')
    mid = len(r) // 2
    r_biased = r[mid:mid + order + 1] / N
    
    # Construct Toeplitz Matrix
    from scipy.linalg import toeplitz
    R_matrix = toeplitz(r_biased[:order])
    r_vector = r_biased[1:order + 1]
    
    # Solve R * a = -r
    a_raw = np.linalg.solve(R_matrix, -r_vector)
    error_variance = r_biased[0] + np.dot(a_raw, r_biased[1:order + 1])
    return a_raw, error_variance

# ============================================================================
# MATHEMATICAL FUNCTION: PURE PYTHON BURG METHOD
# ============================================================================
def pure_burg(signal, order):
    """Computes AR coefficients minimizing forward/backward prediction errors."""
    N = len(signal)
    ef = np.copy(signal)
    eb = np.copy(signal)
    a = np.zeros(order)
    error_variance = np.dot(signal, signal) / N
    
    for k in range(1, order + 1):
        # Calculate Reflection Coefficient (Lattice filter parameter)
        numerator = -2.0 * np.dot(ef[k:N], eb[k-1:N-1])
        denominator = np.dot(ef[k:N], ef[k:N]) + np.dot(eb[k-1:N-1], eb[k-1:N-1])
        rc = numerator / denominator
        
        # Update AR coefficients via Levinson-Durbin recursion
        a_old = np.copy(a)
        a[k-1] = rc
        if k > 1:
            a[:k-1] = a_old[:k-1] + rc * a_old[k-2::-1]
            
        # Update prediction errors
        ef_old = np.copy(ef)
        ef[k:N] = ef_old[k:N] + rc * eb[k-1:N-1]
        eb[k:N] = eb[k-1:N-1] + rc * ef_old[k:N]
        
        error_variance *= (1.0 - rc**2)
        
    return a, error_variance

# ============================================================================
# 1. LOAD AND PRE-PROCESS SIGNAL
# ============================================================================
filename = 'sample-1.wav'
try:
    Fs, x = wavfile.read(filename)
except FileNotFoundError:
    # Fail-safe synthesis if file is missing (Dual-tone signal: 440Hz & 1000Hz)
    Fs = 8000
    t_synth = np.linspace(0, 1, Fs)
    x = np.sin(2 * np.pi * 440 * t_synth) + 0.6 * np.sin(2 * np.pi * 1000 * t_synth)

# Convert to Mono and Normalize to [-1, 1] range to match MATLAB exactly
if len(x.shape) > 1:
    x = x[:, 0]
if x.dtype == np.int16:
    x = x / 32768.0

N = len(x)
t = np.arange(N) / Fs

# ============================================================================
# 2. SPECTRAL ESTIMATION COMPUTATIONS
# ============================================================================
# Method I: Non-Parametric FFT
X_fft = np.fft.fft(x)
f_fft = np.arange(N) * (Fs / N)

# Method II: AR Model - Yule-Walker
p_order = 10
a_yule_raw, e_yule = pure_yule_walker(x, p_order)
a_yule = np.insert(a_yule_raw, 0, 1.0)
f_ar, H_ar = freqz(np.sqrt(e_yule), a_yule, worN=1024, fs=Fs)

# Method III: AR Model - Burg Method
a_burg_raw, e_burg = pure_burg(x, p_order)
a_burg = np.insert(a_burg_raw, 0, 1.0)
f_burg, H_burg = freqz(np.sqrt(e_burg), a_burg, worN=1024, fs=Fs)

# Method IV: ARMA Model (System Identification via Frequency Domain Fit)
q_order = 4
H_arma_tf = X_fft / np.max(np.abs(X_fft))
w_arma = np.linspace(0, np.pi, len(H_arma_tf) // 2)
H_clean = np.nan_to_num(H_arma_tf[:len(w_arma)], nan=0.0, posinf=0.0, neginf=0.0)

b_arma, a_arma = my_invfreqz(H_clean, w_arma, q_order, p_order)
f_arma, H_arma_final = freqz(b_arma, a_arma, worN=1024, fs=Fs)

# ============================================================================
# 3. GLOBAL COMPARISON PLOT
# ============================================================================
plt.figure(figsize=(10, 6))
plt.plot(f_fft[:N//2], 20*np.log10(np.abs(X_fft[:N//2])), color='grey', alpha=0.5, label='FFT (Non-parametric)')
plt.plot(f_ar, 20*np.log10(np.abs(H_ar)), 'r', linewidth=1.5, label=f'AR Yule-Walker (p={p_order})')
plt.plot(f_burg, 20*np.log10(np.abs(H_burg)), 'b', linewidth=1.5, label=f'AR Burg (p={p_order})')
plt.plot(f_arma, 20*np.log10(np.abs(H_arma_final)), 'g', linewidth=1.5, label=f'ARMA (p={p_order}, q={q_order})')

plt.legend(loc='upper right')
plt.title('Comparison of Parametric and Non-Parametric Spectral Methods')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude (dB)')
plt.xlim([0, Fs/2])
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.show()

print("Execution completed successfully.")
