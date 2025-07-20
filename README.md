# Evaluación de solicitudes ABAC en Minikube

Este repositorio contiene todos los archivos necesarios para ejecutar un experimento de evaluación de solicitudes de acceso basado en políticas ABAC dentro de un clúster **Minikube**, utilizando trazas generadas y el cliente `xolo-client`.

---

## Requisitos previos

Antes de comenzar, asegúrate de tener lo siguiente instalado:

- [Python 3.10+](https://www.python.org/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

---

## Estructura esperada

```
abacService/
│
├── xolo-api/                     # Servicio que expone la API ABAC
├── xolo-client/                  # Cliente para evaluar políticas
├── k8s/                          # Archivos YAML para despliegue
│   ├── trace-runner-job.yaml    # Job para ejecutar la traza
│   └── ...                      # Otros manifiestos
│   ├── traza_solicitudes_100.csv
│   ├── traza_solicitudes_1000.csv
│   └── politicas_generadas.json
└── README.md
```

---

## Pasos para ejecutar el experimento

### 1. Iniciar Minikube

```bash
minikube start
```

---

### 2. Construir imágenes localmente

Asegúrate de que los Dockerfiles estén listos en `xolo-api/`, `xolo-client/`, y en el directorio del `trace-runner`. Luego ejecuta:

```bash
eval $(minikube docker-env)
docker build -t xolo-api ./xolo-api
docker build -t xolo-client ./xolo-client
docker build -f k8s/trace-runner.Dockerfile -t trace-runner k8s/
```

---

### 3. Montar directorio para resultados

En otra terminal, ejecuta (en tu propio directorio local):

```bash
minikube mount /home/ricardoibarra/abacService/k8s:/mnt/k8s
```

> Este paso es necesario para compartir un volumen persistente entre el host y el contenedor donde se guardarán los resultados (`resultados_experimento.csv`, gráficos, métricas, etc).

---

### 4. Desplegar el sistema

Desplegar los servicios necesarios, por ejemplo:

```bash
kubectl apply -f k8s/deployments/xolo-api-deployment.yaml
minikube service xolo-api
```

Verifica que el API esté corriendo:

```bash
kubectl get pods
```

Ejecuta los jobs correspondientes para crear políticas (precargadas en la imagen) y preparar las comunidades:

```bash
kubectl apply -f k8s/jobs/job_create.yaml
kubectl apply -f k8s/jobs/job_prepare.yaml
```

---

### 5. Ejecutar el experimento con el trace runner

Modifica el `k8s/trace-runner-job.yaml` para asegurarte de que el volumen esté correctamente montado:

```yaml
volumeMounts:
  - name: resultado-volume
    mountPath: /output
volumes:
  - name: resultado-volume
    hostPath:
      path: /mnt/k8s
      type: Directory
```

Después, ejecuta:

```bash
kubectl apply -f k8s/jobs/job_trace_runner.yaml
```

Verifica los logs del pod:

```bash
kubectl get pods
kubectl logs -f trace-runner-xxxx
```

---

## Archivos generados

Los resultados se almacenarán en el directorio correspondiente:

- `resultados_experimento.csv` – detalles de cada solicitud, tiempo de respuesta, encolamiento
- `grafica_encolamientos.png` – gráfico de solicitudes encoladas vs no encoladas
- `metricas_experimento.csv` – métricas de accuracy, precision, recall, F1, matriz de confusión

---

## Limpiar entorno

Puedes detener el servicio y eliminar los jobs de la siguiente manera:

```bash
kubectl delete service xolo-api
kubectl delete deployment xolo-api
kubectl delete job nombre-del-job

```

## Repetir con diferentes tasas

Puedes modificar el archivo `traza_solicitudes_1000.csv` para experimentar con diferentes tasas de llegada (`λ`) y repetir los pasos anteriores para medir capacidad de respuesta del sistema.

## Uso del cliente `xolo-client`

```bash
cd xolo-client
poetry install
poetry shell
```

Comandos disponibles:

```bash
# Listar todas las políticas
poetry run xolo-client list

# Obtener una política
poetry run xolo-client get P1

# Crear políticas desde archivo
poetry run xolo-client create policies.json

# Eliminar una política
poetry run xolo-client delete P01

# Actualizar una política
poetry run xolo-client update P1 policy_update.json

# Inyectar una política directamente al evaluador
poetry run xolo-client inject policy_to_inject.json

# Preparar comunidades
poetry run xolo-client prepare

# Evaluar una solicitud
poetry run xolo-client evaluate request.json

# Evaluar lote de solicitudes
poetry run xolo-client evaluate-batch requests.json
```


