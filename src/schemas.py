from pydantic import BaseModel, Field
from typing import Literal

class ECGSignalWindow(BaseModel):
    patient_id: str
    sampling_rate_hz: int = Field(default=250, ge=100)
    duration_seconds: float = Field(default=10.0, ge=2.0)
    simulated_arrhythmia_type: Literal["NORMAL_SINUS", "VENTRICULAR_TACHYCARDIA", "PVC_PREMATURE", "ATRIAL_FIBRILLATION"]

class ECGAnomalyReport(BaseModel):
    timestamp: str
    patient_id: str
    mean_heart_rate_bpm: float
    heart_rate_variability_rmssd: float
    anomaly_detected: bool
    classified_rhythm: str
    urgency_level: Literal["NORMAL", "MONITOR", "STAT_EMERGENCY"]
    detected_complexes_count: int
