# Dockerfile de démonstration : quatre défauts volontaires, signalés par
# hadolint et par le scan d'image. Ne pas copier dans un projet réel.
FROM python:3.9-slim
WORKDIR /app
ADD app.py /app/app.py
ADD requirements.txt /app/requirements.txt
RUN cd /app && pip install -r requirements.txt
USER root
EXPOSE 5000
CMD ["python", "app.py"]
