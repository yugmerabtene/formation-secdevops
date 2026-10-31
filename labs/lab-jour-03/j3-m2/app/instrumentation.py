# app/instrumentation.py — à insérer dans app/app.py après la déclaration des notes
import threading
import time

LOKI_URL = os.environ.get("LOKI_URL", "http://loki:3100/loki/api/v1/push")
VERROU, COMPTEURS = threading.Lock(), {"requetes": {}, "webhooks": 0}


def journal(niveau, message):
    charge = {"streams": [{"stream": {"job": "nordmail", "niveau": niveau},
                           "values": [[str(time.time_ns()), message]]}]}
    try:
        requests.post(LOKI_URL, json=charge, timeout=1)
    except requests.RequestException:
        pass


@app.after_request
def tracer(reponse):
    with VERROU:
        cle = (request.path, str(reponse.status_code))
        COMPTEURS["requetes"][cle] = COMPTEURS["requetes"].get(cle, 0) + 1
    if reponse.status_code >= 400:
        journal("erreur", f"{reponse.status_code} {request.path} depuis {request.remote_addr}")
    return reponse

@app.get("/metrics")
def metriques():
    lignes = ["# TYPE nordmail_requetes_total counter"]
    with VERROU:
        lignes += [f'nordmail_requetes_total{{route="{r}",code="{c}"}} {n}'
                   for (r, c), n in sorted(COMPTEURS["requetes"].items())]
        webhooks = COMPTEURS["webhooks"]
    lignes += ["# TYPE nordmail_webhook_alertes_total counter",
               f"nordmail_webhook_alertes_total {webhooks}"]
    return "\n".join(lignes) + "\n", 200, {"Content-Type": "text/plain; version=0.0.4"}


@app.post("/webhook-alerte")
def webhook_alerte():
    charge = request.get_json(silent=True) or {}
    noms = [a.get("labels", {}).get("alertname", "?") for a in charge.get("alerts", [])]
    with VERROU:
        COMPTEURS["webhooks"] += 1
    journal("alerte", f"notification {charge.get('status')} {','.join(noms)}")
    return jsonify({"recu": len(charge.get("alerts", []))}), 200
