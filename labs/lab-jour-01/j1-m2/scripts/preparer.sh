#!/usr/bin/env bash
# Prépare la pile du lab J1-M2 : Jenkins, démon Docker dédié, credential.
# Usage : bash scripts/preparer.sh
set -euo pipefail

cd "$(dirname "$0")/.."

echo "1. Construction et démarrage de la pile"
docker compose up -d --build

echo "2. Attente de Jenkins sur http://localhost:8088"
for _ in $(seq 1 90); do
    if curl -fsS http://localhost:8088/api/json >/dev/null 2>&1; then
        echo "   Jenkins répond"
        break
    fi
    sleep 2
done
curl -fsS http://localhost:8088/api/json >/dev/null

echo "3. Création du credential de démonstration jeton-registre"
COOKIE=$(mktemp)
CRUMB=$(curl -s -c "$COOKIE" http://localhost:8088/crumbIssuer/api/json \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['crumbRequestField']+': '+d['crumb'])")
curl -s -b "$COOKIE" -H "$CRUMB" -o /dev/null \
    -w '   création du credential : HTTP %{http_code}\n' \
    -X POST 'http://localhost:8088/credentials/store/system/domain/_/createCredentials' \
    --data-urlencode 'json={"": "0", "credentials": {"scope": "GLOBAL", "id": "jeton-registre", "secret": "token-registre-exemple", "description": "Jeton du registre local, valeur de demonstration", "$class": "org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl"}}'
rm -f "$COOKIE"

echo "4. État des services"
docker compose ps
