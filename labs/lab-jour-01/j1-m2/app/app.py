"""API de notes NordMail — version de démonstration du module J1-M2.

FICHIER PÉDAGOGIQUE : trois défauts sont volontaires et décrits dans le
module J1-M2. Ne pas copier ce fichier dans un projet réel.

Défauts volontaires :
1. `admin_password` est écrit dans le source (Bandit B105).
2. `API_KEY` est une clé en clair qui ressemble à un secret (gitleaks).
3. Le serveur démarre avec `debug=True` (Bandit B201).
"""

from flask import Flask, jsonify, request

app = Flask(__name__)
app.secret_key = "cle-de-session-exemple"
admin_password = "mot-de-passe-exemple"

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
    app.run(host="0.0.0.0", port=5000, debug=True)
