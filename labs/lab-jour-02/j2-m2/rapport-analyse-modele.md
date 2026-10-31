# Rapport d'analyse — NordMail v2

Auteur : `<initiales>` — Date : `<AAAA-MM-JJ>` — Cible : image `j2m1-app:1`, pile `../j2-m1/`.

## 1. Inventaire

| Question | Réponse |
| --- | --- |
| Commande de collecte | `<commande exacte>` |
| Base de vulnérabilités et date | `<UpdatedAt / NextUpdate>` |
| Constats bruts | `<n>` (Trivy), `<n>` lignes (pip-audit) |
| Constats distincts après dédoublonnage des alias | `<n>` |
| Composants déclarés / résolus / présents dans l'image | `<n> / <n> / <n>` |

## 2. Classement

Cinq constats, classés par exploitation connue puis par exposition, pas par score.

| Rang | ID | Composant | CVSS | EPSS | KEV | Atteignable depuis une route ? | Décision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |

Le constat classé premier par CVSS est-il premier ici ? `<oui/non>`, parce que `<raison>`.

## 3. Corrections et preuves

| Constat | Fichier modifié | Preuve avant | Preuve après |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |

## 4. Ce que les outils n'ont pas vu

Trois lignes : un défaut présent dans le code et absent des rapports, un défaut
absent des trois inventaires, une vulnérabilité sans correctif et le contrôle
qui la réduit.

- `<défaut>` : `<pourquoi aucun outil ne le voit>`.
- `<défaut>` : `<idem>`.
- `<CVE sans correctif>` : `<atténuation retenue, date de réexamen>`.

## 5. Effet sur le pipeline

`<Ce que le registre change dans le Jenkinsfile : seuil, échéance, build bloqué ou non.>`
