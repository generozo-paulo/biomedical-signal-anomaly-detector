import pytest
import numpy as np
from src.schemas import ECGSignalWindow
from src.signal_engine import BiomedicalSignalEngine

def test_normal_sinus_ecg():
    req = ECGSignalWindow(
        patient_id="TEST-NORMAL",
        sampling_rate_hz=250,
        duration_seconds=10.0,
        simulated_arrhythmia_type="NORMAL_SINUS"
    )
    t, sig = BiomedicalSignalEngine.generate_ecg_trace(req)
    report = BiomedicalSignalEngine.analyze_ecg(req, t, sig)
    assert report.anomaly_detected is False
    assert report.urgency_level == "NORMAL"
    assert 60 <= report.mean_heart_rate_bpm <= 85

def test_ventricular_tachycardia_emergency():
    req = ECGSignalWindow(
        patient_id="TEST-VT",
        sampling_rate_hz=250,
        duration_seconds=8.0,
        simulated_arrhythmia_type="VENTRICULAR_TACHYCARDIA"
    )
    t, sig = BiomedicalSignalEngine.generate_ecg_trace(req)
    report = BiomedicalSignalEngine.analyze_ecg(req, t, sig)
    assert report.anomaly_detected is True
    assert report.urgency_level == "STAT_EMERGENCY"
    assert "Ventricular" in report.classified_rhythm
