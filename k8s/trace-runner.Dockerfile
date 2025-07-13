FROM python:3.10

WORKDIR /app

COPY trace_player.py .
COPY traza_solicitudes_1000.csv .

RUN pip install requests pandas matplotlib scikit-learn

CMD ["python", "trace_player.py"]
