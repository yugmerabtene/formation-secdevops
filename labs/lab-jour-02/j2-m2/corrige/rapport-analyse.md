# Rapport d'analyse — NordMail v2

Auteur : formateur — Date : 2026-10-31 — Cible : image `j2m1-app:1`, pile `../j2-m1/`.

## 1. Inventaire

| Question | Réponse |
| --- | --- |
| Commande de collecte | `trivy fs --scanners vuln --format json travail/app` et `pip-audit -r travail/app/requirements.txt --format json` |
| Base de vulnérabilités et date | Trivy 0.71.2, base du 2026-10-30, prochaine mise à jour le 2026-10-31 |
| Constats bruts | 17 (Trivy), 33 lignes (pip-audit) |
| Constats distincts après dédoublonnage des alias | 17 CVE |
| Composants déclarés / résolus / présents dans l'image | 5 / 12 / 101 |

Les trois nombres de constats décrivent le même risque : 17 vulnérabilités
distinctes, 33 lignes parce que pip-audit répète chaque identifiant sous ses
alias, 1 seule au-dessus du seuil HIGH.

## 2. Classement

| Rang | ID | Composant | CVSS | EPSS | KEV | Atteignable depuis une route ? | Décision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CODE-03 | app.py:86 | non calculé | non applicable | non | oui, `/ping?hote=` | planifiée, 2026-11-07 |
| 2 | CODE-02 | app.py:73 | non calculé | non applicable | non | oui, `/recherche?q=` | planifiée, 2026-11-07 |
| 3 | CODE-01 | app.py:79 | non calculé | non applicable | non | oui, `/export?fichier=` | corrigée |
| 4 | CVE-2024-34069 | Werkzeug 2.3.4 | 7.5 | 0.03397 | non | oui, `debug=True` active la console | corrigée |
| 5 | CVE-2023-46136 | Werkzeug 2.3.4 | 7.5 | 0.01288 | non | non, aucune route n'accepte de `multipart` | corrigée |

Un classement par CVSS place CVE-2024-34069 en tête, à 7,5 — score fourni par la
rubrique GHSA du rapport, la rubrique NVD y étant vide. Le classement retenu
place trois défauts de code devant, parce qu'une seule requête les atteint et
qu'aucun correctif de bibliothèque ne les fermera. Un constat de code n'a pas de
score tant que l'organisation ne l'a pas calculé : la colonne porte
« non calculé », elle ne s'invente pas.

## 3. Corrections et preuves

| Constat | Fichier modifié | Preuve avant | Preuve après |
| --- | --- | --- | --- |
| CODE-01 | `app.py`, `safe_join` sur `BASE_EXPORT` | `200 b'root:x:0:0:root:/roo'` | `404 b'{"erreur":"fichier incon'`, et `200 b'export de demonstration'` sur `notes.txt` |
| 17 CVE de dépendances | `requirements.txt` : Flask 3.1.3, Werkzeug 3.1.9, Jinja2 3.1.6, requests 2.33.0 | `Total: 17 (LOW: 1, MEDIUM: 15, HIGH: 1, CRITICAL: 0)` | `requirements.txt │ pip │ 0`, code 0 |

Les deux preuves de CODE-01 viennent du client de test de Flask exécuté dans
l'image `j2m1-app:1`, sans serveur ni port. La compatibilité des versions
montées a été vérifiée par `from app import app` dans un environnement Python
3.14 avec ces quatre versions.

## 4. Ce que les outils n'ont pas vu

- `POST /admin/purge` sans contrôle d'accès : aucun des cinq outils du jour 2 ne
  teste l'autorisation, seule une relecture du code la trouve.
- Une attaque inédite de la chaîne de dépendances, comme la porte dérobée
  xz-utils de mars 2024 : aucune base ne la connaît avant sa révélation, le SBOM
  sert à mesurer l'exposition après coup.
- 164 des 187 constats de l'image `j2m1-app:1` n'ont aucune version corrigée
  publiée, dont 44 HIGH : la décision est la cadence de reconstruction de
  l'image et la fermeture des ports, pas une correction de paquet.

## 5. Effet sur le pipeline

Le seuil bloquant reste HIGH, mais une vulnérabilité présente au catalogue KEV
bloque désormais sans condition de sévérité : KEV passe avant le score. Les
constats ouverts vivent dans le registre avec une échéance par sévérité, et le
tableau de bord compte les constats dont l'échéance est dépassée, pas le nombre
total de constats.
