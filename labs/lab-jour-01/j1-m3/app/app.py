"""Application Flask de démonstration pour le lab J1-M3.

Objectif : exposer des métriques Prometheus et des routes capables de
provoquer des signaux intéressants pour la surveillance :

- /boom        : erreur 5xx (panne applicative simulée)
- /slow        : latence anormale pilotée par le paramètre ?delay=<secondes>
- /login       : authentification de démonstration (401 si identifiants faux)
- /admin       : zone réservée (403 si non autorisé)
- /metrics     : exposition Prometheus (format texte)

Cette application est un support pédagogique. Elle n'est pas destinée à
être exposée sur Internet ni utilisée en production : serveur de
développement Flask, identifiants de démonstration, pas de TLS.
"""

import os
import time

from flask import Flask, Response, g, jsonify, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)

app = Flask(__name__)

# Liste fermée des routes connues : elle sert à normaliser le label
# "endpoint". Sans normalisation, chaque URL scannée par un attaquant
# créerait une nouvelle série temporelle (explosion de cardinalité).
KNOWN_ENDPOINTS = {
    "/",
    "/healthz",
    "/work",
    "/boom",
    "/slow",
    "/login",
    "/admin",
}

# Durée maximale simulée par /slow, en secondes.
MAX_SIMULATED_DELAY = 5.0

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Nombre total de requêtes HTTP traitées.",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Durée des requêtes HTTP en secondes.",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)

# Compteur dédié aux décisions d'autorisation : il permet de distinguer
# un pic de 401/403 (tentatives d'accès) d'un pic de 5xx (panne).
AUTH_DENIED = Counter(
    "app_auth_denied_total",
    "Nombre de refus d'authentification ou d'autorisation.",
    ["reason"],
)


def normalize_endpoint(path: str) -> str:
    """Ramène toute route inconnue dans la catégorie 'other'."""
    return path if path in KNOWN_ENDPOINTS else "other"


@app.before_request
def start_timer():
    """Mémorise l'instant de début, sauf pour /metrics."""
    if request.path != "/metrics":
        g.start_time = time.perf_counter()
    return None


@app.after_request
def record_metrics(response):
    """Enregistre le statut HTTP et la durée de chaque requête."""
    if request.path == "/metrics":
        return response
    endpoint = normalize_endpoint(request.path)
    REQUEST_COUNT.labels(request.method, endpoint, str(response.status_code)).inc()
    start = getattr(g, "start_time", None)
    if start is not None:
        REQUEST_LATENCY.labels(request.method, endpoint).observe(
            time.perf_counter() - start
        )
    return response


@app.get("/")
def index():
    return (
        "<h1>demo-app J1-M3</h1>"
        "<p>Routes : /work /boom /slow?delay=1.5 /login /admin /healthz /metrics</p>",
        200,
        {"Content-Type": "text/html; charset=utf-8"},
    )


@app.get("/healthz")
def healthz():
    return "ok", 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.get("/work")
def work():
    """Requête nominale, utilisée pour produire un trafic sain."""
    return jsonify(status="ok", route="/work")


@app.get("/boom")
def boom():
    """Simule une erreur serveur (5xx) : déclenche DemoAppHighErrorRate."""
    app.logger.error("Panne simulée sur /boom")
    return jsonify(error="internal error (simulated)"), 500


@app.get("/slow")
def slow():
    """Simule une latence anormale : déclenche DemoAppLatencyHigh."""
    try:
        delay = float(request.args.get("delay", "1.5"))
    except ValueError:
        delay = 1.5
    delay = max(0.0, min(delay, MAX_SIMULATED_DELAY))
    time.sleep(delay)
    return jsonify(status="ok", delay_seconds=delay)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Authentification de démonstration : tout identifiant est refusé.

    AUTH_DENIED et le statut 401 servent de signal pour la règle
    DemoAppAuthFailureSpike (hypothèse : bourrage d'identifiants).
    """
    AUTH_DENIED.labels("invalid_credentials").inc()
    return jsonify(error="unauthorized"), 401


@app.get("/admin")
def admin():
    """Zone réservée : accès refusé, utile pour simuler un balayage."""
    AUTH_DENIED.labels("forbidden").inc()
    return jsonify(error="forbidden"), 403


@app.get("/metrics")
def metrics():
    """Exposition des métriques au format texte Prometheus."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    # Serveur de développement : jamais en production.
    port = int(os.environ.get("APP_PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
