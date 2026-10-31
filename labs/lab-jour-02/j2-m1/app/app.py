"""API de notes NordMail — version 2, cible des modules J2-M1 et J2-M2.

FICHIER PÉDAGOGIQUE : six défauts sont volontaires et numérotés ci-dessous.
Ne jamais copier ce fichier dans un projet réel.

Défauts volontaires :
1. `app.secret_key` est écrit dans le source.
2. `/recherche` compose un gabarit HTML avec l'entrée utilisateur (injection).
3. `/export` ouvre un fichier dont le nom vient de l'URL (traversée de chemin).
4. `/ping` passe une commande concaténée à `shell=True` (injection de commande).
5. `/admin/purge` ne vérifie aucune autorisation.
6. `hashlib.md5` sert d'empreinte de jeton.
Plus un septième, côté exécution : `debug=True` dans `app.run`.
"""

import hashlib
import os
import subprocess

import requests
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)
app.secret_key = "cle-session-nordmail-2026"  # défaut 1

BASE_EXPORT = "/srv/nordmail/export"
WEBHOOK = os.environ.get("WEBHOOK_NOTIFICATION", "http://127.0.0.1:9999/notification")

NOTES = [{"id": 1, "texte": "Relire le pipeline avant la fusion"}]


@app.get("/sante")
def sante():
    return jsonify({"statut": "ok"})


@app.get("/")
def accueil():
    """Page d'accueil : donne au scanner une porte d'entrée vers les routes."""
    return (
        "<h1>NordMail API</h1><ul>"
        '<li><a href="/notes">notes</a></li>'
        '<li><a href="/recherche?q=reunion">recherche</a></li>'
        '<li><a href="/export?fichier=notes.txt">export</a></li>'
        '<li><a href="/ping?hote=127.0.0.1">ping</a></li>'
        "</ul>"
    )


@app.get("/notes")
def lister_notes():
    return jsonify(NOTES)


@app.post("/notes")
def ajouter_note():
    contenu = request.get_json(silent=True) or {}
    texte = str(contenu.get("texte", "")).strip()
    if not texte:
        return jsonify({"erreur": "texte obligatoire"}), 400
    note = {"id": len(NOTES) + 1, "texte": texte}
    NOTES.append(note)
    try:
        requests.post(WEBHOOK, json=note, timeout=2)
    except requests.RequestException:
        pass
    return jsonify(note), 201


@app.get("/recherche")
def recherche():
    terme = request.args.get("q", "")
    return render_template_string("<h1>Résultats pour " + terme + "</h1>")  # défaut 2


@app.get("/export")
def exporter():
    nom = request.args.get("fichier", "notes.txt")
    with open(os.path.join(BASE_EXPORT, nom), "rb") as fichier:  # défaut 3
        return fichier.read()


@app.get("/ping")
def ping():
    hote = request.args.get("hote", "127.0.0.1")
    sortie = subprocess.run("ping -c 1 " + hote, shell=True, capture_output=True, text=True)  # défaut 4
    return jsonify({"code": sortie.returncode, "sortie": sortie.stdout})


@app.post("/admin/purge")
def purger():
    NOTES.clear()  # défaut 5
    return jsonify({"statut": "purge"})


@app.post("/jeton")
def jeton():
    valeur = request.args.get("valeur", "")
    return jsonify({"empreinte": hashlib.md5(valeur.encode()).hexdigest()})  # défaut 6


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
