import streamlit as st
import numpy as np
import plotly.graph_objects as go
from src.schemas import ECGSignalWindow
from src.signal_engine import BiomedicalSignalEngine

st.set_page_config(
    page_title="Biomedical ECG Signal Anomaly Detector",
    page_icon="💓",
    layout="wide"
)

st.title("💓 Biomedical Signal Anomaly Detector (ECG & Telemetria)")
st.markdown("""
Processamento Digital de Sinais (DSP) e Detecção Automatizada de Arritmias Cardíacas Críticas (**Taquicardia Ventricular, Fibrilação Atrial e Extrassístoles**) com cálculo de variabilidade R-R (**RMSSD**).
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Parâmetros do Traçado ECG")
    patient_id = st.text_input("ID do Paciente (Leito UTI)", "PAC-BED-04")
    rhythm_choice = st.selectbox(
        "Ritmo Cardíaco / Arritmia Simulada:",
        ["NORMAL_SINUS", "VENTRICULAR_TACHYCARDIA", "PVC_PREMATURE", "ATRIAL_FIBRILLATION"]
    )
    duration = st.slider("Duração do Traçado (Segundos)", 5.0, 15.0, 10.0, 1.0)
    fs = st.selectbox("Taxa de Amostragem (Hz)", [250, 500], index=0)

    req = ECGSignalWindow(
        patient_id=patient_id,
        sampling_rate_hz=fs,
        duration_seconds=duration,
        simulated_arrhythmia_type=rhythm_choice
    )

    t, signal = BiomedicalSignalEngine.generate_ecg_trace(req)
    report = BiomedicalSignalEngine.analyze_ecg(req, t, signal)

    st.markdown("### 📋 Diagnóstico em Tempo Real")
    urgency_badge = "🚨 EMERGÊNCIA STAT" if report.urgency_level == "STAT_EMERGENCY" else ("⚠️ MONITORAR" if report.urgency_level == "MONITOR" else "🟢 RITMO NORMAL")
    st.metric("Classificação de Urgência", urgency_badge)
    st.info(f"**Ritmo Identificado**: {report.classified_rhythm}")
    st.metric("Frequência Cardíaca Média", f"{report.mean_heart_rate_bpm} bpm")
    st.metric("Variabilidade R-R (RMSSD)", f"{report.heart_rate_variability_rmssd} ms")
    st.metric("Batimentos Detectados", report.detected_complexes_count)

with col2:
    st.subheader("Osciloscópio Eletrocardiográfico (Derivação DII)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t,
        y=signal,
        mode='lines',
        name='Traçado DII',
        line=dict(color='#00ff41' if report.urgency_level == 'NORMAL' else '#ff3333', width=1.8)
    ))
    fig.update_layout(
        title=f"ECG Contínuo - {report.classified_rhythm}",
        xaxis_title="Tempo (segundos)",
        yaxis_title="Amplitude (mV)",
        template="plotly_dark",
        height=450,
        yaxis=dict(range=[-2.5, 3.0])
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    💡 **Critérios de Triagem Algorítmica**:
    - **Taquicardia Ventricular**: Alarme sonoro contínuo e bloqueio para cardioversão elétrica imediata.
    - **Fibrilação Atrial**: Alta variabilidade R-R e ausência de ondas P organizadas.
    """)
