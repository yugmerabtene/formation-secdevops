# Registre des vulnérabilités — NordMail

Registre du 2026-10-31, application NordMail v2, image `j2m1-app:1`, base Trivy
du 2026-10-30. Une ligne par constat distinct : un défaut vu par deux outils ne
compte qu'une fois, et un constat écarté reste écrit.

| ID | Composant | Sévérité | CVSS | EPSS | KEV | Décision | Propriétaire | Détecté le | Échéance | Autorité / réexamen | Preuve |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CVE-2024-34069 | Werkzeug 2.3.4 | HIGH | 7.5 | 0.03397 | non | corrigée | resp-dependances | 2026-10-31 | 2026-11-30 | sans objet | `trivy fs travail/app` rend 0 constat après montée en Werkzeug 3.1.9 |
| CVE-2023-46136 | Werkzeug 2.3.4 | MEDIUM | 7.5 | 0.01288 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2024-49767 | Werkzeug 2.3.4 | MEDIUM | 7.5 | 0.01095 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2024-47081 | requests 2.31.0 | MEDIUM | 5.3 | 0.00980 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2024-34064 | Jinja2 3.1.2 | MEDIUM | 5.4 | 0.00979 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2024-22195 | Jinja2 3.1.2 | MEDIUM | 6.1 | 0.00892 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2024-49766 | Werkzeug 2.3.4 | MEDIUM | 5.3 | 0.00776 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2026-27199 | Werkzeug 2.3.4 | MEDIUM | 5.3 | 0.00631 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2025-66221 | Werkzeug 2.3.4 | MEDIUM | 5.3 | 0.00547 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2024-56326 | Jinja2 3.1.2 | MEDIUM | 7.8 | 0.00522 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2025-27516 | Jinja2 3.1.2 | MEDIUM | 8.8 | 0.00507 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2026-21860 | Werkzeug 2.3.4 | MEDIUM | 5.3 | 0.00475 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2026-27205 | Flask 2.3.2 | LOW | 4.3 | 0.00400 | non | corrigée | resp-dependances | 2026-10-31 | 2027-04-29 | sans objet | idem, 0 constat |
| CVE-2026-102598 | Werkzeug 2.3.4 | MEDIUM | 5.3 | 0.00370 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2024-35195 | requests 2.31.0 | MEDIUM | 5.6 | 0.00340 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2024-56201 | Jinja2 3.1.2 | MEDIUM | 8.8 | 0.00307 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CVE-2026-25645 | requests 2.31.0 | MEDIUM | 5.5 | 0.00189 | non | corrigée | resp-dependances | 2026-10-31 | 2027-01-29 | sans objet | idem, 0 constat |
| CODE-01 | app.py:79 | CRITICAL | non calculé | non applicable | non | corrigée | dev-nordmail | 2026-10-31 | 2026-11-07 | sans objet | `/export?fichier=%2Fetc%2Fpasswd` : 200 et `root:x:0:0` avant, 404 après `safe_join` |
| CODE-02 | app.py:73 | CRITICAL | non calculé | non applicable | non | planifiée | dev-nordmail | 2026-10-31 | 2026-11-07 | sans objet | ZAP [90035] et règle `nordmail-gabarit-utilisateur` : injection de gabarit, correction en cours |
| CODE-03 | app.py:86 | CRITICAL | non calculé | non applicable | non | planifiée | dev-nordmail | 2026-10-31 | 2026-11-07 | sans objet | ZAP [90020] et règle `nordmail-shell-concatene` : `shell=True` sur une commande concaténée |
| CODE-04 | app.py:103 | HIGH | non calculé | non applicable | non | planifiée | dev-nordmail | 2026-10-31 | 2026-11-30 | sans objet | `debug=True` laissé dans `app.run` ; la console Werkzeug est active sur le port 8099 |
| CODE-05 | app.py:92 | HIGH | non calculé | non applicable | non | planifiée | dev-nordmail | 2026-10-31 | 2026-11-30 | sans objet | Relecture manuelle : `POST /admin/purge` sans contrôle d'accès, aucun outil ne le signale |
| CODE-06 | app.py:99 | LOW | non calculé | non applicable | non | planifiée | dev-nordmail | 2026-10-31 | 2027-04-29 | sans objet | Règle `nordmail-empreinte-md5` : MD5 sur un jeton, sans preuve d'exploitation |
| CODE-07 | /export | MEDIUM | non applicable | non applicable | non | fausse alerte | dev-nordmail | 2026-10-31 | 2026-11-30 | sans objet | ZAP [30001] : preuve réduite à `Connection: close`, aucune charge rejouable |
| BASE-01 | python:3.12-slim, 44 HIGH sans correctif | HIGH | non calculé | non applicable | non | atténuée | resp-plateforme | 2026-10-31 | 2026-11-30 | resp-plateforme / 2027-01-29 | `trivy image` : 44 HIGH restent sans version corrigée ; port publié limité à `127.0.0.1`, exécution sous `10001`, reconstruction planifiée |

## Lecture

17 constats de dépendances, 7 constats de code et un constat d'image, dont 18
corrigés, 5 planifiés, 1 atténué et 1 écarté. Les 44 constats HIGH sans version
corrigée chez Debian tiennent en une ligne : ils relèvent d'une cadence de
reconstruction et d'un réexamen daté, pas d'une correction de paquet.
