"""API de notes NordMail, version de demonstration du module J1-M1.

FICHIER PEDAGOGIQUE : les defauts sont volontaires et decrits dans le
module J1-M1. Ni authentification, ni validation d'entree, ni cle de
signature hors du code : ce fichier ne doit pas etre deploye tel quel.
"""

import os

from flask import Flask, jsonify, request

app = Flask(__name__)

# Cle de signature des sessions ecrite dans le code source.
app.secret_key = "cle-de-session-exemple"

NOTES = {"1": "Renouveler le certificat TLS avant le 30 juin."}


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.get("/notes/<identifiant>")
def lire_note(identifiant):
    # Aucun controle d'acces : n'importe quel identifiant est lisible.
    return jsonify(identifiant=identifiant, texte=NOTES.get(identifiant))


@app.post("/notes")
def creer_note():
    # Aucune validation : un corps vide ou un champ absent fait echouer la requete.
    charge = request.get_json()
    identifiant = str(len(NOTES) + 1)
    NOTES[identifiant] = charge["texte"]
    return jsonify(identifiant=identifiant), 201


if __name__ == "__main__":
    # Mode debug actif : la console interactive Werkzeug est exposee.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
