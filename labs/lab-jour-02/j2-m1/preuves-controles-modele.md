# Preuves de contrôles — API NordMail (module J2-M1)

Modèle à recopier sous le nom `preuves-controles.md`, puis à remplir pendant le
lab. Une ligne par contrôle, dans l'ordre où il a été exécuté.

## 1. Identification

| Champ | Valeur |
| --- | --- |
| Auteur | `<vos initiales>` |
| Date | `<AAAA-MM-JJ>` |
| Empreinte du `Jenkinsfile` | `<sha256 du fichier>` |
| Versions | Trivy 0.58.1, Semgrep 1.168.0, SonarQube 9.9.8, ZAP 2.17.0 |

## 2. Contrôles

Règles de remplissage :

- **Mode et seuil** : `bloquant` ou `consultatif`, suivi du seuil chiffré.
- **Commande** : la commande exacte exécutée, entre accents graves.
- **Sortie observée** : trois lignes maximum, copiées du journal.
- **Verdict** : `SUCCES` ou `ECHEC`, avec le code retour.
- **Preuve archivée** : le fichier ou l'artefact conservé, avec son horodatage.

| # | Contrôle | Étape | Mode et seuil | Commande | Sortie observée | Verdict | Preuve archivée |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Dépendances (SCA) |  |  |  |  |  |  |
| 2 | Analyse statique (SAST) |  |  |  |  |  |  |
| 3 | Qualité (SonarQube) |  |  |  |  |  |  |
| 4 | Scan de l'image construite |  |  |  |  |  |  |
| 5 | DAST (ZAP, hors pipeline) |  |  |  |  |  |  |

## 3. Cas d'échec reproduits

Une ligne par contrôle dont l'échec a été vu. Un contrôle dont l'échec n'a
jamais été observé n'a pas été vérifié.

| Contrôle | Commande qui provoque l'échec | Message observé | Ce que j'en conclus |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

## 4. Ce que chaque outil n'a pas vu

Une ligne par outil, avec le constat réellement observé sur NordMail.

| Outil | Ce qu'il a trouvé | Ce qu'il n'a pas trouvé | Pourquoi |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

## 5. Décisions pour J2-M2

Trois réponses courtes.

1. Quel contrôle reste consultatif, et à quelle condition datée devient-il
   bloquant ?
2. Quels constats entrent au registre des vulnérabilités, avec quel
   propriétaire et quelle échéance ?
3. Quelle preuve de ce fichier sera conservée six mois, et où ?
