# outils/indicateurs.py
import datetime
import re
import statistics
import sys

CHEMIN, JOUR = sys.argv[1], datetime.date.fromisoformat(sys.argv[2])
OUVERTES = ("planifiée", "atténuée", "acceptée")
constats = []
for champs in (l.split("|") for l in open(CHEMIN, encoding="utf-8") if re.match(r"\| [A-Z]", l)):
    champs = [c.strip() for c in champs]
    if len(champs) < 14 or champs[1] in ("ID", ""):
        continue
    if champs[7] not in OUVERTES:
        continue
    constats.append((champs[8], datetime.date.fromisoformat(champs[9]),
                     datetime.date.fromisoformat(champs[10])))
retard = [c for c in constats if c[2] < JOUR]
ages = [(JOUR - c[1]).days for c in constats]
part = 100 * sum(1 for c in constats if c[0]) / len(constats) if constats else 0
print(f"constats ouverts      : {len(constats)}")
print(f"hors échéance         : {len(retard)}")
print(f"âge médian (jours)    : {statistics.median(ages) if ages else 0:.1f}")
print(f"avec propriétaire (%) : {part:.0f}")
