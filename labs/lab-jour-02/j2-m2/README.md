# Lab J2-M2 — analyser et corriger les vulnérabilités de NordMail

Ce dossier ne contient pas de copie de l'application : le lab réutilise la pile
du module J2-M1, à l'adresse `../j2-m1/` (image `j2m1-app:1`, Compose `j2m1`,
application `127.0.0.1:8099`). Une seule pile tourne pour les deux modules, les
ports du jour 1 restent libres.

## Ce que contient ce dossier

| Chemin | Rôle |
| --- | --- |
| `outils/prioriser.py` | Joint un rapport Trivy, l'EPSS du jour et le catalogue KEV, puis classe par exploitation connue. |
| `registre-vulnerabilites-modele.md` | Modèle vide du registre à recopier en `registre-vulnerabilites.md`. |
| `rapport-analyse-modele.md` | Modèle du rapport d'analyse à recopier en `rapport-analyse.md`. |
| `scripts/verifier-registre.sh` | Contrôle de forme du registre rempli. |
| `corrige/` | Version corrigée du registre, du rapport et des deux fichiers de `app/`. |

## Réutilisation de la pile J2-M1

```bash
cd labs/lab-jour-02/j2-m2
mkdir -p travail
cp -a ../j2-m1/app/. travail/app/       # la pile J2-M1 n'est jamais modifiée
cd ../j2-m1 && docker compose up -d     # une seule pile pour les deux modules
```

Le travail se fait sur `travail/app`, copie jetable. Le `docker-compose.yml`,
l'application, le `Jenkinsfile` et `outils/semgrep-nordmail.yml` restent ceux de
J2-M1 : les modifier reviendrait à casser les preuves du module précédent.

`travail/`, les rapports JSON, les SBOM et le registre rempli sont des sorties
régénérables : ils sont ignorés par Git (`.gitignore`).

## Déroulé

1. Rapport brut : `trivy fs --scanners vuln --format json --output rapport-trivy.json --no-progress --quiet travail/app` et `pip-audit -r travail/app/requirements.txt --format json > rapport-pipaudit.json`, qui rend 1 quand il trouve.
2. Classement : `python3 outils/prioriser.py rapport-trivy.json` ; l'API EPSS et le catalogue KEV doivent être joignables, sinon le script s'arrête sur `Temporary failure in name resolution`.
3. Corrections : `travail/app/app.py` et `travail/app/requirements.txt`. La reconstruction de l'image exige PyPI depuis le démon Docker ; sans cet accès, la preuve d'image manque et le rapport l'écrit.
4. Registre et rapport remplis, puis `bash scripts/verifier-registre.sh`.

## Critère de réussite

`/export?fichier=%2Fetc%2Fpasswd` rend 404, `/export?fichier=notes.txt` rend 200,
`trivy fs` ne rend plus aucun constat, le registre passe le script avec zéro
écart et chaque ligne porte un propriétaire, une échéance et une preuve.
