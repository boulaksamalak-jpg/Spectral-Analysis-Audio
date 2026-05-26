clc;
clear;
close all;

%% ============================================
% Spectral Analysis of Audio Signals
% This script works on ANY .wav file
% Just change the filename below
% Malak BOULAKSA 
% ============================================

%% ============================================
% 1. CHOOSE YOUR AUDIO FILE
% ============================================

% Change this to the name of your .wav file
filename = 'sample-1.wav';   % <-- MODIFY THIS LINE

% Check if file exists
if ~exist(filename, 'file')
    error('File "%s" not found. Please check the filename or path.', filename);
end

%% ============================================
% 2. LOAD THE SIGNAL
% ============================================

[x, Fs] = audioread(filename);   % Load audio signal
x = x(:,1);                      % Mono channel
t = (0:length(x)-1)/Fs;          % Time axis

figure
plot(t, x)
title(['Audio Signal: ' filename])
xlabel('Time (s)')
ylabel('Amplitude')

%% ============================================
% 3. CHECK NON-STATIONARITY (Spectrogram)
% ============================================

figure
spectrogram(x, 256, 200, 256, Fs, 'yaxis')
title(['Signal Spectrogram: ' filename])
xlabel('Time (s)')
ylabel('Frequency (Hz)')

%% ============================================
% 4. FFT SPECTRAL ANALYSIS
% ============================================

N = length(x);
X = fft(x);
f = (0:N-1) * (Fs / N);

figure
plot(f, 20*log10(abs(X)))
title('FFT Spectrum')
xlabel('Frequency (Hz)')
ylabel('Amplitude (dB)')
xlim([0 Fs/2])

%% ============================================
% 5. AR MODEL - YULE-WALKER METHOD
% ============================================

p = 10;      % Model order

[a, e] = aryule(x, p);
[H_ar, f_ar] = freqz(sqrt(e), a, 1024, Fs);

figure
plot(f_ar, 20*log10(abs(H_ar)))
title('PSD using AR Model (Yule-Walker)')
xlabel('Frequency (Hz)')
ylabel('Amplitude (dB)')

%% ============================================
% 6. AR MODEL - BURG METHOD
% ============================================

[a_burg, e_burg] = arburg(x, p);
[H_burg, f_burg] = freqz(sqrt(e_burg), a_burg, 1024, Fs);

figure
plot(f_burg, 20*log10(abs(H_burg)))
title('PSD - Burg Method')
xlabel('Frequency (Hz)')
ylabel('Amplitude (dB)')

%% ============================================
% 7. LOCAL ANALYSIS (NON-STATIONARY SIGNALS)
% ============================================

window_length = 1024;
noverlap = 512;

segments = buffer(x, window_length, noverlap, 'nodelay');

for i = 1:size(segments, 2)
    segment = segments(:, i);
    [a, e] = aryule(segment, p);
    [H, f] = freqz(sqrt(e), a, 512, Fs);
    PSD(:, i) = 20*log10(abs(H));
end

figure
imagesc(PSD)
axis xy
title('Time Evolution of AR Spectrum')
xlabel('Time Segments')
ylabel('Frequency Index')

%% ============================================
% 8. ARMA MODEL (without System Identification Toolbox)
% ============================================

q = 4;      % MA order

N_arma = length(x);
X_arma = fft(x);
H_arma_tf = X_arma ./ max(abs(X_arma));     % Normalization
w = linspace(0, pi, length(H_arma_tf)/2);

% Remove any NaN or Inf values
H_clean = H_arma_tf(1:length(w));
H_clean(isnan(H_clean)) = 0;
H_clean(isinf(H_clean)) = 0;

[b, a_arma] = invfreqz(H_clean, w, q, p);

[H_arma_final, f_arma] = freqz(b, a_arma, 1024, Fs);

figure
plot(f_arma, 20*log10(abs(H_arma_final)))
title('PSD - ARMA Model')
xlabel('Frequency (Hz)')
ylabel('Amplitude (dB)')

%% ============================================
% 9. GLOBAL COMPARISON
% ============================================

figure
plot(f, 20*log10(abs(X(1:length(f)))), 'k', 'LineWidth', 1)
hold on
plot(f_ar, 20*log10(abs(H_ar)), 'r', 'LineWidth', 1.5)
plot(f_burg, 20*log10(abs(H_burg)), 'b', 'LineWidth', 1.5)
plot(f_arma, 20*log10(abs(H_arma_final)), 'g', 'LineWidth', 1.5)

legend('FFT', 'AR Yule-Walker', 'AR Burg', 'ARMA')
title('Comparison of Spectral Methods')
xlabel('Frequency (Hz)')
ylabel('Amplitude (dB)')
xlim([0 Fs/2])
grid on

%% ============================================
% END OF SCRIPT
% ============================================
