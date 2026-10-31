#!/usr/bin/env bash
# Vérifie le livrable preuves-controles.md sans juger la qualité des preuves.
# Usage : bash scripts/verifier-preuves.sh [chemin]
set -uo pipefail

FICHIER="${1:-preuves-controles.md}"
ERREURS=0

if [ ! -f "$FICHIER" ]; then
    echo "ECHEC : fichier absent — $FICHIER"
    exit 1
fi

lignes_controles=$(grep -cE '^\| [1-6] \|' "$FICHIER" || true)
lignes_echecs=$(grep -cE '^\| (Détection|Dépendances|Analyse|Tests|Durcissement|Scan)' "$FICHIER" || true)

verifier() {
    if [ "$1" -lt "$2" ]; then
        echo "ECHEC : $3 ($1, attendu $2)"
        ERREURS=$((ERREURS + 1))
    else
        echo "OK : $3 ($1)"
    fi
}

verifier "$lignes_controles" 6 "six lignes de contrôle"
verifier "$lignes_echecs" 6 "six cas d'échec"

for motif in '<vos initiales>' '<AAAA-MM-JJ>' '<sha256 du fichier>'; do
    if grep -qF "$motif" "$FICHIER"; then
        echo "ECHEC : gabarit non rempli — $motif"
        ERREURS=$((ERREURS + 1))
    fi
done

if ! grep -qE 'SUCCES|ECHEC' "$FICHIER"; then
    echo "ECHEC : aucun verdict SUCCES ou ECHEC"
    ERREURS=$((ERREURS + 1))
fi

if [ "$ERREURS" -eq 0 ]; then
    echo "RESULTAT : livrable complet"
    exit 0
fi
echo "RESULTAT : $ERREURS écart(s)"
exit 1
