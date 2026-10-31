#!/usr/bin/env python3
"""Classe un rapport Trivy JSON par exploitation connue, pas par score.

Usage : python3 outils/prioriser.py rapport.json
Réseau requis : API EPSS (FIRST) et catalogue KEV (CISA), tous deux publics.
Le CVSS affiché vient de la première rubrique renseignée du rapport — NVD,
GHSA puis Red Hat — avec sa source : un score absent de la rubrique NVD n'est
pas un score absent.
"""
import json
import sys
import urllib.request

EPSS = "https://api.first.org/data/v1/epss?cve="
KEV = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
SOURCES = ("nvd", "ghsa", "redhat")


def lire(url):
    with urllib.request.urlopen(url, timeout=30) as reponse:
        return json.load(reponse)


def score(constat):
    cvss = constat.get("CVSS", {}) or {}
    for source in SOURCES:
        valeur = (cvss.get(source) or {}).get("V3Score")
        if valeur:
            return valeur, source
    return None, "aucune"


rapport = json.load(open(sys.argv[1]))
lignes = [
    (v["VulnerabilityID"], v["PkgName"], v["Severity"], *score(v))
    for r in rapport.get("Results", [])
    for v in r.get("Vulnerabilities") or []
]
cves = sorted({ligne[0] for ligne in lignes})
if not cves:
    print("aucun constat : rien à classer")
    sys.exit(0)
epss = {d["cve"]: float(d["epss"]) for d in lire(EPSS + ",".join(cves))["data"]}
kev = {v["cveID"] for v in lire(KEV)["vulnerabilities"]}
for cve, paquet, gravite, cvss, source in sorted(
        lignes, key=lambda l: (l[0] in kev, epss.get(l[0], 0)), reverse=True):
    print(f"{cve:16} {paquet:10} {gravite:7} CVSS {str(cvss):5} {source:6} "
          f"EPSS {epss.get(cve, 0):.5f} KEV {'oui' if cve in kev else 'non'}")
