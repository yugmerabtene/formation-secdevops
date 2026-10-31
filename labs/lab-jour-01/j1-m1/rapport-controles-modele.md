# Rapport de contrôles — chaîne de livraison NordMail

Modèle à compléter pendant le lab du module J1-M1, puis à enregistrer sous le nom
`rapport-controles.md` dans ce dossier. Le module J1-M2 part de ce fichier pour
construire le pipeline Jenkins correspondant : ne renommez ni les six contrôles,
ni les colonnes des grilles.

## 1. Identification

| Champ | Valeur à saisir |
| --- | --- |
| Auteur | `<vos initiales>` |
| Date | `<AAAA-MM-JJ>` |
| Dossier audité | `labs/lab-jour-01/j1-m1/` |
| Module | J1-M1 |

## 2. Grille de placement des contrôles

Règles de remplissage :

- **État** : `présent`, `absent` ou `sans effet` — un contrôle déclaré présent
  qui n'arrête rien est `sans effet`.
- **Étape du cycle** : une seule valeur, prise dans cette liste fermée :
  `poste de développement`, `revue de code`, `build`, `registre`,
  `déploiement`, `production`.
- **Preuve observée** : la référence `fichier:ligne`, ou la commande exécutée
  avec son code retour quand le contrôle est absent, entre accents graves.
  Sans preuve, la ligne ne compte pas.
- **Mode** : `bloquant` ou `consultatif`.
- **Ce que le contrôle empêche** : une phrase à l'infinitif, avec la menace
  nommée.

| # | Contrôle | État | Étape du cycle | Preuve observée | Mode | Ce que le contrôle empêche |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Détection de secrets |  |  |  |  |  |
| 2 | Analyse des dépendances (SCA) |  |  |  |  |  |
| 3 | Analyse statique (SAST) |  |  |  |  |  |
| 4 | Scan d'image |  |  |  |  |  |
| 5 | Tests automatisés |  |  |  |  |  |
| 6 | Revue de code |  |  |  |  |  |

## 3. Défauts constatés

Une ligne par défaut, huit lignes minimum. La colonne « Contrôle associé » doit
reprendre un numéro de la grille de la partie 2.

| # | Référence `fichier:ligne` | Défaut constaté | Conséquence si rien ne change | Contrôle associé |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |
| 6 |  |  |  |  |
| 7 |  |  |  |  |
| 8 |  |  |  |  |

## 4. Cas d'échec reproduits

Deux commandes au minimum, avec leur sortie recopiée telle qu'elle apparaît.
C'est cette partie qui prouve que le défaut existe, au lieu de l'affirmer.

| Commande exécutée | Sortie observée (extrait) |
| --- | --- |
|  |  |
|  |  |

## 5. Ce que je transmets au module J1-M2

Trois réponses courtes, une à trois phrases chacune.

1. Quel contrôle dois-je implémenter en premier, et pourquoi celui-là ?
2. Quel contrôle reste consultatif dans un premier temps, et à quelle condition
   deviendra-t-il bloquant ?
3. Quelle preuve le pipeline de J1-M2 devra-t-il archiver pour que ce rapport
   reste vérifiable six mois plus tard ?
