import pandas as pd
import numpy as np

# Parámetros
lambda_rate = 10  # solicitudes por segundo
np.random.seed(42)

# Cargar datos
df = pd.read_csv("solicitudes_abac_kdd_refinadas.csv")

# Separar por label
df_normal = df[df['label'] == 'normal'].drop_duplicates()
df_anormal = df[df['label'] != 'normal'].drop_duplicates()

# Tomar 800 normales (permitimos duplicados si no hay suficientes únicos)
df_normal_sample = df_normal.sample(n=800, replace=True, random_state=42)

# Tomar 200 anormales diferentes
df_anormal_sample = df_anormal.sample(n=200, replace=False, random_state=42)

# Combinar y mezclar
df_trace = pd.concat([df_normal_sample, df_anormal_sample]).sample(frac=1, random_state=42).reset_index(drop=True)

# Generar tiempos de interarribo y llegada
interarrival_times = np.random.exponential(scale=1/lambda_rate, size=len(df_trace))
arrival_times = np.cumsum(interarrival_times)

# Agregar columnas
df_trace['interarrival_time'] = interarrival_times.round(3)
df_trace['timestamp'] = arrival_times.round(3)

# Guardar traza
df_trace.to_csv("traza_solicitudes_1000.csv", index=False)
