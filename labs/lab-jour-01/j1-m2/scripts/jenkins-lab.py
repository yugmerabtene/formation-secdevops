#!/usr/bin/env python3
"""Pilote l'instance Jenkins du lab J1-M2 sans passer par l'interface.

Sous-commandes :
    valider   envoie le Jenkinsfile au convertisseur déclaratif
    creer     crée ou met à jour le job j1m2-pipeline depuis le Jenkinsfile
    lancer    crée le job, déclenche une construction et attend le verdict
    journal   affiche le journal de la dernière construction

Usage :
    python3 scripts/jenkins-lab.py valider
    python3 scripts/jenkins-lab.py lancer
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

RACINE = Path(__file__).resolve().parents[1]
JENKINSFILE = RACINE / "Jenkinsfile"
BASE = "http://localhost:8088"
JOB = "j1m2-pipeline"

COOKIES = http.cookiejar.CookieJar()
OUVREUR = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(COOKIES))


def requete(chemin: str, donnees: bytes | None = None, entetes: dict | None = None):
    url = f"{BASE}{chemin}"
    demande = urllib.request.Request(url, data=donnees, method="POST" if donnees is not None else "GET")
    for cle, valeur in (entetes or {}).items():
        demande.add_header(cle, valeur)
    return OUVREUR.open(demande, timeout=60)


def crumb() -> dict:
    """Rend l'en-tête CSRF si l'instance en exige un."""
    try:
        with requete("/crumbIssuer/api/json") as reponse:
            donnees = json.load(reponse)
        return {donnees["crumbRequestField"]: donnees["crumb"]}
    except Exception:
        return {}


def valider() -> int:
    contenu = JENKINSFILE.read_text(encoding="utf-8")
    corps = urllib.parse.urlencode({"jenkinsfile": contenu}).encode()
    entetes = {"Content-Type": "application/x-www-form-urlencoded", **crumb()}
    with requete("/pipeline-model-converter/validate", corps, entetes) as reponse:
        texte = reponse.read().decode("utf-8", errors="replace")
    print(f"HTTP {reponse.status}")
    print(texte)
    return 0 if "successfully validated" in texte else 1


def config_xml() -> bytes:
    script = escape(JENKINSFILE.read_text(encoding="utf-8"))
    return f"""<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job">
  <description>Pipeline du lab J1-M2</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps">
    <script>{script}</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
""".encode("utf-8")


def creer() -> int:
    corps = config_xml()
    entetes = {"Content-Type": "application/xml; charset=UTF-8", **crumb()}
    try:
        with requete(f"/createItem?name={JOB}", corps, entetes) as reponse:
            print(f"création du job {JOB} : HTTP {reponse.status}")
            return 0
    except urllib.error.HTTPError as erreur:
        if erreur.code != 400:
            raise
    with requete(f"/job/{JOB}/config.xml", corps, entetes) as reponse:
        print(f"mise à jour du job {JOB} : HTTP {reponse.status}")
    return 0


def dernier_numero() -> int:
    with requete(f"/job/{JOB}/api/json") as reponse:
        donnees = json.load(reponse)
    return (donnees.get("lastBuild") or {}).get("number", 0)


def lancer(attente: int) -> int:
    creer()
    avant = dernier_numero()
    entetes = crumb()
    with requete(f"/job/{JOB}/build", b"", entetes) as reponse:
        print(f"déclenchement : HTTP {reponse.status}")
    for _ in range(attente):
        time.sleep(2)
        try:
            with requete(f"/job/{JOB}/lastBuild/api/json") as reponse:
                donnees = json.load(reponse)
        except urllib.error.HTTPError as erreur:
            if erreur.code == 404:
                continue
            raise
        numero = donnees.get("number", 0)
        if numero > avant and not donnees.get("building", False):
            with requete(f"/job/{JOB}/{numero}/consoleText") as reponse:
                journal = reponse.read().decode("utf-8", errors="replace")
            print(journal)
            print(f"résultat : {donnees.get('result')} en {donnees.get('duration')} ms")
            return 0 if donnees.get("result") == "SUCCESS" else 1
    print("délai dépassé", file=sys.stderr)
    return 2


def journal() -> int:
    with requete(f"/job/{JOB}/lastBuild/consoleText") as reponse:
        print(reponse.read().decode("utf-8", errors="replace"))
    return 0


def main() -> int:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("action", choices=("valider", "creer", "lancer", "journal"))
    parseur.add_argument("--attente", type=int, default=150, help="nombre de tranches de 2 s")
    arguments = parseur.parse_args()
    actions = {
        "valider": valider,
        "creer": creer,
        "lancer": lambda: lancer(arguments.attente),
        "journal": journal,
    }
    return actions[arguments.action]()


if __name__ == "__main__":
    sys.exit(main())
