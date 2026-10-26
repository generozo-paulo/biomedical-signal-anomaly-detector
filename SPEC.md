# Especificação Contratual (SDD) - Biomedical Signal Anomaly Detector (ECG & Telemetry)

## 1. Escopo & Objetivos
Detecção de arritmias ventriculares e anomalias hemodinâmicas em tempo real em traçados de Eletrocardiograma (ECG de derivação DII e V5).
Utiliza decomposição de ondaletas (Wavelets), detecção de complexos QRS (Pan-Tompkins) e autoencoders/modelos de isolamento para identificar:
- Taquicardia Ventricular (TV)
- Extrassístoles Ventriculares Prematuras (PVC)
- Fibrilação Atrial (FA) com ritmo irregular R-R

## 2. Contratos de Entrada (Pydantic)

### 2.1 Janela de Sinal Biomédico (`ECGSignalWindow`)
- `patient_id`: str
- `sampling_rate_hz`: int = 250
- `duration_seconds`: float = 10.0
- `simulated_arrhythmia_type`: Literal["NORMAL_SINUS", "VENTRICULAR_TACHYCARDIA", "PVC_PREMATURE", "ATRIAL_FIBRILLATION"]

## 3. Contratos de Saída (Pydantic)

### 3.1 Relatório de Análise Eletrocardiográfica (`ECGAnomalyReport`)
- `timestamp`: str
- `patient_id`: str
- `mean_heart_rate_bpm`: float
- `heart_rate_variability_rmssd`: float
- `anomaly_detected`: bool
- `classified_rhythm`: str
- `urgency_level`: Literal["NORMAL", "MONITOR", "STAT_EMERGENCY"]
- `detected_complexes_count`: int
