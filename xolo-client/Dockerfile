FROM python:3.10

# Instalar Poetry
RUN pip install poetry

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml poetry.lock README.md /app/

# Copiar código fuente
COPY xolo_client /app/xolo_client
COPY config /app/config
COPY tests /app/tests

# Instalar dependencias (sin virtualenv)
RUN poetry config virtualenvs.create false && poetry install

# Copiar archivos JSON para inyectar desde dentro
COPY *.json /data/

# Comando por defecto
ENTRYPOINT ["poetry", "run", "xolo-client"]



