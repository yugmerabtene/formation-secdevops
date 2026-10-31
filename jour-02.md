# Formation SecDevOps — JOUR 2 — Outils et automatisation des tests de sécurité

## Module J2-M1 — Automatisation des tests de sécurité

### Préambule

Sur NordMail, application Flask de notes du lab [J1-M2](jour-01.md#lab--durcir-le-pipeline-de-lapi-nordmail), Semgrep, analyseur statique à règles, applique quatre règles et ne signale rien sur la route `/export`. Le scan actif de ZAP (Zed Attack Proxy) y relève pourtant une traversée de chemin. Un outil ne voit que ce que ses règles ou ses requêtes décrivent.

Un pipeline de sécurité combine six familles d’analyse, et chacune a un angle mort. Il ne peut donc pas tout détecter : il doit savoir ce que chaque outil ne voit pas, et décider quoi faire quand un outil signale un constat (un résultat d’analyse à qualifier).

La CVE-2021-44228 (Log4Shell) est révélée publiquement le 9 décembre 2021. Le lendemain, la NVD (National Vulnerability Database) la publie avec un score CVSS (Common Vulnerability Scoring System) 3.1 de 10,0. Une organisation qui tenait un inventaire de ses dépendances a pu mesurer son exposition le jour même ; les autres ont dû repérer la bibliothèque vulnérable dans chaque image et chaque serveur.

### Le vocabulaire en clair

| Terme | En clair | Où on le rencontre |
| --- | --- | --- |
| SCA (Software Composition Analysis) | Analyse des dépendances déclarées, comparées aux vulnérabilités publiées. | Étape `Dependances`, `requirements.txt`. |
| SAST (Static Application Security Testing) | Analyse du code source sans l’exécuter, sur des motifs décrits par des règles. | Étape `Analyse statique`, Semgrep. |
| DAST (Dynamic Application Security Testing) | Analyse d’une application en fonctionnement, par des requêtes HTTP (HyperText Transfer Protocol). | ZAP, hors pipeline. |
| Scan d’image | Analyse des paquets contenus dans l’image construite. | Étape `Scan image`. |
| Scan de configuration | Analyse d’un `Dockerfile` ou d’un fichier Compose contre des règles de bonne pratique. | `trivy config`. |
| Détection de secrets | Recherche de formats de clés connus dans les fichiers. | gitleaks. |
| Faux positif | Alerte qui ne correspond à aucune faille exploitable. | Rapport ZAP, alerte `Buffer Overflow`. |
| Seuil | Valeur chiffrée qui transforme un constat en échec du build. | `--severity`, `--exit-code`, condition de la gate. |
| Quality gate | Ensemble de conditions sur le code nouveau, évalué après analyse. | SonarQube, étape `Qualite`. |
| Base de vulnérabilités | Liste datée des CVE (Common Vulnerabilities and Exposures) connues, téléchargée avant le scan. | `trivy --version`. |

### Objectifs du module

À l’issue de ce module, vous serez capable de :

1. **Distinguer** les six familles d’analyse par ce qu’elles lisent et par leur angle mort.
2. **Exécuter** Trivy, scanner de vulnérabilités et de configuration, sur trois cibles et lire un code retour, un seuil et une date de base.
3. **Opposer** scan passif et scan actif, puis **décider** où placer un DAST.
4. **Interpréter** une quality gate SonarQube et nommer ce qu’elle ne prouve pas.
5. **Intégrer** trois outils dans le pipeline Jenkins de NordMail, avec un seuil bloquant, un seuil consultatif et des preuves archivées.

**Public et prérequis.** Ce module s’adresse aux développeurs, aux ingénieurs DevOps et SRE (Site Reliability Engineering), aux ingénieurs QA (Quality Assurance), aux ingénieurs sécurité et aux chefs de projet techniques. Le niveau attendu est intermédiaire, avec des bases de Git, de la ligne de commande, de Docker Compose et d’un pipeline déclaratif Jenkins.

### Contenu du module

#### 1. Six familles d’analyse, six angles morts

| Famille | Ce qu’elle lit | Ce qu’elle ne trouve jamais | Durée mesurée sur NordMail |
| --- | --- | --- | --- |
| SCA | `requirements.txt` | une faille dans votre propre code | 2 s à froid, 0,1 s avec cache |
| SAST | le source Python | un motif qu’aucune règle ne décrit | 2 s |
| Détection de secrets | les fichiers | une clé maison sans format connu | 0,4 s |
| Scan d’image | les couches de l’image | un défaut logique de l’application | 4 s à froid |
| Scan de configuration | `Dockerfile`, Compose | un secret écrit dans le code | 2 s |
| DAST | le trafic HTTP | tout ce qui n’est pas atteignable par l’interface | 33 s à 2 min 38 |

Un code retour 0 ne démontre pas l’absence de défaut : il indique seulement que l’outil n’a trouvé aucun défaut dans le périmètre couvert par ses règles. Semgrep applique ici quatre règles, écrites pour l’application NordMail, et produit quatre constats. Aucun ne porte sur la route `/export`, qui ouvre un fichier dont le nom vient de l’URL (Uniform Resource Locator) : cette faille n’est pas couverte par les règles. Le SAST ne voit donc que ce que ses règles décrivent. Avec ses règles par défaut, gitleaks 8.28.0 rend `no leaks found` sur `app/`, alors que ce dossier contient `app.secret_key` en clair : la détection de secrets ne reconnaît que des formats connus.

#### 2. Trivy : trois cibles, une base datée

`trivy fs` lit un répertoire sans rien installer. `trivy image` lit les couches d’une image construite. `trivy config` applique des règles de configuration. Le moteur est le même, mais les trois périmètres donnent trois résultats différents.

| Commande | Sortie mesurée le 2026-10-31 | Code |
| --- | --- | --- |
| `trivy fs --scanners vuln --severity HIGH,CRITICAL --no-progress app` | `Total: 1 (HIGH: 1, CRITICAL: 0)` | 0 |
| même commande avec `--exit-code 1` | même rapport | 1 |
| `trivy fs --scanners vuln --severity CRITICAL --exit-code 1 --no-progress app` | aucune vulnérabilité : `0` dans le tableau de synthèse | 0 |
| `trivy image --severity HIGH --quiet j2m1-app:1` | `Total: 44 (HIGH: 44)` pour debian 13.7, `Total: 1 (HIGH: 1)` pour Python | 0 |
| `trivy config app/Dockerfile` | `Tests: 27 (SUCCESSES: 26, FAILURES: 1)`, contrôle Trivy `DS-0026 (LOW)` : HEALTHCHECK absent | 0 |

`--severity` filtre le rapport. `--exit-code` fixe le code retour du build : sans `--exit-code`, Trivy rend 0 quelle que soit la gravité trouvée. La commande bloquante du lab porte les deux options. Une étape sans `--exit-code` ne produit qu’un rapport, sans effet sur la livraison : c’est le premier défaut à repérer dans un pipeline inconnu.

Le format de sortie se choisit. `trivy fs --format sarif --output rapports/dependances.sarif app` produit un SARIF (Static Analysis Results Interchange Format) 2.1.0 de 17 résultats, un format lisible par les outils de revue de code. `--format json` produit un fichier d’archive, et `--format cyclonedx` produit le SBOM (Software Bill of Materials), l’inventaire des composants, repris en [J2-M2](#module-j2-m2--gestion-des-vulnérabilités-et-remédiations).

La base de vulnérabilités porte une date : `UpdatedAt` vaut 2026-10-30 et `NextUpdate` vaut 2026-10-31, soit une fenêtre de vingt-quatre heures. Un scanner qui ne retélécharge pas sa base compare donc les dépendances à une liste figée : une CVE publiée la veille passe inaperçue.

La porte dérobée de xz-utils, publiée le 29 mars 2024 sous la CVE-2024-3094, ne figurait dans aucune base avant sa révélation par un développeur. Un SCA apporte l’inventaire des versions présentes, mais il ne connaît pas une attaque inédite.

#### 3. DAST : le passif observe, l’actif attaque

Le scan passif explore l’application et lit ce que le serveur renvoie. Le scan actif envoie des requêtes d’attaque, appelées charges (payloads), et observe la réponse. Les deux modes sont mesurés ici sur la même cible, le même jour, avec la même image.

| Mode | Ce qu’il envoie | Durée mesurée | Résultat |
| --- | --- | --- | --- |
| `zap-baseline.py` | exploration et règles passives | 33 s | `WARN-NEW: 4`, `PASS: 58`, code 2 |
| `zap-full-scan.py -m 1 -T 5` | exploration et charges actives | 2 min 38 | `WARN-NEW: 11`, `PASS: 103`, code 2 |

Le mode actif trouve ce que le mode passif ne voit pas. Sur `/export?fichier=%2Fetc%2Fpasswd`, il relève `Path Traversal [6]`, avec un code 200 (succès) qui contient `root:x:0:0`. Sur `/ping`, il relève `Remote OS Command Injection [90020]` et sa variante temporelle `[90037]`. Sur `/recherche`, il relève `Cross Site Scripting (Reflected) [40012]` et `Server Side Template Injection [90035]`.

Un scan actif attaque réellement la cible : il ne se lance que sur un système dont vous détenez l’autorisation écrite. Sur un environnement partagé, il modifie l’état. Par exemple, `POST /admin/purge` vide les notes de NordMail, et rien n’empêche le scanner d’appeler cette route.

Un faux positif se reconnaît à sa preuve. L’alerte `Buffer Overflow [30001]` sur `/export?fichier=notes.txt` est annoncée à risque moyen et à confiance moyenne, mais la preuve observée se limite à `Connection: close`. Une alerte sans requête reproductible reste une piste, pas un constat.

La durée du scan fixe donc sa place : 2 min 38 pour neuf routes locales, et plusieurs heures pour une application authentifiée avec des parcours métier. Le DAST s’exécute la nuit, sur un déploiement de préproduction, jamais à chaque fusion.

Une application authentifiée exige un contexte : `zap-baseline.py -n nordmail.context -U demo` charge le formulaire déclaré, sans quoi le scanner ne voit que les pages publiques. Les options sont vérifiées par `-h`, mais l’exécution n’est pas vérifiée dans cet environnement, faute de formulaire dans la pile.

#### 4. SonarQube : la quality gate mesure le code nouveau

SonarQube applique trois familles de règles : bogues, dette technique et points chauds (security hotspots). Une quality gate (porte de qualité) évalue le code nouveau, c’est-à-dire le code modifié depuis la version de référence. La gate compare donc la version courante à la précédente, et non le projet à un idéal.

Sur NordMail, SonarQube compte 73 lignes de code, hors lignes vides et commentaires : c’est la métrique NCLOC (Non-Comment Lines of Code). La gate rend `status OK`, mais le champ des conditions ignorées vaut `true` : les conditions sur le code nouveau n’ont pas été évaluées. `new_coverage` vaut 0,0 pour un seuil de 80, `vulnerabilities` vaut 0 et `security_hotspots` vaut 2, pour une couverture globale de `0.0`. La première analyse ne contient aucun code nouveau, donc la gate passe sans rien mesurer.

Une valeur `vulnerabilities` à 0 ne prouve pas que le code est sain. Les deux points chauds sont la création d’une application Flask sans protection CSRF (Cross-Site Request Forgery), règle `python:S4502`, ligne 23 de `app/app.py`, en HIGH, et un appel à `hashlib.md5`, règle `python:S4790`, ligne 99, en LOW. Les quatre défauts relevés par Semgrep et les injections relevées par ZAP n’y figurent pas. Un point chaud demande une décision consignée, pas une correction faite à l’aveugle.

#### 5. Jenkins : ordre, seuils, panne

Le contrôle le moins coûteux et le plus bloquant passe en premier. Le build mesuré s’arrête à l’étape `Dependances`, au bout de 2 863 ms, et ignore les quatre étapes suivantes. Le motif remonte ainsi en trois secondes, au lieu de trente et une.

Une famille d’analyse ne porte qu’un seul contrôle bloquant. Deux contrôles bloquants sur la même famille arrêtent la livraison deux fois pour le même motif. Un faux positif sur l’un des deux suffit alors à tout bloquer.

Un rapport consultatif qui n’est pas archivé n’existe pas pour l’audit. La section `post` du `Jenkinsfile` archive `rapports/**` et le rend consultable après le build. Le build vert mesuré dure 31 001 ms et archive trois fichiers.

Une panne d’outil n’est pas une vulnérabilité. Sans réseau, Trivy rend `FATAL Fatal error init error: DB error: failed to download vulnerability DB` et un code non nul, sans aucun constat. Un `|| true` sur l’étape bloquante transforme cette panne en silence. Le journal du build doit donc distinguer un « scan en échec » d’un « scan qui a trouvé ».

### Les techniques, pas à pas

#### Technique 1 — Lancer les trois familles sur la même application

Les trois commandes qui suivent s’exécutent depuis `labs/lab-jour-02/j2-m1/`, avec trois périmètres et trois codes retour. Elles lisent des fichiers : l’image `j2m1-app:1` n’est pas nécessaire ici. La commande Semgrep porte `--severity ERROR` : les deux règles WARNING du jeu de règles, injection de gabarit et empreinte MD5, sont donc écartées, d’où deux constats au lieu de quatre.

```bash
trivy fs --scanners vuln --severity HIGH,CRITICAL --exit-code 1 --no-progress --quiet app; echo "code=$?"
```

```text
[… tableau de synthèse omis …]
requirements.txt (pip)
======================
Total: 1 (HIGH: 1, CRITICAL: 0)
[… table des vulnérabilités omise …]
code=1
```

```bash
semgrep --config outils/semgrep-nordmail.yml --severity ERROR --error --quiet app; echo "code=$?"
```

```text
2 Code Findings
app/app.py
❯❯❱ outils.nordmail-shell-concatene
   ❰❰ Blocking ❱❱
   subprocess avec shell=True et une commande construite : injection de commande.
   86┆ sortie = subprocess.run("ping -c 1 " + hote, shell=True, capture_output=True, text=True)  # défaut 4
❯❯❱ outils.nordmail-flask-debogage
   ❰❰ Blocking ❱❱
   Serveur Flask démarré avec debug=True : la console de débogage expose le code.
   103┆ app.run(host="0.0.0.0", port=5000, debug=True)
code=1
```

```bash
docker run --rm -v "$PWD/app:/src:ro" ghcr.io/gitleaks/gitleaks:v8.28.0 detect --source /src --no-git; echo "code=$?"
```

```text
[… préfixe horaire retiré …]
INF scanned ~3623 bytes (3.62 KB) in 43ms
INF no leaks found
code=0
```

Ces sorties prouvent deux choses : le SCA et le SAST échouent bien avec `--exit-code` et `--error`, et la détection de secrets ne voit rien. Elles ne prouvent pas que la clé de session est sûre, ni que `/export` est inoffensif, car aucune des trois commandes ne lit le comportement de la route.

#### Technique 2 — Dater une exception de vulnérabilité

Une vulnérabilité dont le correctif ne peut pas être déployé dans le délai ne se supprime pas. Elle devient une exception datée, versionnée et relue. Le fichier d’exceptions porte l’identifiant, le chemin, la justification et la date de fin. Créez donc `outils/trivyignore.yaml` :

```yaml
# outils/trivyignore.yaml
vulnerabilities:
  - id: CVE-2024-34069
    paths:
      - requirements.txt
    statement: "Déploiement du correctif 3.0.3 impossible sous 48 h ; correction planifiée en J2-M2."
    expired_at: 2026-11-30
```

```bash
trivy fs --scanners vuln --severity HIGH,CRITICAL --exit-code 1 --ignorefile outils/trivyignore.yaml --no-progress --quiet app; echo "code=$?"
```

```text
│ requirements.txt │ pip  │        0        │
[…]
code=0
```

Remplacez `expired_at` par `2026-10-01` et relancez la commande. Le constat revient sans qu’aucune autre ligne ne change, avec `Total: 1 (HIGH: 1, CRITICAL: 0)` et `code=1`. L’exception ne vaut que jusqu’à sa date : passé ce terme, le build redevient rouge sans intervention.

#### Technique 3 — Lire une quality gate et ses conditions ignorées

L’API (Application Programming Interface) de SonarQube rend le statut et le motif, deux informations qu’un écran vert ne montre pas. Le compte `admin:admin` est celui de l’image de démonstration : il doit être changé avant tout usage hors du lab.

```bash
curl -s -u admin:admin "http://127.0.0.1:9000/api/qualitygates/project_status?projectKey=nordmail-api" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)['projectStatus']
print('statut', d['status'], '| conditions ignorees', d['ignoredConditions'])
for c in d['conditions']:
    if c['metricKey'] == 'new_coverage':
        print(c['metricKey'], 'valeur', c['actualValue'], 'seuil', c['errorThreshold'], c['status'])
"
```

```text
statut OK | conditions ignorees True
new_coverage valeur 0.0 seuil 80 OK
```

Une condition au statut `OK`, avec une valeur de 0,0 sous un seuil de 80, n’est pas une erreur de calcul. Le champ des conditions ignorées vaut `true`, donc la condition n’a pas été évaluée, faute de code nouveau. La gate ne dit rien de la couverture du projet, qui reste à `0.0`.

#### Technique 4 — Confronter le scan passif et le scan actif

Les deux scans utilisent le même conteneur et la même cible, mais deux scripts différents. Le premier n’envoie pas de charge, le second en envoie : la comparaison des deux rapports montre ce que le mode actif ajoute.

```bash
docker run --rm --network host -v "$PWD/rapports:/zap/wrk:rw" zaproxy/zap-stable \
  zap-baseline.py -t http://127.0.0.1:8099 -J zap-baseline.json; echo "code=$?"
```

```text
FAIL-NEW: 0 FAIL-INPROG: 0 WARN-NEW: 4 WARN-INPROG: 0 INFO: 0 IGNORE: 0 PASS: 58
code=2
```

```bash
docker run --rm --network host -v "$PWD/rapports:/zap/wrk:rw" zaproxy/zap-stable \
  zap-full-scan.py -t http://127.0.0.1:8099 -m 1 -T 5 -J zap-full.json; echo "code=$?"
```

```text
FAIL-NEW: 0 FAIL-INPROG: 0 WARN-NEW: 11 WARN-INPROG: 0 INFO: 0 IGNORE: 0 PASS: 103
code=2
```

L’ordre d’affichage de la console n’est pas garanti. Le fichier JSON (JavaScript Object Notation) fait foi, pas l’affichage.

Les codes 1, 2 et 3 signalent, dans l’ordre, un échec au niveau configuré, la présence d’avertissements et une erreur d’exécution du script, par exemple une cible injoignable. Un pipeline qui teste `if [ $? -ne 0 ]` bloque donc aussi sur un simple en-tête manquant. La comparaison montre que le mode actif atteint les routes qui acceptent des paramètres. Elle ne montre pas que ces routes sont les seules.

### Lab — Intégrer trois outils dans le pipeline de NordMail

Le `Jenkinsfile` de NordMail place déjà quatre étapes de sécurité et six contrôles. Votre travail consiste à le faire tourner, à expliquer son premier échec, à lever cet échec par une exception datée, à exécuter le DAST hors du pipeline et à produire les preuves qui rendent chaque contrôle vérifiable.

#### Prérequis

- avoir exécuté les techniques 1 et 2 ; faire la technique 3 après l’étape 4 du lab, et la technique 4 après l’étape 1 ;
- pile [`labs/lab-jour-01/j1-m2/`](jour-01.md#module-j1-m2--contrôles-de-sécurité-dans-les-pipelines-devops) construite (image `j1m2-jenkins:2.580.2`) ; `trivy` 0.71.2 et `semgrep` 1.168.0 installés sur l’hôte ; Docker sur l’hôte ; 2 Go de mémoire disponibles pour SonarQube, en plus de Jenkins ;
- accès réseau pour tirer `sonarqube:9.9.8-community`, `docker:29.1.3-dind` et `zaproxy/zap-stable`, puis la base Trivy ;
- ports `8099`, `8089` et `9000` libres sur la machine.

#### Environnement

| Élément | Valeur |
| --- | --- |
| Hôte | Ubuntu 26.04, Docker local, sans orchestration |
| Docker Engine | 29.1.3 |
| Docker Compose | 2.40.3 |
| Dossier du lab | `labs/lab-jour-02/j2-m1/` |
| Application | `127.0.0.1:8099`, image `j2m1-app:1` ; le pipeline construit `nordmail-api:<numéro de build>` |
| SonarQube | `127.0.0.1:9000`, image `sonarqube:9.9.8-community` |
| Jenkins | `127.0.0.1:8089`, image `j2m1-jenkins:2.580.2` |
| Trivy | 0.58.1 dans Jenkins, 0.71.2 sur l’hôte |
| Semgrep | 1.168.0 |
| ZAP | `zaproxy/zap-stable`, version 2.17.0, hors Compose |
| Rapports | `rapports/`, archivés par le pipeline |
| Modèle de preuves | [`preuves-controles-modele.md`](labs/lab-jour-02/j2-m1/preuves-controles-modele.md) |

#### Étapes du lab

**Étape 1 — Démarrer la pile.** Le script construit l’image, attend SonarQube, crée un jeton de démonstration dans un credential Jenkins et télécharge la base Trivy. Comptez une à deux minutes pour SonarQube.

```bash
cd labs/lab-jour-02/j2-m1
bash scripts/preparer.sh
```

```text
   création du credential : HTTP 200
[…]
```

```bash
curl -s http://localhost:9000/api/system/status
```

```text
{"id":"147B411E-AaGPM1378TN08P4WXFuB","version":"9.9.8.100196","status":"UP"}
```

**Cas d’échec à constater.** Si l’étape 4 du script n’atteint pas le registre de conteneurs qui héberge la base, elle rend `FATAL Fatal error init error: DB error: failed to download vulnerability DB` et s’arrête avant l’étape 5 : la pile tourne, mais la base est absente.

**Étape 2 — Déclencher le pipeline.** Le script `jenkins-lab.py` valide le `Jenkinsfile` avant de lancer le build : un pipeline invalide ne produit qu’un message.

```bash
python3 scripts/jenkins-lab.py valider
python3 scripts/jenkins-lab.py lancer
```

```text
HTTP 200
Jenkinsfile successfully validated.
[… journal du build …]
résultat : FAILURE en 2 863 ms
```

**Étape 3 — Lire l’échec bloquant.** Le journal complet est long ; les lignes décisives sont le constat et les étapes ignorées.

```bash
python3 scripts/jenkins-lab.py journal | grep -E 'Total:|skipped due|Finished:'
```

```text
Total: 1 (HIGH: 1, CRITICAL: 0)
Stage "Analyse statique" skipped due to earlier failure(s)
Stage "Qualite" skipped due to earlier failure(s)
Stage "Construction" skipped due to earlier failure(s)
Stage "Scan image" skipped due to earlier failure(s)
Finished: FAILURE
```

Le build s’arrête avant l’étape de construction : aucune image n’est produite, donc il n’y a rien à déployer. Quatre contrôles n’ont pas tourné : leur silence ne dit rien de ce qu’ils auraient trouvé.

**Étape 4 — Dater l’exception et rendre le build vert.** Créez `outils/trivyignore.yaml` avec le contenu de la technique 2, puis ajoutez `--ignorefile outils/trivyignore.yaml` à la commande bloquante de l’étape `Dependances`. Relancez le pipeline.

```bash
python3 scripts/jenkins-lab.py lancer | grep -E 'QUALITY GATE|Total:|Archiving|résultat :'
```

```text
QUALITY GATE STATUS: PASSED
Total: 0 (CRITICAL: 0)
Archiving artifacts
résultat : SUCCESS en 31001 ms
```

La ligne `Total: 0 (CRITICAL: 0)` vient du scan d’image, qui imprime un total même lorsque celui-ci vaut zéro. À l’étape `Dependances`, l’exception lève le constat, et l’étape n’affiche aucun total.

Les rapports ne sont pas versionnés dans le dépôt : le pipeline les produit dans son espace de travail, puis les archive. Interrogez l’API du dernier build pour obtenir la liste des artefacts :

```bash
curl -s http://127.0.0.1:8089/job/j2m1-pipeline/lastBuild/api/json \
  | python3 -c "
import json,sys
for a in json.load(sys.stdin)['artifacts']:
    print(a['relativePath'])
"
```

```text
rapports/dependances-medium.json
rapports/image-high.json
rapports/semgrep.json
```

**Cas d’échec à constater.** Remplacez la date par `2026-10-01`, relancez : le build redevient `FAILURE` sur le même constat, sans qu’aucune ligne du `Jenkinsfile` n’ait changé. Une exception sans date, ou dont la date est dépassée, ne protège plus.

**Étape 5 — Exécuter le DAST hors du pipeline.** Lancez le scan passif de la technique 4, puis relevez les quatre avertissements, dont trois signalent un en-tête HTTP absent. Le dossier `rapports/` doit exister avant le montage : créez-le par `mkdir -p rapports` s’il a été supprimé. Le scan actif dure 2 min 38 : gardez-le pour la fin du lab ou pour la préproduction.

```bash
python3 -c "
import json
d = json.load(open('rapports/zap-baseline.json'))
for a in d['site'][0]['alerts']:
    print(a['pluginid'], a['alert'], '| risque', a['riskcode'], '|', len(a['instances']), 'URL')
"
```

```text
10038 Content Security Policy (CSP) Header Not Set | risque 2 | 5 URL
10020 Missing Anti-clickjacking Header | risque 2 | 3 URL
10036 Server Leaks Version Information … | risque 1 | 5 URL
10021 X-Content-Type-Options Header Missing | risque 1 | 5 URL
```

**Étape 6 — Remplir les preuves et les vérifier.** Copiez le modèle, remplissez les cinq parties avec les sorties réellement observées, puis passez le contrôle. La sortie ci-dessous est celle du modèle recopié tel quel, avant remplissage.

```bash
cp preuves-controles-modele.md preuves-controles.md
bash scripts/verifier-preuves.sh preuves-controles.md; echo "code=$?"
```

```text
OK : cinq lignes de contrôle (5)
OK : trois cas d'échec (3)
OK : trois lignes « ce qu'il n'a pas vu » (3)
ECHEC : gabarit non rempli — <vos initiales>
ECHEC : gabarit non rempli — <AAAA-MM-JJ>
ECHEC : gabarit non rempli — <sha256 du fichier>
RESULTAT : 3 écart(s)
code=1
```

Le script compte des lignes de tableau et trois gabarits, mais il ne juge pas le contenu. Une ligne vide passe donc le compte, et une preuve fausse aussi.

#### Ce que ce lab produit

Le lab produit cinq contrôles renseignés dans `preuves-controles.md`, trois rapports archivés par le pipeline, le rapport ZAP produit localement, le `Jenkinsfile` modifié et `outils/trivyignore.yaml`. Ces pièces servent en J2-M2 : le [registre des vulnérabilités](#lab--analyser-et-corriger-lapplication-nordmail-existante) reprend les constats, et l’exception datée devient une échéance de correction.

**Critère de réussite.** Le build rend `SUCCESS` après l’exception datée, les cinq contrôles portent commande, sortie observée, verdict et preuve archivée, et les trois cas d’échec sont reproduits, dont celui de l’exception expirée. **Quand le contrôle manque.** Sans `--exit-code`, le SCA rend 0 sur une vulnérabilité HIGH : le build est vert alors que Werkzeug 2.3.4 reste dans l’image.

### Exercices

#### Exercice 1 — Choisir la famille d’analyse

Pour chaque situation, nommez la famille à mobiliser en premier.

1. Une bibliothèque transitive, installée par une dépendance sans être déclarée, est publiée vulnérable : vous ignorez si elle est présente.
2. Vous voulez savoir si `/export` laisse lire `/etc/passwd`.
3. Vous doutez qu’une image Debian de base soit à jour.
4. Vous cherchez un jeton dans un fichier poussé par erreur.

**Corrigé et critère.** 1 : SCA, sur le fichier de dépendances et le SBOM. 2 : DAST, seul à observer le comportement. 3 : scan d’image, pas le SCA du fichier de dépendances. 4 : détection de secrets, puis rotation, car l’historique Git conserve le fichier. Quatre réponses, chacune avec la raison pour laquelle une autre famille ne suffit pas.

#### Exercice 2 — Choisir le mode et le seuil

Trois constats sur NordMail : `CVE-2024-34069` HIGH, déploiement du correctif 3.0.3 impossible sous 48 h ; `DS-0026` LOW, HEALTHCHECK absent du `Dockerfile` ; `semgrep-nordmail-empreinte-md5` WARNING sans exploitation démontrée. Décidez pour chacun : bloquant ou consultatif, avec quel seuil, et quelle échéance.

**Corrigé et critère.** `CVE-2024-34069` : bloquant sur HIGH, ou exception datée à 30 jours avec propriétaire. `DS-0026` : consultatif sur LOW ; la règle devient bloquante dès que la supervision du conteneur ou le redémarrage automatique en dépend. `empreinte-md5` : consultatif jusqu’à preuve d’exploitation, revue à la prochaine analyse. Trois décisions datées, chacune avec le critère qui la ferait changer.

#### Exercice 3 — Trier trois alertes ZAP

Le scan actif rend `Buffer Overflow [30001]` sur `/export?fichier=notes.txt` (risque moyen, preuve `Connection: close`), `Path Traversal [6]` sur `/export?fichier=%2Fetc%2Fpasswd` (réponse 200, `root:x:0:0`) et `X-Content-Type-Options` absent. Classez : à corriger, à vérifier, à ignorer.

**Corrigé et critère.** `Path Traversal` : à corriger, preuve reproductible avec contenu de fichier. `Buffer Overflow` : à vérifier, l’en-tête HTTP n’est pas un débordement. `X-Content-Type-Options` : à corriger sans urgence, en-tête ajouté par le serveur. Trois classements justifiés par la preuve, pas par le risque affiché.

#### Exercice 4 — Mesurer le coût d’un contrôle

Le pipeline vert dure 31 s, le scan passif 33 s et le scan actif 158 s. Calculez la durée du pipeline avec le scan passif, puis avec le scan actif, pour 20 fusions par jour, et concluez.

**Corrigé et critère.** Avec le scan passif, le build dure 64 s, soit 21 min par jour. Avec le scan actif, il dure 189 s, soit 63 min par jour. Les quatre valeurs sont exactes et mènent à une décision : scan passif à chaque fusion, scan actif la nuit. Un contrôle dont la durée dépasse le temps accepté pour une fusion se désactive au premier incident, pas au premier rapport.

### Résumé

- Chacune des six familles a son périmètre : un outil se juge à ce qu’il ne lit pas.
- Un code retour 0 ne prouve pas l’absence de défaut. `--exit-code` et `--error` transforment un constat en échec.
- Une base de vulnérabilités et une exception portent chacune une date. Sans `expired_at`, l’exception ne cesse jamais de s’appliquer.
- Le scan actif attaque la cible : il exige une autorisation écrite, un environnement dédié et une exécution nocturne.
- Une quality gate mesure le code nouveau : `vulnerabilities 0` ne certifie pas le projet.

### Références

- OWASP (Open Worldwide Application Security Project) ZAP, scan de base en conteneur : <https://www.zaproxy.org/docs/docker/baseline-scan/>
- OWASP ZAP, scan complet en conteneur : <https://www.zaproxy.org/docs/docker/full-scan/>
- WSTG (Web Security Testing Guide), cadre de test d’intrusion applicatif : <https://owasp.org/www-project-web-security-testing-guide/>
- Trivy, filtrage et fichiers d’exceptions : <https://trivy.dev/latest/docs/configuration/filtering/>
- SonarQube, quality gates : <https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/quality-gates/>
- Semgrep, référence de la ligne de commande : <https://semgrep.dev/docs/cli-reference>
- National Institute of Standards and Technology (NIST), base NVD, CVE-2021-44228 : <https://nvd.nist.gov/vuln/detail/CVE-2021-44228>
- NIST NVD, CVE-2024-3094 : <https://nvd.nist.gov/vuln/detail/CVE-2024-3094>
- NIST SP 800-218, Secure Software Development Framework : <https://csrc.nist.gov/pubs/sp/800/218/final>

## Module J2-M2 — Gestion des vulnérabilités et remédiations

### Préambule

Un constat de sécurité reste ouvert tant qu’aucune décision ne le ferme. Un rapport d’outil ne désigne ni responsable, ni échéance, ni preuve de correction. Sans cycle de vie, c’est-à-dire sans étapes du constat à sa clôture, les mêmes alertes reviennent à chaque build et personne ne sait où en est chaque constat.

NordMail rend 17 constats de dépendances, dont un seul est HIGH, et des injections dans son propre code, relevées par Semgrep, analyseur statique à règles, et par le scan actif de ZAP (Zed Attack Proxy). Un classement par score place en tête la dépendance ; une lecture du code place en tête les injections. Ce module apprend à trancher entre les deux, puis à écrire la décision.

### Le vocabulaire en clair

| Terme | En clair | Où on le rencontre |
| --- | --- | --- |
| CVSS (Common Vulnerability Scoring System) | Note de gravité technique de 0 à 10, calculée sans connaître votre système. | Champ `CVSS` du rapport. |
| EPSS (Exploit Prediction Scoring System) | Probabilité, entre 0 et 1, que la faille soit exploitée dans les 30 jours. | API (Application Programming Interface) de FIRST (Forum of Incident Response and Security Teams). |
| KEV (Known Exploited Vulnerabilities) | Catalogue des failles réellement exploitées, tenu par la CISA (Cybersecurity and Infrastructure Security Agency). | `known_exploited_vulnerabilities.json`. |
| Exploitabilité | Possibilité d’atteindre le code fautif par une entrée que vous exposez. | Relecture des routes. |
| Exposition | Ce que voit un attaquant : port, authentification, réseau. | `docker-compose.yml`, `ss -ltn`. |
| Criticité métier | Ce que coûte la perte de la donnée ou du service. | Fiche d’homologation. |
| SBOM (Software Bill of Materials) | Liste datée des composants réellement présents dans un livrable. | `sbom-app.json`, `sbom-image.json`. |
| Dépendance transitive | Bibliothèque installée par une dépendance, jamais écrite dans `requirements.txt`. | `urllib3`, `markupsafe`. |
| Registre | Tableau des constats avec propriétaire, décision et échéance. | `registre-vulnerabilites.md`. |
| Constat accepté | Risque assumé par une autorité nommée, avec date de réexamen. | Ligne `acceptée` du registre. |

### Objectifs du module

À l’issue de ce module, vous serez capable de :

1. **Décrire** les six étapes du cycle de vie d’une vulnérabilité et le critère de sortie de chacune.
2. **Classer** des constats par exploitation réelle, en croisant CVSS, EPSS, KEV, exposition et criticité métier.
3. **Choisir** entre Snyk (service d’analyse des dépendances), présenté à titre documentaire uniquement (non installé, non exécuté dans cet environnement), Trivy et pip-audit (analyse des dépendances Python) selon ce que chacun lit et ce qu’il fait sortir du réseau.
4. **Produire** un SBOM et **distinguer** les composants déclarés des composants réellement installés.
5. **Tenir** un registre avec propriétaire, échéance et preuve, et **corriger** deux vulnérabilités avec preuve avant/après.

**Prérequis.** Ce module s’adresse aux développeurs, aux ingénieurs DevOps et SRE (Site Reliability Engineering), aux ingénieurs QA (Quality Assurance), aux ingénieurs sécurité et aux chefs de projet techniques. Le niveau attendu est intermédiaire, avec des bases de Git, de Docker Compose et d’un pipeline Jenkins ; les rapports produits en [J2-M1](#module-j2-m1--automatisation-des-tests-de-sécurité) servent de matière première.

### Contenu du module

#### 1. Les six étapes, et ce qui autorise à passer à la suivante

Un constat entre dans le cycle par une détection et en sort par une clôture prouvée. Entre les deux, chaque étape possède un critère de sortie écrit. Sans ce critère, le constat revient au build suivant.

| Étape | Ce qu’elle produit | Critère de sortie |
| --- | --- | --- |
| Détection | Un rapport daté, avec la version analysée. | La base et l’image sont datées dans le rapport. |
| Tri | Un constat unique par défaut réel. | Les alias, un même défaut publié sous deux identifiants, sont fusionnés et la version installée est confirmée. |
| Priorisation | Un rang et une décision. | La décision cite CVSS, EPSS, KEV, exposition et criticité. |
| Correction | Un fichier modifié. | La modification est versionnée et testée. |
| Vérification | Une sortie avant et une sortie après. | La commande ne reproduit plus le constat. |
| Clôture | Une ligne de registre fermée. | La preuve est jointe et la date de clôture est écrite. |

Le tri n’est pas une formalité. pip-audit rend 33 lignes, 18 avis distincts et 17 CVE (Common Vulnerabilities and Exposures). Un avis est l’identifiant d’un défaut dans une base, OSV (Open Source Vulnerabilities) ou GHSA (GitHub Security Advisory) : un même défaut en reçoit donc un par base. Compter les lignes gonfle le travail de près du double. Trivy rend 17 constats, un par CVE, pour les mêmes paquets.

#### 2. Prioriser : le score décrit la faille, pas votre risque

Le CVSS 3.1 note la gravité technique d’une faille sur 10. Il ignore votre exposition et la disponibilité d’un exploit public. Plusieurs sources publient ce score. Six des 17 constats de NordMail n’ont aucune valeur dans la rubrique NVD (National Vulnerability Database) du rapport Trivy, alors que GHSA et Red Hat les notent. Un score absent d’une rubrique peut donc exister ailleurs : il faut interroger plusieurs sources avant de conclure.

| Indicateur | Ce qu’il mesure | Ce qu’il ignore | Source |
| --- | --- | --- | --- |
| CVSS 3.1 | Gravité intrinsèque, de 0 à 10. | Votre exposition, l’exploitation réelle. | FIRST, NVD. |
| EPSS | Probabilité d’exploitation sous 30 jours. | La gravité si la faille est exploitée. | FIRST, mise à jour quotidienne. |
| KEV | Exploitation observée dans le monde. | Les failles non encore exploitées. | CISA, catalogue daté. |
| Exposition | Atteignabilité depuis une entrée exposée. | La valeur de la donnée atteinte. | Lecture du code et des ports. |
| Criticité métier | Conséquence d’une compromission. | La facilité de l’attaque. | Fiche d’homologation. |

La mesure du 2026-10-30 sur NordMail donne un EPSS maximal de 0,03397, pour CVE-2024-34069, soit le 88,8e centile, et aucune des 17 CVE ne figure au catalogue KEV. Aucune de ces failles n’est donc une urgence d’exploitation. Deux injections du code, en revanche, s’atteignent par une seule requête.

Log4Shell présente le contraste inverse. CVE-2021-44228 affiche un CVSS 3.1 de 10,0 et un EPSS de 0,99999. Elle figure au catalogue KEV depuis le 10 décembre 2021, avec un usage rançongiciel documenté. Une faille de cette classe ne se planifie pas à trente jours.

```bash
curl -s https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['catalogVersion'], d['count'], [v['dateAdded'] for v in d['vulnerabilities'] if v['cveID']=='CVE-2021-44228'])"
```

```text
2026.10.30 1766 ['2021-12-10']
```

La règle de décision comporte quatre points. Une vulnérabilité inscrite au KEV se corrige sous 7 jours, quelle que soit sa sévérité. Un EPSS supérieur à 0,1 se traite comme un constat HIGH : ce seuil est interne, non une recommandation de FIRST, et il ne retient que 4,4 % des 398 142 CVE notées le 2026-10-30. Un constat non atteignable descend d’un rang sans disparaître, et un CVSS absent se remplace par une évaluation interne, jamais par zéro.

L’exposition change le rang plus que le score. CVE-2024-34069 touche la console de débogage de Werkzeug, la bibliothèque serveur de Flask. Celle-ci n’est active que si `debug=True`, ce que NordMail fait : la faille est donc atteignable sur `127.0.0.1:8099`. La criticité métier départage le reste : la lecture de notes de réunion et celle de coordonnées de bénéficiaires n’ont pas le même poids, à CVSS et à EPSS égaux.

#### 3. Snyk, Trivy, pip-audit : trois lectures, un inventaire

Les trois outils ne lisent pas la même chose. Snyk interroge son propre service et suit un projet dans le temps. Trivy compare des fichiers ou une image à une base locale. pip-audit résout l’arbre des dépendances et interroge OSV.

| Outil | Ce qu’il lit | Compte et réseau | Ce qu’il ne voit pas |
| --- | --- | --- | --- |
| `snyk test` (documentaire) | Dépendances déclarées, remontées à Snyk. | Jeton `{env:SNYK_TOKEN}` requis hors session authentifiée. | Le code de l’application. |
| `snyk monitor` (documentaire) | Le même graphe, conservé côté service. | Même jeton, envoi durable du graphe. | Ce qui n’est pas déclaré. |
| `trivy fs` | `requirements.txt` ou image complète. | Aucun compte ; base téléchargée, réseau requis. | Les transitives non déclarées. |
| `pip-audit -r` | Le fichier, arbre résolu. | Aucun compte ; OSV interrogé en ligne. | La gravité et la priorisation. |

Sans jeton, `snyk test` s’arrête sur un message d’authentification et ne produit aucun constat. Avec un jeton, `snyk monitor` conserve le graphe côté service et alerte quand une CVE est publiée plus tard ; sans compte, seul un scan planifié rafraîchit le rapport. Snyk n’est pas installé dans cet environnement : les deux commandes du tableau sont documentaires uniquement, non vérifiées ici, et les équivalents sans compte sont mesurés dans les techniques.

#### 4. SBOM, transitives, et failles sans correctif

Un SBOM répond vite à une seule question, y compris pour une faille publiée après la livraison : « suis-je exposé ? » Trois périmètres permettent d’y répondre, et ils ne donnent pas le même nombre de composants.

| Périmètre | Commande de comptage | Composants |
| --- | --- | --- |
| Fichier de dépendances | `trivy fs --format cyclonedx` | 5 |
| Dépendances résolues | `pip-audit -r` | 12 |
| Image construite | `trivy image --format cyclonedx` | 101 |

Les 5 composants du fichier sont les quatre dépendances directes et le fichier lui-même. Les huit dépendances transitives n’y figurent pas, alors qu’elles sont installées dans l’image : `blinker`, `certifi`, `charset-normalizer`, `click`, `idna`, `itsdangerous`, `markupsafe` et `urllib3`. Ce que vous déclarez n’est pas ce que vous livrez.

Épingler quatre dépendances directes ne fige pas l’image. Les transitives varient au moment du `pip install`, donc deux constructions à une semaine d’intervalle peuvent contenir des versions différentes. Le SBOM d’image daté est la trace la plus fidèle de ce qui a réellement tourné : 101 composants, base Debian comprise, contre 5 pour le fichier.

L’image `j2m1-app:1` porte 187 constats. Pour 164 d’entre eux, aucune version corrigée n’est publiée, parmi lesquels 44 HIGH dans la base Debian. Un constat sans correctif admet trois réponses : atténuer, isoler ou surveiller. Ici, l’équipe retire les paquets inutiles de l’image, garde l’exécution sous l’utilisateur `10001` déjà déclaré et ne publie le port que sur `127.0.0.1`. Elle réexamine ensuite le constat à chaque reconstruction planifiée, selon une cadence écrite.

La porte dérobée de xz-utils, publiée sous CVE-2024-3094 le 29 mars 2024, n’était dans aucune base de vulnérabilités avant sa révélation. Aucun des trois outils ne l’aurait signalée. Le SBOM a servi à mesurer l’exposition après coup, pas à prévenir.

#### 5. Registre, échéances, dette

Un registre tient sur douze colonnes : identifiant, composant, sévérité, CVSS, EPSS, KEV, décision, propriétaire, date de détection, échéance, autorité avec sa date de réexamen, preuve. Une ligne sans propriétaire ne peut pas être clôturée, et une ligne sans preuve n’a pas d’état vérifiable.

| Sévérité | Délai de correction | Cas KEV |
| --- | --- | --- |
| CRITICAL | 7 jours | 7 jours, quelle que soit la sévérité |
| HIGH | 30 jours | idem |
| MEDIUM | 90 jours | idem |
| LOW | 180 jours | idem |

Le registre n’admet que cinq décisions : `corrigée`, `planifiée`, `atténuée`, `acceptée` et `fausse alerte`. Une valeur hors de cette liste est un commentaire, pas un suivi. Une ligne `acceptée` sans autorité nommée, ou sans date de réexamen, est un oubli déguisé. Trois indicateurs pilotent la dette : le nombre de constats ouverts hors échéance, l’âge médian calculé depuis la date de détection et la part des constats qui ont un propriétaire.

### Les techniques, pas à pas

Les quatre techniques et le lab s’exécutent dans `labs/lab-jour-02/j2-m2`. La cible de travail est une copie de la pile J2-M1 ; la pile d’origine n’est jamais modifiée :

```bash
cd labs/lab-jour-02/j2-m2
mkdir -p travail && cp -a ../j2-m1/app/. travail/app/
```

#### Technique 1 — Trois vues du même rapport

```bash
trivy fs --scanners vuln --no-progress --quiet travail/app 2>/dev/null | grep Total
trivy fs --scanners vuln --severity HIGH,CRITICAL --no-progress --quiet travail/app 2>/dev/null | grep Total
pip-audit -r travail/app/requirements.txt --format json 2>/dev/null \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('lignes', sum(len(x['vulns']) for x in d['dependencies']), 'paquets', len(d['dependencies']))"
```

```text
Total: 17 (UNKNOWN: 0, LOW: 1, MEDIUM: 15, HIGH: 1, CRITICAL: 0)
Total: 1 (HIGH: 1, CRITICAL: 0)
lignes 33 paquets 12
```

Ces sorties prouvent qu’il existe 17 vulnérabilités distinctes, dont une seule dépasse le seuil, et que 12 paquets sont réellement résolus. Elles ne prouvent pas que les 16 constats MEDIUM sont inoffensifs, ni que les 17 sont atteignables.

#### Technique 2 — Classer par exploitation réelle

Le script `outils/prioriser.py` combine trois sources : le rapport Trivy, l’EPSS du jour et le catalogue KEV. Il trie par présence au KEV, puis par EPSS décroissant, et il affiche le CVSS avec la source qui le fournit : NVD, GHSA ou Red Hat.

```bash
trivy fs --scanners vuln --format json --output rapport-trivy.json --no-progress --quiet travail/app
python3 outils/prioriser.py rapport-trivy.json
```

```text
CVE-2024-34069   Werkzeug   HIGH    CVSS 7.5   ghsa   EPSS 0.03397 KEV non
CVE-2023-46136   Werkzeug   MEDIUM  CVSS 7.5   nvd    EPSS 0.01288 KEV non
CVE-2024-49767   Werkzeug   MEDIUM  CVSS 7.5   nvd    EPSS 0.01095 KEV non
CVE-2024-47081   requests   MEDIUM  CVSS 5.3   ghsa   EPSS 0.00980 KEV non
[…13 lignes, mêmes colonnes, EPSS décroissant…]
```

Les deux premières lignes portent le même CVSS, 7,5. Seule la première est classée HIGH : l’ordre entre elles vient donc de l’EPSS. La quatrième n’a aucune valeur dans la rubrique NVD. Le repli sur GHSA, puis sur Red Hat, évite une colonne vide et un rang incomparable.

#### Technique 3 — Corriger la traversée de chemin, avec preuve avant et après

`/export` ouvre un fichier dont le nom vient de l’URL (Uniform Resource Locator). La preuve avant tient en une seule requête, exécutée dans l’image, sans serveur ni port.

```bash
docker run --rm j2m1-app:1 python -c "
from app import app
c = app.test_client()
r = c.get('/export?fichier=%2Fetc%2Fpasswd')
print('export', r.status_code, r.data[:20])
"
```

```text
export 200 b'root:x:0:0:root:/roo'
```

Le correctif, dans `travail/app/app.py`, remplace `os.path.join` par `werkzeug.utils.safe_join`, qui rend `None` quand le chemin sort du répertoire autorisé. `BASE_EXPORT`, déclarée ligne 26 de `app.py`, vaut `/srv/nordmail/export`.

```python
from werkzeug.utils import safe_join

@app.get("/export")
def exporter():
    nom = request.args.get("fichier", "notes.txt")
    chemin = safe_join(BASE_EXPORT, nom)
    if chemin is None:
        return jsonify({"erreur": "fichier inconnu"}), 404
    with open(chemin, "rb") as fichier:
        return fichier.read()
```

```bash
docker run --rm -v "$PWD/travail/app:/app:ro" j2m1-app:1 python -c "
from app import app
c = app.test_client()
for u in ('/export?fichier=%2Fetc%2Fpasswd','/export?fichier=notes.txt'):
    r = c.get(u); print(u, r.status_code, r.data[:24])
"
```

```text
/export?fichier=%2Fetc%2Fpasswd 404 b'{"erreur":"fichier incon'
/export?fichier=notes.txt 200 b'export de demonstration\n'
```

Le code 404, ressource absente, ne prouve pas à lui seul la correction : l’application pourrait refuser tous les fichiers. Le 200 sur `notes.txt` montre que la route sert encore à son usage. La paire des deux réponses constitue la preuve.

#### Technique 4 — Corriger les dépendances, reconstruire, produire le SBOM

Le fichier de dépendances passe à Flask 3.1.3, Werkzeug 3.1.9, Jinja2 3.1.6 et requests 2.33.0. La même commande que la technique 1 rend alors zéro constat.

```bash
printf 'Flask==3.1.3\nWerkzeug==3.1.9\nJinja2==3.1.6\nrequests==2.33.0\n' > travail/app/requirements.txt
trivy fs --scanners vuln --no-progress --quiet travail/app 2>/dev/null | grep -E "requirements|Total"
pip-audit -r travail/app/requirements.txt; echo "code=$?"
```

```text
│ requirements.txt │ pip  │        0        │
No known vulnerabilities found
code=0
```

Corriger le fichier ne corrige pas l’image en service : il faut reconstruire l’image, puis la rescanner. Le filtre `--pkg-types` sépare les deux périmètres, sans quoi un seul total mélange bibliothèques et base Debian.

```bash
trivy image --scanners vuln --pkg-types library --severity HIGH,CRITICAL \
  --no-progress --quiet j2m1-app:1 | grep Total
trivy image --scanners vuln --pkg-types os --severity HIGH,CRITICAL \
  --no-progress --quiet j2m1-app:1 | grep Total
```

```text
Total: 1 (HIGH: 1, CRITICAL: 0)
Total: 44 (HIGH: 44, CRITICAL: 0)
```

Le 1 correspond à Werkzeug 2.3.4, seul constat de bibliothèque au-dessus du seuil. Les 44 autres viennent de la base Debian et forment avec lui les 45 HIGH du scan complet.

```bash
docker build -t j2m2-app:1 travail/app
trivy image --scanners vuln --pkg-types library --severity HIGH,CRITICAL --no-progress --quiet j2m2-app:1 | grep Total
```

Ce `docker build` n’est pas vérifié dans cet environnement. Depuis le démon Docker, `pip install` ne résout pas PyPI : il échoue avec `Temporary failure in name resolution`, y compris avec `--network host`. Sur l’hôte, l’installation des quatre versions épinglées aboutit. Après reconstruction, la première ligne devrait tomber à `Total: 0`, et les 44 HIGH de la base Debian resteraient à traiter.

Les deux SBOM sont produits par la même option `--format cyclonedx`. Le nombre de composants dépend du périmètre, pas de l’outil.

```bash
trivy fs --format cyclonedx --output sbom-app.json --no-progress --quiet travail/app
trivy image --format cyclonedx --output sbom-image.json --no-progress --quiet j2m1-app:1
python3 -c "
import json
for f in ('sbom-app.json','sbom-image.json'):
    d=json.load(open(f)); print(f, d['specVersion'], len(d['components']))
"
```

```text
sbom-app.json 1.7 5
sbom-image.json 1.7 101
```

### Lab — Analyser et corriger l’application NordMail existante

Le lab reprend la pile de J2-M1 sans la modifier : `docker-compose.yml`, `app/`, `Jenkinsfile` et `outils/` restent dans `../j2-m1/`. Vous travaillez sur une copie, dans `travail/app`, et vous produisez un registre et un rapport d’analyse.

#### Prérequis

- avoir exécuté les quatre techniques de ce module ;
- pile [`labs/lab-jour-02/j2-m1/`](#lab--intégrer-trois-outils-dans-le-pipeline-de-nordmail) démarrée et `curl http://127.0.0.1:8099/sante` qui répond `"statut": "ok"` ;
- réseau nécessaire pour la base Trivy (`trivy`), pour OSV (`pip-audit`), pour l’API EPSS et pour le catalogue KEV (`prioriser.py`) ; sans DNS, `prioriser.py` s’arrête sur `urlopen error [Errno -3] Temporary failure in name resolution` et la technique 2 n’est pas reproductible ;
- ports `8099`, `9000` et `8089` déjà tenus par la pile J2-M1, à ne pas relancer.

#### Environnement

| Élément | Valeur |
| --- | --- |
| Hôte | Ubuntu 26.04, Docker local, sans orchestration |
| Docker Engine et Compose | 29.1.3 et 2.40.3 |
| Dossier du lab | `labs/lab-jour-02/j2-m2/` |
| Application | `127.0.0.1:8099`, image `j2m1-app:1`, réutilisée depuis J2-M1 |
| Dossier de travail | `travail/app`, copie de `../j2-m1/app` |
| Trivy | 0.71.2 sur l’hôte, base du 2026-10-30 |
| pip-audit | 2.10.1, base OSV |
| Snyk | absent, aucun compte, aucune commande exécutée |
| Registre et rapport | `registre-vulnerabilites.md` et `rapport-analyse.md`, copiés des modèles |

#### Étapes du lab

**Étape 1 — Remettre la copie en état et vérifier la cible.** La pile J2-M1 tourne déjà ; ne relancez `docker compose up -d` que si `curl` échoue. La copie a servi aux techniques : cette commande la rend à son état d’origine.

```bash
cd labs/lab-jour-02/j2-m2
mkdir -p travail && cp -a ../j2-m1/app/. travail/app/
curl -s http://127.0.0.1:8099/sante
curl -s -o /dev/null -w "%{http_code}\n" "http://127.0.0.1:8099/export?fichier=%2Fetc%2Fpasswd"
```

```text
{
  "statut": "ok"
}
200
```

Flask en `debug=True` renvoie du JSON (JavaScript Object Notation) indenté : la sortie tient sur trois lignes, ce qui n’est pas un échec. Le 200 sur `/export?fichier=%2Fetc%2Fpasswd` est la preuve avant du constat principal : l’application lit un fichier du système.

**Cas d’échec à constater.** Si `curl` ne répond pas, la pile est arrêtée : `cd ../j2-m1 && docker compose up -d` puis attendre `"statut": "ok"`. Un lab lancé sur une pile éteinte produit des rapports vides, pas des preuves.

**Étape 2 — Collecter les constats.** Deux rapports, deux formats, une date.

```bash
trivy fs --scanners vuln --format json --output rapport-trivy.json \
  --no-progress --quiet travail/app
pip-audit -r travail/app/requirements.txt --format json > rapport-pipaudit.json; echo "code=$?"
python3 -c "
import json
t=json.load(open('rapport-trivy.json')); p=json.load(open('rapport-pipaudit.json'))
print('trivy', sum(len(r.get('Vulnerabilities') or []) for r in t['Results']),
      'pip-audit', sum(len(x['vulns']) for x in p['dependencies']))
"
```

```text
code=1
trivy 17 pip-audit 33
```

pip-audit rend 1 lorsqu’il trouve une vulnérabilité : le code retour signale un constat, pas une panne. Un script qui traite 1 comme une erreur d’exécution confond les deux.

**Étape 3 — Classer et décider.** Lancez `python3 outils/prioriser.py rapport-trivy.json`, puis remplissez les cinq premières lignes du rapport d’analyse. Chaque rang doit citer un critère d’exposition : route atteignable, `debug=True`, aucune authentification.

```bash
python3 outils/prioriser.py rapport-trivy.json | head -5
```

```text
CVE-2024-34069   Werkzeug   HIGH    CVSS 7.5   ghsa   EPSS 0.03397 KEV non
CVE-2023-46136   Werkzeug   MEDIUM  CVSS 7.5   nvd    EPSS 0.01288 KEV non
CVE-2024-49767   Werkzeug   MEDIUM  CVSS 7.5   nvd    EPSS 0.01095 KEV non
CVE-2024-47081   requests   MEDIUM  CVSS 5.3   ghsa   EPSS 0.00980 KEV non
CVE-2024-34064   Jinja2     MEDIUM  CVSS 5.4   ghsa   EPSS 0.00979 KEV non
```

Aucune ligne KEV et un EPSS maximal de 0,034 : la priorité ne vient pas des dépendances. Elle vient des routes lues à l’étape 1, du rapport DAST (Dynamic Application Security Testing) du scan actif de J2-M1, `rapports/zap-full.json` dans `labs/lab-jour-02/j2-m1/`, et du rapport Semgrep `rapports/semgrep.json`, que le `Jenkinsfile` produit à chaque exécution. Le scan actif s’exécute hors du pipeline : s’il n’a pas été lancé à l’étape 5 de J2-M1, `zap-full.json` manque et les deux constats ZAP du registre restent sans preuve.

Le scan actif rend onze alertes, que le registre ramène à quatre lignes, une par constat, dont deux portent aussi une règle Semgrep. Le paramètre `q` est celui de `/recherche` : les deux XSS (Cross-Site Scripting), réfléchi et DOM (Document Object Model), ont la même cause que l’injection de gabarit et tiennent donc dans sa ligne, et `[90037]` ne fait que répéter `[90020]`. Les quatre alertes d’en-têtes HTTP (HyperText Transfer Protocol) relèvent de l’étape 5 du lab de [J2-M1](#module-j2-m1--automatisation-des-tests-de-sécurité).

**Étape 4 — Corriger la traversée de chemin.** Appliquez le correctif de la technique 3 dans `travail/app/app.py`, puis prouvez l’avant et l’après.

```bash
docker run --rm -v "$PWD/travail/app:/app:ro" j2m1-app:1 python -c "
from app import app
c = app.test_client()
for u in ('/export?fichier=%2Fetc%2Fpasswd','/export?fichier=notes.txt'):
    r = c.get(u); print(u, r.status_code, r.data[:24])
"
```

```text
/export?fichier=%2Fetc%2Fpasswd 404 b'{"erreur":"fichier incon'
/export?fichier=notes.txt 200 b'export de demonstration\n'
```

**Cas d’échec à constater.** Remplacez `safe_join` par `os.path.join` en gardant le contrôle `if chemin is None` : le 404 disparaît, la route rend de nouveau 200 sur `/etc/passwd`. Un correctif qui ne s’exécute pas ne corrige rien.

**Étape 5 — Corriger les dépendances, produire le SBOM, remplir le registre.** Reprenez les commandes de la technique 4 sur `travail/app`. La montée de version rend `requirements.txt │ pip │ 0` et `No known vulnerabilities found`, les deux SBOM sont produits et datés sans reconstruction. Le `docker build` et le rescan d’image, eux, exigent un accès à PyPI depuis le démon Docker. Sans cet accès, la preuve d’image manque : le registre l’écrit au lieu de l’ignorer.

Copiez les modèles, remplissez une ligne par constat, puis passez le contrôle de forme ; la sortie ci-dessous est celle du corrigé.

```bash
cp registre-vulnerabilites-modele.md registre-vulnerabilites.md
cp rapport-analyse-modele.md rapport-analyse.md
bash scripts/verifier-registre.sh registre-vulnerabilites.md
```

```text
OK : 18 ligne(s) en décision « corrigée »
OK : 5 ligne(s) en décision « planifiée »
OK : 1 ligne(s) en décision « atténuée »
OK : 1 ligne(s) en décision « fausse alerte »
INFO : 25 ligne(s) de constat analysée(s)
RESULTAT : registre conforme
```

Le script compte des lignes et vérifie des formats, dans un ordre fixe, mais une preuve fausse passe le contrôle. Il refuse en revanche six défauts : un propriétaire vide, une date de détection absente, une échéance hors format, une décision inventée, une acceptation sans autorité et une atténuation sans date de réexamen.

#### Ce que ce lab produit

Le lab produit `registre-vulnerabilites.md`, avec 25 constats : 17 CVE, quatre constats Semgrep, deux constats ZAP, une relecture manuelle et une ligne pour les 44 HIGH de la base. Il produit aussi `rapport-analyse.md`, avec cinq rangs et deux preuves avant et après, deux SBOM datés et un dossier `travail/app` corrigé sur deux points. Le registre sert en [J3-M2](jour-03.md#module-j3-m2--approches-avancées-pour-secdevops) : les [indicateurs de dette](jour-03.md#lab--tableau-de-bord-de-surveillance) s’en déduisent sans nouvelle collecte.

**Critère de réussite.** La route rend 404 sur `/export?fichier=%2Fetc%2Fpasswd` et 200 sur `notes.txt`, `trivy fs` et `pip-audit` ne rendent aucun constat sur `travail/app` après la montée des dépendances, et le registre est conforme avec au moins huit constats, chacun porteur d’un propriétaire, d’une date de détection, d’une échéance et d’une preuve. **Quand le contrôle manque.** Une ligne `planifiée` sans échéance, ou une ligne `acceptée` sans autorité, laisse le constat ouvert sans que personne ne le sache.

### Exercices

#### Exercice 1 — Classer trois constats

Trois constats portent sur le même service. Le premier est CVE-2021-44228, de CVSS 10,0 et d’EPSS 0,99999, présent au KEV depuis 2021. Le second est CVE-2024-34069, de CVSS 7,5 et d’EPSS 0,03397, absent du KEV. Le troisième est une injection de commande dans `/ping`, sans CVE. Classez-les et nommez le critère qui tranche.

**Corrigé et critère.** Log4Shell vient en premier, car le KEV impose 7 jours quelle que soit la sévérité. L’injection de commande vient ensuite, car elle est atteignable par une seule requête et n’a pas de correctif de bibliothèque. CVE-2024-34069 vient en dernier, avec un EPSS de 0,034 et un correctif disponible. Trois rangs et trois critères nommés, dont un hors score.

#### Exercice 2 — Décider sans correctif

L’image porte 44 constats HIGH sans version corrigée dans Debian. Choisissez la décision du registre et les trois contrôles qui la rendent défendable.

**Corrigé et critère.** La décision est `atténuée`, avec une date de réexamen à la prochaine reconstruction. Trois contrôles la rendent défendable : le retrait des paquets inutiles, l’exécution sous l’utilisateur `10001` et la publication du port limitée à `127.0.0.1`. Une ligne `acceptée` sans autorité nommée serait un oubli déguisé.

#### Exercice 3 — Lire un registre et calculer ses échéances

Trois lignes ont été détectées le 2026-10-31. La ligne `A` est corrigée, avec la preuve `trivy 0`, une échéance au 2026-11-30 et la valeur `sans objet` en autorité. La ligne `B` est acceptée, avec le propriétaire `resp-metier`, une échéance au 2027-01-29, la valeur `sans objet` en autorité et la justification « risque faible ». La ligne `C` est atténuée, avec le propriétaire `dev-nordmail`, une échéance au 2026-12-15 et la valeur `resp-plateforme / 2026-12-15`. Laquelle de ces lignes est une vulnérabilité oubliée, et pourquoi ? Donnez ensuite les échéances d’un CRITICAL, d’un HIGH, d’un MEDIUM et d’un MEDIUM présent au catalogue KEV.

**Corrigé et critère.** La ligne `B` est la vulnérabilité oubliée : elle est `acceptée` sans autorité nommée, donc sans responsable du risque accepté. La ligne `A` porte une preuve, et la ligne `C` porte un propriétaire et une date de réexamen. Les échéances sont le 2026-11-07 pour un CRITICAL, le 2026-11-30 pour un HIGH, le 2027-01-29 pour un MEDIUM et le 2026-11-07 pour un MEDIUM présent au catalogue KEV. Cinq réponses exactes, et la règle KEV appliquée avant la sévérité.

### Résumé

- Le CVSS décrit la faille ; le KEV et l’EPSS décrivent l’exploitation ; l’exposition et la criticité métier décident du rang.
- Trois outils, trois inventaires : 5 composants déclarés, 12 résolus, 101 installés.
- Le SBOM daté répond à une alerte publiée après la livraison ; il ne prévient pas d’une faille inconnue, comme xz-utils en mars 2024.
- Sur 187 constats de l’image, 164 n’ont pas de correctif : il faut atténuer, reconstruire et réexaminer à date fixe.

### Références

- FIRST, spécification CVSS 3.1 : <https://www.first.org/cvss/v3-1/specification-document>
- FIRST, EPSS, méthode et API : <https://www.first.org/epss/>
- CISA, catalogue des vulnérabilités exploitées : <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- National Institute of Standards and Technology (NIST) SP 800-218, Secure Software Development Framework (SSDF), pratiques RV.1 et RV.2 : <https://csrc.nist.gov/pubs/sp/800/218/final>
- CycloneDX, spécification du format SBOM : <https://cyclonedx.org/specification/overview/>
- Snyk, référence de la ligne de commande : <https://docs.snyk.io/snyk-cli>
- Trivy, génération de SBOM : <https://trivy.dev/latest/docs/supply-chain/sbom/>
- pip-audit, utilisation : <https://pypi.org/project/pip-audit/>
- NIST NVD, CVE-2021-44228 : <https://nvd.nist.gov/vuln/detail/CVE-2021-44228>
