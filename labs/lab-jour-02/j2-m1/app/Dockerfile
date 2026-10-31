# Image de l'API NordMail v2 — cible des modules J2-M1 et J2-M2.
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN mkdir -p /srv/nordmail/export \
    && echo "export de demonstration" > /srv/nordmail/export/notes.txt

USER 10001
EXPOSE 5000
CMD ["python", "app.py"]
