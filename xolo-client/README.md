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


EN DOCKER:

# Listar todas las políticas
docker run --rm --network ricardoibarra_abac-network -v $PWD/xolo-client:/data xolo-client list

# Obtener una política
docker run --rm --network ricardoibarra_abac-network -v $PWD/xolo-client:/data xolo-client get P1

# Crear políticas desde archivo
docker run --rm --network ricardoibarra_abac-network -v $PWD/xolo-client:/data xolo-client create /data/policies.json

# Eliminar una política
docker run --rm --network ricardoibarra_abac-network -v $PWD/xolo-client:/data xolo-client delete P13

# Actualizar una política
docker run --rm --network ricardoibarra_abac-network -v $PWD/xolo-client:/data xolo-client update P12 /data/policy_update.json

# Inyectar una política directamente al evaluador
docker run --rm --network ricardoibarra_abac-network -v $PWD/xolo-client:/data xolo-client inject /data/policy_to_inject.json

# Preparar comunidades
docker run --rm --network ricardoibarra_abac-network -v $PWD/xolo-client:/data xolo-client prepare

# Evaluar una solicitud
docker run --rm --network ricardoibarra_abac-network -v $PWD/xolo-client:/data xolo-client evaluate /data/request.json

# Evaluar lote de solicitudes
docker run --rm --network ricardoibarra_abac-network -v $PWD/xolo-client:/data xolo-client evaluate-batch /data/requests.json

PARA KUBERNETES:

# Iniciar minikube si no está iniciado
minikube start

# Entrar  al entorno de minikube
eval $(minikube docker-env)

# Construir la imagen del server localmente:
docker build -t xolo-api ./xolo-api

# Construir la imagen del cliente localmente:
docker build -t xolo-client ./xolo-client

# Construir la imagen del runner localmente:
docker build -f k8s/trace-runner.Dockerfile -t trace-runner k8s/

# Aplicar manifiesto (sin traer la imagen de docker hub)
kubectl apply -f k8s/deployments/xolo-api-deployment.yaml

# Iniciar servicio
minikube service xolo-api

# Ejecutar jobs
kubectl apply -f k8s/jobs/job_create.yaml
kubectl apply -f k8s/jobs/job_prepare.yaml
kubectl apply -f k8s/jobs/job_trace_runner.yaml

# Detener servicio y eliminar jobs
kubectl delete service xolo-api
kubectl delete deployment xolo-api

kubectl delete job xolo-client-create
kubectl delete job xolo-client-evaluate
kubectl delete job xolo-client-prepare
kubectl delete job trace-runner
kubectl delete job xolo-client-evaluate-batch