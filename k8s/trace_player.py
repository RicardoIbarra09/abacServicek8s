# trace_player.py

import pandas as pd
import time
import requests
import csv
import os
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

API_URL = "http://xolo-api:10000/api/v4/policies/evaluate/batch"
OUTPUT_DIR = "/output"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "resultados_experimento.csv")
OUTPUT_IMG = os.path.join(OUTPUT_DIR, "grafica_encolamientos.png")
METRICAS_CSV = os.path.join(OUTPUT_DIR, "metricas_experimento.csv")

# Cargar traza
df = pd.read_csv("traza_solicitudes_1000.csv")

# Inicializar cronómetro
start_time = time.time()

# Lista para guardar resultados
resultados = []

for i, row in df.iterrows():
    # Esperar según el timestamp planeado
    elapsed = time.time() - start_time
    wait_time = row["timestamp"] - elapsed
    if wait_time > 0:
        time.sleep(wait_time)

    request = [{
        "subject": {"attribute": "rol", "value": row["rol"]},
        "asset": {"attribute": "recurso", "value": row["recurso"]},
        "space": {"attribute": "ubicacion", "value": row["ubicacion"]},
        "time": {"attribute": "rango_horario", "value": row["rango_horario"]},
        "action": {"attribute": "accion", "value": row["accion"]}
    }]

    t0 = time.time()
    try:
        response = requests.post(API_URL, json=request)
        t1 = time.time()
        response_time = round(t1 - t0, 4)

        resultado = {
            "index": i + 1,
            "timestamp_planeado": row["timestamp"],
            "tiempo_respuesta": response_time,
            "codigo_http": response.status_code,
            "resultado": response.json(),
            "encolado": response_time > row["interarrival_time"],
            "label": row["label"],
            "esperado": "permit" if row["label"] == "normal" else "deny",
            "real": response.json()[0]["result"] if response.status_code == 200 else "error"
        }

        print(f"[{i+1}] {response.status_code} - {response_time}s - Encolado: {resultado['encolado']}")
        resultados.append(resultado)

    except Exception as e:
        print(f"[{i+1}] Error: {e}")

# Guardar CSV de resultados
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
    writer.writeheader()
    writer.writerows(resultados)

# Métricas
df_result = pd.DataFrame(resultados)
y_true = df_result["esperado"]
y_pred = df_result["real"]

# Generar informe
reporte = classification_report(y_true, y_pred, output_dict=True)
matriz = confusion_matrix(y_true, y_pred, labels=["permit", "deny"])

# Guardar como CSV
with open(METRICAS_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Métrica", "Valor"])
    writer.writerow(["Accuracy", reporte["accuracy"]])
    writer.writerow(["Precision (permit)", reporte["permit"]["precision"]])
    writer.writerow(["Recall (permit)", reporte["permit"]["recall"]])
    writer.writerow(["F1 Score (permit)", reporte["permit"]["f1-score"]])
    writer.writerow(["Precision (deny)", reporte["deny"]["precision"]])
    writer.writerow(["Recall (deny)", reporte["deny"]["recall"]])
    writer.writerow(["F1 Score (deny)", reporte["deny"]["f1-score"]])
    writer.writerow(["---"])
    writer.writerow(["Matriz de confusión"])
    writer.writerow(["", "Pred permit", "Pred deny"])
    writer.writerow(["Esperado permit", matriz[0][0], matriz[0][1]])
    writer.writerow(["Esperado deny", matriz[1][0], matriz[1][1]])

# Gráfica de encolamiento
conteo = df_result["encolado"].value_counts().rename({True: "Encoladas", False: "No encoladas"})
plt.figure(figsize=(6, 4))
conteo.plot(kind="bar", color=["red", "green"])
plt.title("Solicitudes encoladas vs no encoladas")
plt.ylabel("Cantidad")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_IMG)

print(f"Resultados en: {OUTPUT_CSV}")
print(f"Métricas en: {METRICAS_CSV}")
print(f"Gráfica exportada en: {OUTPUT_IMG}")
