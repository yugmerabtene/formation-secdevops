# Préparation du poste pour les labs SecDevOps

Cette page prépare un poste Windows, macOS, Ubuntu Desktop ou Debian 13 à exécuter les huit modules du cours. Les commandes se lancent dans un shell Linux ou dans le Terminal de macOS : Ubuntu natif ou Debian 13, distribution WSL 2 (Windows Subsystem for Linux 2), machine virtuelle (VM), ou Terminal en `zsh`.

## Matériel et périmètre

| Élément | Minimum | Recommandé |
| --- | --- | --- |
| Mémoire vive | 8 Go | 16 Go |
| Processeurs | 4 cœurs | 6 cœurs |
| Disque libre | 40 Go | 60 Go |
| Virtualisation matérielle | activée dans le firmware | activée |

Les labs exécutent Docker local, Jenkins, une application Python 3.12 et Flask, puis Trivy, SonarQube, Prometheus, Alertmanager, Grafana et Loki en conteneurs. Aucun cluster Kubernetes, aucun service en nuage, aucun compte obligatoire. Six dossiers de lab contiennent un `docker-compose.yml` ; J1-M1 se lit sans démarrer sa pile, J2-M2, J3-M1 et J3-M3 n’en ont pas.

## Quelle distribution Linux pour les labs

Installez Ubuntu 24.04 LTS (Long Term Support) Desktop, architecture x86_64 (amd64). Le noyau est 6.8 pour l’image initiale ; les images 24.04.2 et suivantes livrent un noyau HWE (Hardware Enablement) 6.11 ou 6.14, sans effet sur les labs.

- Docker Engine publie des paquets `noble` maintenus : la liste des versions de la documentation Docker affiche `docker-ce/noble 5:29.8.2-1~ubuntu.24.04~noble`, relevé le 31 octobre 2026.
- Ubuntu 24.04 reçoit les mises à jour de sécurité standard jusqu’en avril 2029 (Canonical).
- L’installateur graphique, les Additions invité de la version de VirtualBox installée et les images `amd64` des labs se tirent sans émulation ; `python:3.12-slim`, la base des applications, repose sur Debian 13 (trixie).

| Choix | Verdict | Limite |
| --- | --- | --- |
| Debian 13 | acceptable | mêmes commandes `apt`, dépôt Docker à configurer comme ci-dessous |
| Ubuntu 26.04 LTS | acceptable sous condition | `curl -fsSL https://download.docker.com/linux/ubuntu/dists/resolute/Release` doit répondre, sinon restez en 24.04 |
| Fedora, Arch, RHEL (Red Hat Enterprise Linux) | hors périmètre | les commandes du cours sont écrites pour `apt` et `docker compose` |

**Piège ARM (Advanced RISC Machine).** Les images des labs ne sont pas toutes publiées pour `arm64`. Relevé le 31 octobre 2026 : `mailhog/mailhog:v1.0.1` (J1-M3) et `sonarsource/sonar-scanner-cli:12.3.0.4285_8.1.0` (J2-M1) n’existent qu’en `amd64` ; SonarQube publie les deux. Sur Apple Silicon, l’émulation Rosetta de Docker Desktop les exécute lentement. Sur un moteur `arm64` sans binfmt ni qemu, le conteneur s’arrête sur `exec format error`. Un poste `amd64` évite le sujet.

## Installer tous les outils d’un coup

Chaque outil ci-dessous sert dans au moins un module. Installez-les tous au départ, jamais au fil des modules.

| Outil | À quoi il sert | Installation | Vérification |
| --- | --- | --- | --- |
| `git` | Cloner le cours, suivre les livrables | `apt` ou `brew` | `git --version` |
| `curl` | Interroger les ports publiés par les labs | `apt` ou `brew` | `curl --version` |
| `jq` | Relire les sorties JSON (JavaScript Object Notation) | `apt` ou `brew` | `jq --version` |
| Docker Engine ou Docker Desktop | Exécuter les conteneurs des labs | bloc ci-dessous | `docker version` |
| module Compose | Démarrer une pile de lab | `docker-compose-plugin` | `docker compose version` |
| Python 3.12 | Langage de l’application des labs | fourni par Ubuntu 24.04 | `python3 --version` |
| `pip`, `pipx` | Isoler les outils Python | `python3-pip`, `pipx` | `pipx --version` |
| `trivy` | Scanner images, dépendances, configurations | dépôt Aqua | `trivy --version` |
| `semgrep` | Analyse statique du code applicatif | `pipx install semgrep` | `semgrep --version` |
| `gitleaks` | Détecter les secrets dans un dépôt | binaire GitHub | `gitleaks version` |
| `hadolint` | Analyser un `Dockerfile` | binaire GitHub | `hadolint --version` |
| `pip-audit` | Auditer les dépendances Python | `pipx install pip-audit` | `pip-audit --version` |
| `bandit` | Chercher les motifs dangereux en Python | `pipx install bandit` | `bandit --version` |
| `snyk` | Comparer une application au service Snyk | facultatif, voir note | `snyk --version` |

`snyk test` exige une authentification (`SNYK_TOKEN`) : sans compte, la commande s’arrête sur un message d’authentification et ne produit aucun constat. Aucun lab ne l’appelle, l’installation reste facultative.

`promtool` et `amtool` ne s’installent pas : ils viennent des images. `docker run --rm --entrypoint promtool prom/prometheus:v2.55.1 --version` rend `promtool, version 2.55.1 …` et `docker run --rm --entrypoint amtool prom/alertmanager:v0.27.0 --version` rend `amtool, version 0.27.0 …` (mesuré le 31 octobre 2026).

### Ubuntu 24.04 et Debian 13

```bash
set -euo pipefail
sudo apt update
sudo apt install -y git curl jq python3-pip pipx gnupg && pipx ensurepath
# Dépôt Docker officiel : clé GPG (GNU Privacy Guard) puis fichier docker.list
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"
# Trivy, dépôt officiel Aqua
curl -fsSL https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | sudo tee /etc/apt/sources.list.d/trivy.list > /dev/null
sudo apt update && sudo apt install -y trivy
# Outils Python isolés, puis binaires hors paquets Debian
pipx install semgrep && pipx install pip-audit && pipx install bandit
# Binaires GitHub : somme SHA-256 vérifiée, installation enchaînée à la vérification
curl -fsSLO https://github.com/gitleaks/gitleaks/releases/download/v8.28.0/gitleaks_8.28.0_linux_x64.tar.gz
curl -fsSL https://github.com/gitleaks/gitleaks/releases/download/v8.28.0/gitleaks_8.28.0_checksums.txt | grep linux_x64 | sha256sum -c - && sudo tar -xzf gitleaks_8.28.0_linux_x64.tar.gz -C /usr/local/bin gitleaks
sudo curl -fsSL -o /usr/local/bin/hadolint https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64
echo "56de6d5e5ec427e17b74fa48d51271c7fc0d61244bf5c90e828aab8362d55010  /usr/local/bin/hadolint" | sha256sum -c - && sudo chmod +x /usr/local/bin/hadolint
```

Sur Debian 13, remplacez `ubuntu` par `debian` dans les deux URL du dépôt Docker. Le bloc ouvre sur `set -euo pipefail` et chaque installation suit sa vérification par `&&` : un `FAILED` de `sha256sum -c` arrête la suite, `tar` et `chmod` ne touchent jamais un binaire non conforme. Vérification groupée, après réouverture du terminal pour que le groupe `docker` s’applique :

```bash
git --version && jq --version && docker compose version && python3 --version \
  && trivy --version | head -1 && semgrep --version && gitleaks version \
  && hadolint --version && pip-audit --version && bandit --version | head -1
```

Attendu : dix lignes de version, aucune erreur, et `OK` pour les deux `sha256sum -c` du bloc. Mesures du 31 octobre 2026 sur un poste amd64 : `git 2.53.0`, `jq 1.8.1`, Compose `2.40.3`, Trivy `0.71.2`, Semgrep `1.168.0`, `gitleaks 8.28.0`, hadolint `2.12.0`, `pip-audit 2.10.1`.

### macOS, avec Homebrew

```bash
brew install git jq pipx trivy gitleaks hadolint
pipx install semgrep && pipx install pip-audit && pipx install bandit
pipx ensurepath    # ajoute ~/.local/bin au PATH : rouvrez le Terminal ensuite
brew install --cask docker && open -a Docker
brew tap snyk/tap && brew install snyk/tap/snyk   # facultatif
```

Attendu : `brew` installe les formules sans erreur et `open -a Docker` démarre Docker Desktop, dont le client fournit `docker` et `docker compose`. Sans `pipx ensurepath` et sans réouverture du Terminal, `semgrep --version` rend `command not found`. Vérification : la commande groupée ci-dessus.

### Windows 11, avec WSL 2

```powershell
# PowerShell en administrateur
wsl --install -d Ubuntu-24.04
wsl --update
```

Dans le terminal Ubuntu fourni par WSL 2, deux moteurs possibles :

- **Docker Desktop.** Sautez la ligne `apt install … docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin` et la ligne `usermod` du bloc Ubuntu, puis activez l’intégration de la distribution dans les réglages de Desktop.
- **Docker Engine dans la distribution.** Aucun abonnement : exécutez le bloc Ubuntu sans modification, puis rouvrez la distribution pour que le groupe `docker` s’applique.

Vérification dans les deux cas : la commande groupée, puis `docker version`, qui affiche une section Client et une section Server.

## Choisir son chemin

| Poste | Chemin | Pourquoi |
| --- | --- | --- |
| Windows 11 | Docker Desktop avec moteur WSL 2, ou Docker Engine dans la distribution WSL 2 | moteur Linux fourni ; la variante Engine évite l’abonnement Desktop |
| macOS | Docker Desktop | même moteur, Rosetta pour les images `amd64` |
| macOS sans Docker Desktop | Colima | `brew install colima docker docker-compose` puis `colima start --cpu 4 --memory 6` |
| Ubuntu Desktop 24.04 | Docker Engine | natif, sans surcouche commerciale |
| Virtualisation active, Docker Desktop non licencié, hôte Intel ou AMD | VM VirtualBox avec Docker Engine | indépendant de Docker Desktop, aucun abonnement |

Le choix de Docker Desktop dépend du statut de l’organisation, pas de la puissance du poste. Ses conditions d’utilisation le réservent gratuitement aux entreprises de moins de 250 salariés réalisant moins de 10 M$ de chiffre d’affaires, à l’usage personnel, à l’enseignement et aux projets libres non commerciaux. Les entités publiques ne figurent pas dans la liste gratuite : une grande administration doit un abonnement payant. Cette exclusion justifie la VM. Sans virtualisation matérielle, la VM ne démarre pas non plus : `VBoxManage startvm` s’arrête sur `VT-x is not available`.

## Windows 11

1. **Firmware.** Activez VT-x (Intel) ou AMD-V, nommé SVM, dans le firmware. Le Gestionnaire des tâches, onglet Performance, affiche alors « Virtualisation : Activé ».
2. **WSL 2.** Après le bloc PowerShell ci-dessus, redémarrez. `wsl --list --verbose` affiche `Ubuntu-24.04   Stopped   2` tant que la distribution n’est pas lancée, puis `Running   2` après `wsl -d Ubuntu-24.04`.
3. **Docker Desktop.** Variante Desktop seulement : installez-le, choisissez le moteur WSL 2, puis `Settings > Resources > WSL Integration` : activez `Ubuntu-24.04`, Apply and restart.
4. **Ressources.** Créez `%UserProfile%\.wslconfig`, puis exécutez `wsl --shutdown` :

```ini
[wsl2]
memory=6GB
processors=4
```

5. **Terminal de travail.** Toutes les commandes du cours se lancent dans `wsl -d Ubuntu-24.04`, jamais dans PowerShell.
6. **Mémoire virtuelle du noyau.** Le lab J2-M1 démarre SonarQube, dont la documentation demande `vm.max_map_count` supérieur ou égal à 524288. Contrôlez la valeur vue par les conteneurs par `docker run --rm --privileged --pid=host alpine nsenter -t 1 -m -u -n -i sysctl vm.max_map_count`, qui affiche une valeur à comparer au seuil 524288. Le `docker-compose.yml` du lab désactive le contrôle de démarrage (`SONAR_ES_BOOTSTRAP_CHECKS_DISABLE`), la pile démarre donc même sous 524288. Si SonarQube refuse malgré tout, écrivez l’affectation : `docker run --rm --privileged --pid=host alpine nsenter -t 1 -m -u -n -i sysctl -w vm.max_map_count=524288`. Le réglage vise la VM du moteur, pas la distribution, et ne survit pas à `wsl --shutdown`. Commandes non vérifiées dans cet environnement.

## macOS

- Prenez Docker Desktop pour Apple Silicon (`arm64`) ou pour Intel (`amd64`) : un binaire `arm64` sur Mac Intel ne démarre pas.
- Installez Rosetta 2 par `softwareupdate --install-rosetta`, puis activez l’émulation `x86_64`/`amd64` par Rosetta dans `Settings > General`, indispensable aux deux images `amd64` citées plus haut.
- Fixez 6 Go de mémoire et 4 processeurs dans `Settings > Resources`, puis redémarrez le moteur ; les commandes du cours se lancent dans Terminal, en `zsh`, avec la même syntaxe.
- Avertissement : `mailhog/mailhog:v1.0.1` et `sonar-scanner-cli` tournent par émulation ; comptez plusieurs minutes de démarrage pour SonarQube au module J2-M1.

## Ubuntu Desktop 24.04

Le bloc d’installation a déjà posé Docker Engine. Terminez la configuration, puis vérifiez.

```bash
printf 'vm.max_map_count=524288\n' | sudo tee /etc/sysctl.d/99-sonarqube.conf
sudo sysctl --system
sysctl vm.max_map_count
docker version --format '{{.Client.Version}} / {{.Server.Version}}'
docker compose version
docker run --rm hello-world
```

Attendu : `vm.max_map_count = 524288`, deux numéros de version, `Docker Compose version v2.x`, puis `Hello from Docker!`. Le groupe `docker` n’agit qu’après réouverture de session, comme indiqué pour l’installation ; un `Cannot connect to the Docker daemon` signifie que le service ne tourne pas : `sudo systemctl enable --now docker`.

## VirtualBox

Ce chemin donne un poste Linux complet, sans Docker Desktop, sur un hôte Intel ou AMD. VirtualBox sur Mac à processeur ARM ne prend en charge que des invités `arm64`, alors que le tableau ci-dessous impose une ISO `amd64` : sur Mac ARM, passez par Docker Desktop ou Colima. Coût réel : 30 à 45 minutes de mise en place, installation d’Ubuntu Desktop comprise, et 4 à 8 Go de mémoire retirés à l’hôte selon le module. Sur Ubuntu ou Debian, installez par `sudo apt install -y virtualbox virtualbox-guest-additions-iso` ; sur Windows ou Mac Intel, l’installeur 7.2.x de virtualbox.org fournit `VBoxManage`. Dans les deux cas, `VBoxManage --version` rend la version installée.

| Paramètre de la VM | Valeur |
| --- | --- |
| Système d’exploitation | Ubuntu 24.04 Desktop, ISO (image disque au format ISO 9660) amd64 |
| Mémoire vive | 4096 Mo, jamais plus de la moitié de la mémoire de l’hôte ; 8192 Mo si l’hôte a 16 Go et que le lab J2-M1 tourne |
| Processeurs | 4 |
| Disque | VDI (VirtualBox Disk Image), 30 Go, alloué dynamiquement |
| Système | EFI (Extensible Firmware Interface) activé |
| Affichage | 128 Mo, contrôleur VMSVGA |
| Réseau | NAT (Network Address Translation) |

Le paquet du dépôt Ubuntu est souvent plus ancien que celui de virtualbox.org ; les Additions invité doivent porter la même version que l’hyperviseur. Si l’hôte est lui-même une VM, cochez Système > Processeur > Activer la virtualisation imbriquée VT-x/AMD-V, sinon la VM invitée refuse de démarrer. Après l’installation d’Ubuntu, installez les prérequis de compilation par `sudo apt install -y build-essential linux-headers-$(uname -r)`, montez l’image par Périphériques > Insérer l’image CD des Additions invité, puis lancez `sudo ./VBoxLinuxAdditions.run` depuis le point de montage. Sans ces paquets, l’installeur s’arrête sur `Please install the gcc make perl packages`. Clonez alors le dépôt dans la VM avant d’installer Docker Engine comme sur Ubuntu natif.

## Récupérer le cours

```bash
git clone https://github.com/yugmerabtene/formation-secdevops.git
cd formation-secdevops
ls
```

Attendu : `README.md  flowchart-architecture-securisee.png  jour-01.md  jour-02.md  jour-03.md  labs  prerequis.md`.

Le programme et les liens vers les trois journées sont dans `README.md` ; les fichiers de lab sont dans `labs/`. Sans Git : bouton Code > Download ZIP sur la page du dépôt, puis décompression. Les labs demandent ensuite un accès réseau pour trois usages : tirer les images Docker, télécharger la base de vulnérabilités Trivy, que `scripts/preparer.sh` de J2-M1 charge depuis le conteneur Jenkins par `docker compose exec -T jenkins trivy fs --download-db-only --no-progress`, et interroger PyPI (Python Package Index) ou OSV (Open Source Vulnerabilities) par `pip-audit`. L’espace occupé se mesure par `docker system df`, colonne `SIZE` : plusieurs gigaoctets pour l’ensemble des labs.

## Se repérer dans les labs

```text
labs/
├── lab-jour-01/   j1-m1 audit, j1-m2 pipeline, j1-m3 surveillance, j1-m3-solution
├── lab-jour-02/   j2-m1 analyse statique, j2-m2 vulnérabilités
└── lab-jour-03/   j3-m1 atelier, j3-m2 tableau de bord, j3-m3 plan
```

Le nom d’un dossier suit la convention `j<jour>-m<module>` : `j2-m1` correspond au module J2-M1. Un dossier de lab contient `docker-compose.yml` quand une pile se démarre, `outils/` pour les configurations, `app/` et `scripts/` quand le lab fournit du code et des vérifications, `donnees-*/` écrit par les conteneurs et `corrige/` quand une correction est fournie (J1-M2, J2-M2) ; `j1-m3-solution/` rejoue le lab J1-M3 complet, corrigé. `j1-m1` fait exception : `app.py`, `requirements.txt` et `outils/` à sa racine, sans `app/` ni `scripts/`.

Les livrables s’écrivent dans le dossier du lab indiqué par le module, à côté du modèle fourni ; `travail/` reçoit les essais de J2-M2. Seuls `labs/lab-jour-02/j2-m1/.gitignore` et `labs/lab-jour-02/j2-m2/.gitignore` existent : ils masquent les artefacts lourds de ces deux labs. Les livrables restent des fichiers non suivis dans `git status`, c’est le comportement attendu.

## Lancer et arrêter un lab

```bash
cd labs/lab-jour-01/j1-m3
docker compose up -d --build
docker compose ps
docker compose logs -f app    # Ctrl-C interrompt le suivi des journaux
docker compose down -v
```

`docker compose ps` doit montrer chaque service `running` ou `healthy` : `j1m3lab-app` affiche `Up (healthy)` et `j1m3lab-prometheus` affiche `Up`, relevé le 31 octobre 2026 ; le statut `healthy` vient du `healthcheck` du fichier, un service sans `healthcheck` affiche `Up` seul.

`docker compose logs -f` ne rend pas la main : appuyez sur `Ctrl-C` avant `docker compose down -v`. `down -v` arrête la pile et supprime ses volumes : exécutez-la entre deux modules, sinon les données du module précédent faussent le suivant. Un port déjà pris rend `Bind for 0.0.0.0:9090 failed: port is already allocated`, signe d’une autre pile encore démarrée ; `docker compose ps` et `ss -ltnp` nomment le processus fautif.

## Ports publiés par module

Relevé dans les fichiers du dépôt le 31 octobre 2026. Seuls les ports listés ici sont publiés sur l’hôte.

| Module | Ports sur l’hôte | Usage |
| --- | --- | --- |
| J1-M1 | 5000, 5432 | API (Application Programming Interface) et PostgreSQL, déclarés ; pile non démarrée dans le lab |
| J1-M2 | 127.0.0.1:8088, 127.0.0.1:50000 | interface Jenkins, port des agents |
| J1-M3 | 8000, 9090, 9093, 3000, 1025, 8025 | application, Prometheus, Alertmanager, Grafana, SMTP (Simple Mail Transfer Protocol) et interface MailHog |
| J2-M1 | 127.0.0.1:8099, 127.0.0.1:9000, 127.0.0.1:8089 | application, SonarQube, Jenkins |
| J2-M2, J3-M1, J3-M3 | aucun | pas de conteneur : analyse hors ligne, atelier, plan écrit |
| J3-M2 | 127.0.0.1:9101, 127.0.0.1:9190, 127.0.0.1:9193, 127.0.0.1:3101, 127.0.0.1:3300 | application, Prometheus, Alertmanager, Loki, Grafana |

Les ports préfixés par `127.0.0.1` ne sont joignables que depuis le poste ; les autres le sont depuis le réseau local. Ne les exposez jamais sur Internet : les identifiants des labs sont des valeurs de démonstration.

## Checklist finale

| Commande | Résultat attendu |
| --- | --- |
| `git --version` | `git version 2.x` |
| `curl --version` | `curl 8.x` et les protocoles pris en charge |
| `jq --version` | `jq-1.8` ou plus récent |
| `docker version` | une section Client et une section Server, sans erreur |
| `docker compose version` | `Docker Compose version v2.x` |
| `python3 --version` | `Python 3.12.x` sur Ubuntu 24.04 |
| `trivy --version` | `Version:` suivi d’un numéro, puis `Vulnerability DB` |
| `semgrep --version` | un numéro, parfois précédé d’un avis de mise à jour |
| `gitleaks version` | `8.28.0`, sans préfixe `v` |
| `hadolint --version` | `Haskell Dockerfile Linter 2.12.0` |
| `bandit --version` | `bandit 1.8.x`, puis les versions de Python |
| `pip-audit --version` | `pip-audit 2.x` |
| `docker run --rm hello-world` | `Hello from Docker!` |

## Dépannage

| Symptôme | Cause | Action |
| --- | --- | --- |
| « Virtualisation : Désactivé » dans le Gestionnaire des tâches | VT-x ou SVM désactivé | activer dans le firmware, redémarrer |
| `wsl --install` échoue | WSL 2 absent ou trop ancien | `wsl --update`, redémarrer, relancer en administrateur |
| Docker Desktop reste sur « Engine starting » | moteur WSL 2 arrêté ou intégration absente | activer l’intégration, puis restart |
| `Bind for 0.0.0.0:9090 failed` | port occupé par une autre pile | `docker compose ps`, `ss -ltnp`, puis `down -v` sur l’autre pile |
| un conteneur devient `unhealthy` puis `Exited` | mémoire insuffisante, échec applicatif ou image absente | `docker compose logs <service>`, puis mémoire du moteur ou image à corriger |
| SonarQube refuse de démarrer sur `max virtual memory areas` | `vm.max_map_count` trop bas | 524288 sur l’hôte Linux, ou `sysctl -w vm.max_map_count=524288` dans la VM du moteur |
| les images `amd64` prennent des minutes sur Apple Silicon | émulation | préférer un poste amd64, ou attendre le démarrage |
| `permission denied` sur le socket Docker | groupe `docker` non appliqué | fermer puis rouvrir la session |

## Versions cibles par module

| Module | Images |
| --- | --- |
| J1-M1 | `postgres:16-alpine`, `registry.local/notes-api:latest` (cible d’audit, non démarrée) |
| J1-M2 | `docker:29.1.3-dind`, `aquasec/trivy:0.58.1`, `j1m2-jenkins:2.580.2` construite localement |
| J1-M3 | `prom/prometheus:v2.55.1`, `prom/alertmanager:v0.27.0`, `grafana/grafana:11.3.1`, `mailhog/mailhog:v1.0.1` |
| J2-M1 | `j2m1-app:1` construite localement, `sonarqube:9.9.8-community`, `docker:29.1.3-dind`, `j2m1-jenkins:2.580.2`, `sonarsource/sonar-scanner-cli:12.3.0.4285_8.1.0` |
| J2-M2, J3-M1, J3-M3 | aucun conteneur : outils du poste et documents écrits |
| J3-M2 | `prom/prometheus:v3.5.0`, `prom/alertmanager:v0.28.1`, `grafana/grafana:12.1.0`, `grafana/loki:3.5.1` |

Les images sont épinglées par les fichiers du dépôt : ne les remplacez pas par `latest`. Le `jenkins/Dockerfile` de J2-M1 déclare `FROM j1m2-jenkins:2.580.2`, image produite par le seul lab J1-M2 : construisez J1-M2 avant J2-M1, sinon `pull access denied for j1m2-jenkins` arrête la construction. J1-M3 et J3-M2 n’embarquent pas les mêmes versions, Prometheus passant de 2.55.1 à 3.5.0 et Grafana de 11.3.1 à 12.1.0 : les règles Prometheus 2.x et 3.x ne sont pas interchangeables.

## Références

- Docker : installation d’Engine sur Ubuntu <https://docs.docker.com/engine/install/ubuntu/>, conditions d’utilisation de Docker Desktop <https://docs.docker.com/subscription/desktop-license/>, moteur WSL 2 <https://docs.docker.com/desktop/features/wsl/>
- Microsoft, installation de WSL et fichier `.wslconfig` : <https://learn.microsoft.com/windows/wsl/install> et <https://learn.microsoft.com/windows/wsl/wsl-config>
- Aqua Security, installation de Trivy : <https://trivy.dev/docs/latest/getting-started/installation/>
- SonarSource, prérequis du serveur, dont `vm.max_map_count` : <https://docs.sonarsource.com/sonarqube-server/9.9/requirements/prerequisites-and-overview/>
- Oracle, téléchargement de VirtualBox : <https://www.virtualbox.org/wiki/Downloads>
