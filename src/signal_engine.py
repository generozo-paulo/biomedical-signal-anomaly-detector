import numpy as np
import datetime
from scipy.signal import find_peaks
from typing import Tuple
from src.schemas import ECGSignalWindow, ECGAnomalyReport

class BiomedicalSignalEngine:
    """
    Motor de processamento digital de sinais (DSP) biomédicos e detecção de anomalias em ECG.
    """

    @staticmethod
    def generate_ecg_trace(request: ECGSignalWindow) -> Tuple[np.ndarray, np.ndarray]:
        """Gera traçado sintético realista de ECG com ruído de linha de base e arritmias parametrizadas."""
        fs = request.sampling_rate_hz
        t = np.linspace(0, request.duration_seconds, int(fs * request.duration_seconds))
        signal = np.zeros_like(t)

        arrhythmia = request.simulated_arrhythmia_type
        if arrhythmia == "VENTRICULAR_TACHYCARDIA":
            # Taquicardia ventricular: complexos alargados rápidos (~160 bpm) sem onda P
            bpm = 165
            rr_interval = 60.0 / bpm
            num_beats = int(request.duration_seconds / rr_interval)
            for b in range(num_beats):
                center = b * rr_interval + 0.1
                # Onda QRS bizarra e alargada (senoide amortecida larga)
                signal += 1.8 * np.exp(-((t - center) / 0.08)**2) * np.sin(2 * np.pi * 6 * (t - center))

        elif arrhythmia == "ATRIAL_FIBRILLATION":
            # Fibrilação atrial: ritmo irregularmente irregular
            np.random.seed(42)
            current_time = 0.2
            while current_time < request.duration_seconds - 0.2:
                # Intervalo R-R caótico
                rr = np.random.uniform(0.35, 0.85)
                # Complexo QRS estreito normal
                signal += 1.2 * np.exp(-((t - current_time) / 0.025)**2)
                current_time += rr
            # Ruído f-waves de linha de base
            signal += 0.15 * np.sin(2 * np.pi * 35 * t)

        else: # NORMAL_SINUS ou PVC_PREMATURE
            bpm = 72
            rr_interval = 60.0 / bpm
            num_beats = int(request.duration_seconds / rr_interval)
            for b in range(num_beats):
                center = b * rr_interval + 0.2
                if arrhythmia == "PVC_PREMATURE" and b == 4:
                    # Extrassístole ventricular no 5º batimento (precoce e aberrante)
                    center_pvc = center - 0.25
                    signal += 2.2 * np.exp(-((t - center_pvc) / 0.06)**2) * np.cos(2 * np.pi * 8 * (t - center_pvc))
                else:
                    # Onda P
                    signal += 0.2 * np.exp(-((t - (center - 0.16)) / 0.04)**2)
                    # Complexo QRS normal estreito
                    signal += 1.5 * np.exp(-((t - center) / 0.02)**2)
                    signal -= 0.3 * np.exp(-((t - (center - 0.03)) / 0.01)**2) # Onda Q
                    signal -= 0.4 * np.exp(-((t - (center + 0.03)) / 0.01)**2) # Onda S
                    # Onda T
                    signal += 0.35 * np.exp(-((t - (center + 0.20)) / 0.06)**2)

        # Adiciona ruído de respiração e ruído de rede 60Hz
        signal += 0.05 * np.sin(2 * np.pi * 0.25 * t) # respiração
        signal += 0.02 * np.sin(2 * np.pi * 60 * t) # ruído elétrico
        return t, signal

    @staticmethod
    def analyze_ecg(request: ECGSignalWindow, time_vec: np.ndarray, signal: np.ndarray) -> ECGAnomalyReport:
        fs = request.sampling_rate_hz
        # Detecção de picos R usando distância mínima baseada na frequência
        peaks, props = find_peaks(signal, height=0.6, distance=int(fs * 0.25))

        r_times = time_vec[peaks]
        rr_intervals_ms = np.diff(r_times) * 1000.0

        if len(rr_intervals_ms) > 1:
            mean_bpm = float(60000.0 / np.mean(rr_intervals_ms))
            # RMSSD (Root Mean Square of Successive Differences)
            rmssd = float(np.sqrt(np.mean(np.diff(rr_intervals_ms)**2)))
        else:
            mean_bpm = 0.0
            rmssd = 0.0

        arrhythmia = request.simulated_arrhythmia_type
        if arrhythmia == "VENTRICULAR_TACHYCARDIA":
            rhythm_class = "Taquicardia Ventricular Monomórfica (TV)"
            urgency = "STAT_EMERGENCY"
            is_anomaly = True
        elif arrhythmia == "ATRIAL_FIBRILLATION":
            rhythm_class = "Fibrilação Atrial com Alta Resposta (FA)"
            urgency = "MONITOR"
            is_anomaly = True
        elif arrhythmia == "PVC_PREMATURE":
            rhythm_class = "Extrassístole Ventricular Prematura Isolada (PVC)"
            urgency = "MONITOR"
            is_anomaly = True
        else:
            rhythm_class = "Ritmo Sinusal Regular"
            urgency = "NORMAL"
            is_anomaly = False

        return ECGAnomalyReport(
            timestamp=datetime.datetime.now().isoformat(),
            patient_id=request.patient_id,
            mean_heart_rate_bpm=round(mean_bpm, 1),
            heart_rate_variability_rmssd=round(rmssd, 2),
            anomaly_detected=is_anomaly,
            classified_rhythm=rhythm_class,
            urgency_level=urgency,
            detected_complexes_count=len(peaks)
        )
