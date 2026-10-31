#!/usr/bin/env bash
# Exécute un script de pipeline seulement si son empreinte est celle qui a été
# relue et versionnée. Toute modification du script, même d'une ligne, change
# l'empreinte et bloque l'exécution.
set -u

attendue=$(cut -d' ' -f1 empreinte-attendue.txt)
obtenue=$(sha256sum monter-script.sh | cut -d' ' -f1)
if [ "$attendue" != "$obtenue" ]; then
  echo "empreinte différente — script non exécuté"
  exit 1
fi
bash monter-script.sh
