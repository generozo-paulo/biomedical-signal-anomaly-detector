# CRISP-DM: Entendimento de Negócio (Detecção de Arritmias Cardíacas)

## 1. Problema Clínico
Alarmes falsos em UTI geram fadiga de alarmes (*alarm fatigue*), levando equipes médicas a desativarem ou ignorarem notificações críticas de monitores multiparamétricos.
Por outro lado, taquicardias ventriculares sustentadas levam a colapso hemodinâmico e parada cardiorrespiratória em questão de segundos.

## 2. Requisitos Técnicos
- Processamento em tempo real a 250 Hz.
- Extração de picos R robusta a ruído muscular e oscilação de linha de base.
- Cálculo de variabilidade da frequência cardíaca (HRV / RMSSD).
- Filtragem de falsos positivos com classificação do ritmo.
