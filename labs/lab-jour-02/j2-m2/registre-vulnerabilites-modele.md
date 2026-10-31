# Registre des vulnérabilités — NordMail

Registre du 2026-10-31, application NordMail v2, image `j2m1-app:1`.
Une ligne par constat, y compris les constats écartés : un constat qui n'est pas
dans le registre n'a pas de propriétaire, donc pas de fin.

| ID | Composant | Sévérité | CVSS | EPSS | KEV | Décision | Propriétaire | Détecté le | Échéance | Autorité / réexamen | Preuve |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<CVE ou règle>` | `<paquet ou fichier:ligne>` | `<CRITICAL/HIGH/MEDIUM/LOW>` | `<x.y ou non calculé>` | `<0.00000>` | `<oui/non>` | `<décision>` | `<initiale>` | `<AAAA-MM-JJ>` | `<AAAA-MM-JJ>` | `<autorité / AAAA-MM-JJ ou sans objet>` | `<commande et sortie>` |
|  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |

## Décisions admises

| Décision | Sens | Ce qu'elle exige |
| --- | --- | --- |
| `corrigée` | Le constat ne se reproduit plus. | Une preuve avant/après, pas une déclaration. |
| `planifiée` | Correction datée, propriétaire nommé. | Une échéance dans le délai de la sévérité. |
| `atténuée` | Le correctif manque, un contrôle réduit l'exposition. | Le contrôle nommé et une date de réexamen. |
| `acceptée` | Le risque est assumé par une autorité nommée. | Justification écrite, autorité, date de réexamen. |
| `fausse alerte` | La preuve contredit l'alerte. | La requête ou la ligne de code qui le démontre. |

## Délais de correction

| Sévérité | Délai | Présence au catalogue KEV |
| --- | --- | --- |
| CRITICAL | 7 jours | 7 jours, quelle que soit la sévérité |
| HIGH | 30 jours | idem |
| MEDIUM | 90 jours | idem |
| LOW | 180 jours | idem |

Une ligne `acceptée` sans autorité nommée, ou `atténuée` sans date de réexamen,
est une vulnérabilité oubliée écrite dans un tableau. La date de détection sert
à calculer l'âge médian des constats ouverts : sans elle, aucune ancienneté ne
se mesure.
