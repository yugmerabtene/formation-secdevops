# Preuves de contrôles — API NordMail (module J1-M2)

Modèle à recopier sous le nom `preuves-controles.md`, puis à remplir pendant le
lab. Une ligne par contrôle, dans l'ordre d'exécution du pipeline.

## 1. Identification

| Champ | Valeur |
| --- | --- |
| Auteur | `<vos initiales>` |
| Date | `<AAAA-MM-JJ>` |
| Commit ou empreinte du `Jenkinsfile` | `<sha256 du fichier>` |
| Version de Jenkins | `2.580.2` |

## 2. Contrôles

Règles de remplissage :

- **Mode et seuil** : `bloquant` ou `consultatif`, suivi du seuil chiffré.
- **Commande** : la commande exacte exécutée, entre accents graves.
- **Sortie observée** : trois lignes maximum, copiées du journal.
- **Verdict** : `SUCCES` ou `ECHEC`, avec le code retour.
- **Preuve archivée** : le fichier ou l'artefact conservé, avec son horodatage.

| # | Contrôle | Étape | Mode et seuil | Commande | Sortie observée | Verdict | Preuve archivée |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Détection de secrets |  |  |  |  |  |  |
| 2 | Dépendances (SCA) |  |  |  |  |  |  |
| 3 | Analyse statique |  |  |  |  |  |  |
| 4 | Tests automatisés |  |  |  |  |  |  |
| 5 | Durcissement du `Dockerfile` |  |  |  |  |  |  |
| 6 | Scan de l'image construite |  |  |  |  |  |  |

## 3. Cas d'échec reproduits

Une ligne par contrôle, avec la commande qui provoque l'échec et le message
observé. Un contrôle dont l'échec n'a jamais été vu n'a pas été vérifié.

| Contrôle | Commande qui provoque l'échec | Message observé | Ce que j'en conclus |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

## 4. Décisions et dérogations

| Contrôle | Décision | Propriétaire | Motif | Date d'expiration |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 5. Transmission au module J1-M3

Trois réponses courtes.

1. Quels journaux et métriques le pipeline doit-il produire pour que la
   surveillance en production puisse distinguer une panne d'une attaque ?
2. Quel contrôle reste consultatif, et à quelle condition datée devient-il
   bloquant ?
3. Quelle preuve de ce fichier sera conservée six mois, et où ?
