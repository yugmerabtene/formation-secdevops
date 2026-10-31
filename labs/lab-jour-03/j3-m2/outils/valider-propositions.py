# outils/valider-propositions.py
import json
import sys

CHAMPS = ("route", "entree", "attendu", "preuve")
propositions = json.load(open(sys.argv[1], encoding="utf-8"))
refusees = 0
for numero, proposition in enumerate(propositions, 1):
    manquants = [c for c in CHAMPS if not str(proposition.get(c, "")).strip()]
    if manquants:
        print(f"REFUS {numero} : champ(s) manquant(s) {', '.join(manquants)} — {proposition.get('route', '?')}")
        refusees += 1
    elif not any(mot in proposition["preuve"] for mot in ("curl", "trivy", "semgrep", "zap")):
        print(f"REFUS {numero} : preuve sans commande rejouable — {proposition['route']}")
        refusees += 1
    else:
        print(f"ACCEPTE {numero} : {proposition['route']} — {proposition['entree']}")
print(f"{len(propositions) - refusees} acceptée(s), {refusees} refusée(s)")
sys.exit(1 if refusees else 0)
