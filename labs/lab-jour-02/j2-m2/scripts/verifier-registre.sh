#!/usr/bin/env bash
# Contrôle de forme du registre des vulnérabilités.
# Usage : bash scripts/verifier-registre.sh [registre-vulnerabilites.md]
# Il vérifie la présence, la complétude et la cohérence des colonnes ; il ne juge
# ni la justesse d'une décision ni la véracité d'une preuve.
set -u

fichier=${1:-registre-vulnerabilites.md}
erreurs=0
signale() { printf 'ECHEC : %s\n' "$1"; erreurs=$((erreurs + 1)); }

if [[ ! -f $fichier ]]; then
  printf 'ECHEC : registre absent — %s\n' "$fichier"
  exit 1
fi

grep -q '^| ID | Composant | Sévérité |' "$fichier" || signale "en-tête du tableau absent"
if grep -q '<' "$fichier"; then
  signale "gabarit non rempli — une ou plusieurs valeurs <...> restent"
fi

rapport=$(awk -F'|' '
  function nettoie(s) { gsub(/^ +| +$/, "", s); return s }
  function date(s) { return s ~ /^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$/ }
  /^\| ID \| Composant \|/ { table = 1; next }
  table && /^## / { exit }
  table && /^\|/ && $0 !~ /^\|[-: |]+\|$/ {
    if ($2 ~ /^ *$/) next
    n++
    if (NF != 14) { printf "ECHEC : ligne %d — %d colonnes au lieu de 12\n", NR, NF - 2; e++; next }
    decision = nettoie($8); proprietaire = nettoie($9)
    detecte = nettoie($10); echeance = nettoie($11)
    autorite = nettoie($12); preuve = nettoie($13)
    if (decision !~ /^(corrigée|planifiée|atténuée|acceptée|fausse alerte)$/) {
      printf "ECHEC : ligne %d — décision inconnue « %s »\n", NR, decision; e++ }
    else connue[decision] = 1
    if (proprietaire == "") { printf "ECHEC : ligne %d — propriétaire vide\n", NR; e++ }
    if (!date(detecte)) { printf "ECHEC : ligne %d — date de détection absente ou hors format\n", NR; e++ }
    if (!date(echeance)) { printf "ECHEC : ligne %d — échéance absente ou hors format AAAA-MM-JJ\n", NR; e++ }
    if (preuve == "") { printf "ECHEC : ligne %d — preuve vide\n", NR; e++ }
    if (decision == "acceptée" || decision == "atténuée") {
      split(autorite, champ, " / ")
      qui = nettoie(champ[1]); quand = nettoie(champ[2])
      if (!date(quand)) { printf "ECHEC : ligne %d — réexamen absent pour « %s »\n", NR, decision; e++ }
      if (decision == "acceptée" && (qui == "" || qui == "sans objet")) {
        printf "ECHEC : ligne %d — acceptation sans autorité nommée\n", NR; e++ }
    }
    compte[decision]++
  }
  END {
    if (n < 8) { printf "ECHEC : %d ligne(s) de constat, huit au minimum\n", n; e++ }
    ordre[1] = "corrigée"; ordre[2] = "planifiée"; ordre[3] = "atténuée"
    ordre[4] = "acceptée"; ordre[5] = "fausse alerte"
    for (i = 1; i <= 5; i++) { d = ordre[i]
      if (d in compte) printf "OK : %d ligne(s) en décision « %s »\n", compte[d], d }
    printf "INFO : %d ligne(s) de constat analysée(s)\n", n
    exit (e > 0)
  }
' "$fichier")
code_awk=$?

printf '%s\n' "$rapport"
if (( code_awk != 0 )); then
  erreurs=$((erreurs + $(printf '%s\n' "$rapport" | grep -c '^ECHEC')))
fi

if (( erreurs > 0 )); then
  printf 'RESULTAT : %d ecart(s)\n' "$erreurs"
  exit 1
fi
printf 'RESULTAT : registre conforme\n'
