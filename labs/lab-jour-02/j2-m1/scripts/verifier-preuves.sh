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

# Lignes de données d'une section : entre "## <n>." et la section suivante,
# on garde les lignes de tableau qui ne sont ni l'en-tête ni le séparateur.
lignes_section() {
    awk -v section="## $1." '
        index($0, section) == 1 { dedans = 1; next }
        dedans && /^## / { dedans = 0 }
        dedans && /^\| / && $0 !~ /^\| # / && $0 !~ /^\| --- / && $0 !~ /^\| Champ / \
            && $0 !~ /^\| Contrôle / && $0 !~ /^\| Outil / && $0 !~ /^\| ---/ { n++ }
        END { print n + 0 }
    ' "$FICHIER"
}

verifier() {
    if [ "$1" -lt "$2" ]; then
        echo "ECHEC : $3 ($1, attendu $2)"
        ERREURS=$((ERREURS + 1))
    else
        echo "OK : $3 ($1)"
    fi
}

verifier "$(lignes_section 2)" 5 "cinq lignes de contrôle"
verifier "$(lignes_section 3)" 3 "trois cas d'échec"
verifier "$(lignes_section 4)" 3 "trois lignes « ce qu'il n'a pas vu »"

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
