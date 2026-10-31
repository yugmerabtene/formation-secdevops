"""Tests de l'API de notes NordMail, exécutés par l'étape `Tests`."""

import app as application

client = application.app.test_client()


def test_sante():
    reponse = client.get("/sante")
    assert reponse.status_code == 200
    assert reponse.get_json() == {"statut": "ok"}


def test_lister_notes():
    reponse = client.get("/notes")
    assert reponse.status_code == 200
    assert isinstance(reponse.get_json(), list)


def test_ajouter_note():
    reponse = client.post("/notes", json={"texte": "Note de test"})
    assert reponse.status_code == 201
    assert reponse.get_json()["texte"] == "Note de test"


def test_refuser_note_vide():
    reponse = client.post("/notes", json={})
    assert reponse.status_code == 400
