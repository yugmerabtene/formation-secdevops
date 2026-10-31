"""API de notes NordMail — version corrigée du module J1-M2.

Les trois défauts du fichier de départ ont été retirés : plus de mot de passe
ni de clé dans le source, et le mode debug est piloté par une variable
d'environnement, désactivée par défaut.
"""

import os
import secrets

from flask import Flask, jsonify, request

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

NOTES = [{"id": 1, "texte": "Relire le pipeline avant la fusion"}]


@app.get("/sante")
def sante():
    """Point de contrôle utilisé par le déploiement."""
    return jsonify({"statut": "ok"})


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
    return jsonify(note), 201


if __name__ == "__main__":
    # L'écoute sur toutes les interfaces est voulue dans le conteneur.
    app.run(
        host="0.0.0.0",  # nosec B104
        port=5000,
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )
