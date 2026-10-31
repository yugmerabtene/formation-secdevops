# Journal de triage — NordMail J1-M3

## Identification
| Champ | Valeur |
| --- | --- |
| Date | `<AAAA-MM-JJ>` |
| Auteur | `<initiales>` |
| Pile | `j1-m3-lab` |
| Cibles Prometheus actives | `<nombre>` |

## Signaux triés
Remplir une ligne par signal observé (erreurs 5xx, refus 401/403, balayage 404).

| # | Horodatage UTC | Alerte | Seuil et fenêtre | Valeur observée | Hypothèse | Vérification effectuée | Verdict | Action immédiate | Suite donnée |
|---|----------------|--------|------------------|-----------------|-----------|------------------------|---------|------------------|--------------|
| 1 | | DemoAppHighErrorRate | >5% 5xx / 1 min (for 1m) | | Panne applicative simulée | Journaux app, `docker compose logs` | | | |
| 2 | | DemoAppAuthFailureSpike | >0,2 refus/s / 1 min | | Bourrage identifiants ou formulaire cassé | Adresses sources, comptes visés, corrélation livraison | | | |
| 3 | | DemoAppNotFoundScan | >0,5 404/s / 1 min (for 30s) | | Balayage de chemins sensibles | Chemins demandés (métriques normalisées → `other`), journaux d'accès | | | |

## Cas d'échec de notification
| Étape | Constat | Cause identifiée | Correction appliquée | Preuve (sujet + heure message) |
|-------|---------|------------------|----------------------|--------------------------------|
| 2 | Alerte `firing` mais 0 message dans MailHog | Routage critique → `equipe-nuit` (127.0.0.1:9999 injoignable) | Remplacer par `mailhog-demo` dans `alertmanager.yml` | `[FIRING] DemoAppHighErrorRate` à HH:MM:SS UTC |
| 2 (suite) | Renvoi attendu au cycle `group_interval` suivant | | Recharger Alertmanager (`/-/reload`) | Deuxième message reçu à HH:MM:SS UTC |

## Décisions pour la suite
Répondre en reprenant la section 5 de `preuves-controles.md` (J1-M2).

1. **Journaux et métriques à produire** pour distinguer panne / attaque :
   `<réponse>`

2. **Contrôle resté consultatif** avec sa condition datée de passage en bloquant :
   `<réponse>`

3. **Preuve conservée six mois** et son emplacement :
   `<réponse>`