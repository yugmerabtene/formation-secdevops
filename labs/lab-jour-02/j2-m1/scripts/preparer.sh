#!/usr/bin/env bash
# Prépare la pile du lab J2-M1 : application, SonarQube, Jenkins, démon Docker.
# Usage : bash scripts/preparer.sh
# Le jeton SonarQube est une valeur de démonstration, créée à l'exécution et
# stockée dans un credential Jenkins. Aucun jeton n'est écrit dans un fichier.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "1. Construction et démarrage de la pile"
docker compose up -d --build

echo "2. Attente de SonarQube sur http://localhost:9000 (une à deux minutes)"
debut=$(date +%s)
for _ in $(seq 1 90); do
    if curl -fsS -m 3 http://localhost:9000/api/system/status 2>/dev/null | grep -q '"status":"UP"'; then
        echo "   SonarQube répond après $(( $(date +%s) - debut )) s"
        break
    fi
    sleep 2
done
curl -fsS -m 3 http://localhost:9000/api/system/status | grep -q '"status":"UP"'

echo "3. Création du jeton d'analyse (compte admin de démonstration)"
JETON=$(curl -sS -u admin:admin -X POST \
    "http://localhost:9000/api/user_tokens/generate" \
    --data-urlencode "name=jenkins-lab-$(date +%s)" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")
test -n "$JETON"

echo "4. Base de vulnérabilités Trivy dans le conteneur Jenkins"
docker compose exec -T jenkins trivy fs --download-db-only --no-progress

echo "5. Attente de Jenkins sur http://localhost:8089"
for _ in $(seq 1 90); do
    if curl -fsS -m 3 http://localhost:8089/api/json >/dev/null 2>&1; then
        echo "   Jenkins répond"
        break
    fi
    sleep 2
done
curl -fsS -m 3 http://localhost:8089/api/json >/dev/null

echo "5. Enregistrement du jeton dans le credential Jenkins jeton-sonar"
COOKIE=$(mktemp)
CRUMB=$(curl -s -c "$COOKIE" http://localhost:8089/crumbIssuer/api/json \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['crumbRequestField']+': '+d['crumb'])")
curl -s -b "$COOKIE" -H "$CRUMB" -o /dev/null \
    -w '   création du credential : HTTP %{http_code}\n' \
    -X POST 'http://localhost:8089/credentials/store/system/domain/_/createCredentials' \
    --data-urlencode "json={\"\": \"0\", \"credentials\": {\"scope\": \"GLOBAL\", \"id\": \"jeton-sonar\", \"secret\": \"$JETON\", \"description\": \"Jeton SonarQube du lab J2-M1\", \"\$class\": \"org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl\"}}"
unset JETON
rm -f "$COOKIE"

echo "6. État des services"
docker compose ps
