# Image de démonstration durcie a minima : utilisateur non privilégié,
# pas de bytecode écrit sur disque, sortie Python non bufferisée pour que
# les logs arrivent en temps réel dans `docker compose logs`.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Utilisateur non privilégié créé après l'installation des dépendances
# (l'installation a besoin de root, l'exécution non).
RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin appuser

COPY --chown=appuser:appuser app.py ./

USER 10001

EXPOSE 8000

CMD ["python", "app.py"]
