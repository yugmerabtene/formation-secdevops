# outils/prioriser-registre.sh
echo "id;composant;severite;echeance;proprietaire;decision"
awk -F'|' '
  function rang(s) { return s == "CRITICAL" ? 1 : s == "HIGH" ? 2 : s == "MEDIUM" ? 3 : s == "LOW" ? 4 : 5 }
  /^\| ID \| Composant \|/ { table = 1; next }
  table && /^## / { exit }
  table && /^\|/ && $0 !~ /^\|[-: |]+\|$/ {
    for (i = 2; i <= 13; i++) gsub(/^ +| +$/, "", $i)
    if ($8 == "corrigée" || $8 == "fausse alerte") next
    printf "%d;%s;%s;%s;%s;%s;%s;%s\n", rang($4), $11, $2, $3, $4, $11, $9, $8
  }' "$1" | sort -t';' -k1,1n -k2,2 | cut -d';' -f3-
