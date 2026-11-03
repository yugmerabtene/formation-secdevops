# Formation SecDevOps — Fiche de référence

Cette fiche rassemble 36 principes SecDevOps qui ne suivent pas le découpage des huit modules, dans l'ordre où ils se présentent dans un projet.
Chaque entrée tient en deux ou trois phrases et une décision : ce qui s'automatise, ce qui bloque, ce qui se mesure.
Elle ne remplace pas un module : elle sert de mémo pour nommer un principe et le rattacher à une pratique sur Docker, Jenkins et Python/Flask.

## Sommaire

- [Flux de travail et culture](#flux-de-travail-et-culture)
- [Cycle de vie et responsabilités](#cycle-de-vie-et-responsabilités)
- [Analyse et tests de sécurité](#analyse-et-tests-de-sécurité)
- [Chaîne d'approvisionnement et artefacts](#chaîne-dapprovisionnement-et-artefacts)
- [Pipeline CI/CD comme surface d'attaque](#pipeline-cicd-comme-surface-dattaque)
- [Déploiement et risque continu](#déploiement-et-risque-continu)
- [Détection, réponse et automatisation](#détection-réponse-et-automatisation)

## Flux de travail et culture

### Lean

Le Lean supprime ce qui ne produit aucune décision : un rapport de scan que personne ne lit, une revue qui n'arrête aucun défaut. La valeur d'un contrôle se mesure aux défauts bloqués avant la production, pas au nombre de règles activées.

- **Ce que ça change** : un contrôle dont la sortie n'alimente aucune décision est supprimé, pas documenté.

### Kanban

Kanban rend visible la file des corrections et fixe une limite au travail en cours. Une vulnérabilité critique qui attend dans une colonne sans date n'a pas de propriétaire.

- **Ce que ça change** : chaque vulnérabilité porte une date d'entrée, une limite de séjour et un nom.

### Modèle de maturité DevSecOps

Un modèle de maturité décrit des pratiques observables à plusieurs niveaux et sert à choisir la prochaine étape, pas à classer une équipe. Deux modèles de l'OWASP (Open Worldwide Application Security Project) publient leur propre échelle : DSOMM (DevSecOps Maturity Model) note chaque activité sur ses niveaux d'implémentation, SAMM (Software Assurance Maturity Model) version 2.0 range chaque fonction métier sur trois niveaux. Le barème ci-dessous est une échelle de travail du cours, pas celle de ces modèles.

- **Ce que ça change** : on mesure une pratique, comme la part d'images signées ou le délai de correction, jamais une impression d'équipe.

```text
niveau  pratique              preuve attendue
0       aucun contrôle        aucune
1       contrôle manuel       revue signée à chaque livraison
2       contrôle automatisé   rapport archivé à chaque construction
3       contrôle bloquant     fusion refusée sans correction
4       contrôle mesuré       délai de correction publié
```

## Cycle de vie et responsabilités

### Cycle de vie de sécurité intégré

Chaque étape du cycle de vie porte une activité de sécurité et un critère de sortie : modèle de menace avant le code, analyse à la fusion, signature avant publication. Une activité sans critère de sortie devient une formalité.

- **Ce que ça change** : la chaîne CI/CD (Continuous Integration / Continuous Delivery, intégration et livraison continues) refuse de passer à l'étape suivante tant que le critère n'est pas rempli.

### Cycle de développement logiciel sécurisé

Le cycle de développement logiciel sécurisé rattache les pratiques à quatre familles : préparer l'organisation, protéger le logiciel, produire un logiciel sécurisé, répondre aux vulnérabilités. Le cadre SSDF (Secure Software Development Framework) du NIST (National Institute of Standards and Technology), publication SP 800-218 de février 2022, nomme ces familles et leurs tâches.

- **Ce que ça change** : chaque contrôle du pipeline se rattache à une tâche SSDF nommée, ce qui rend un audit lisible.

### Modèle de responsabilité partagée

Le fournisseur d'hébergement protège la couche matérielle et l'hyperviseur ; l'équipe applicative protège l'image, la configuration, les identités et les données. La frontière figure dans le contrat, pas dans les habitudes.

- **Ce que ça change** : chaque ligne du contrat devient un contrôle vérifiable ; ce que personne ne couvre est écrit comme risque accepté et daté.

### Fondations d'une livraison logicielle sûre

Une livraison sûre tient à quatre propriétés testables : code source revu, construction reproductible, artefact signé, déploiement autorisé par une politique. SLSA (Supply-chain Levels for Software Artifacts), dont la version courante est la 1.2, décrit la provenance qui rend ces propriétés vérifiables ; la version 1.0 date d'avril 2023.

- **Ce que ça change** : la question n'est plus « la construction est-elle propre ? » mais « quelle preuve accompagne l'artefact ? ».

### Conception de sécurité pilotée par les événements

La sécurité se déclenche sur des événements — fusion, publication d'image, avis de vulnérabilité, alerte d'exécution — et non sur un calendrier. Chaque événement déclenche une action automatisée et laisse une trace.

- **Ce que ça change** : une revue périodique ne remplace pas une réaction à l'événement ; on mesure le délai entre l'événement et l'action.

## Analyse et tests de sécurité

### SAST

SAST (Static Application Security Testing) analyse le code source sans l'exécuter et signale les motifs dangereux : concaténation SQL, appel à `eval`, secret en dur. Il voit ce que le code écrit, jamais ce que la configuration déploie.

- **Ce que ça change** : un rapport SAST n'est utile qu'avec un seuil bloquant sur les règles à fort signal ; le reste part en revue, pas en archive.

### SCA

SCA (Software Composition Analysis) compare les dépendances déclarées et celles réellement embarquées dans l'image aux bases d'avis publics : OSV (Open Source Vulnerabilities), NVD (National Vulnerability Database), avis de l'éditeur. Une dépendance transitive non déclarée n'apparaît que dans l'inventaire du contenu final.

- **Cas réel** : Log4Shell (CVE-2021-44228, décembre 2021) a touché des services dont le code ne citait jamais la bibliothèque vulnérable.

### DAST

DAST (Dynamic Application Security Testing) envoie des requêtes à l'application en fonctionnement et observe les réponses : erreurs révélatrices, injection, contrôle d'accès manquant. Il couvre la surface réellement exposée, y compris la configuration du serveur.

- **Ce que ça change** : le scan tourne avec des comptes de test par rôle ; sans eux, les contrôles d'accès ne sont pas couverts.

### IAST

IAST (Interactive Application Security Testing) instrumente l'application pendant les tests fonctionnels et relie chaque requête à la ligne de code exécutée. Le bruit baisse parce que seuls les chemins réellement parcourus sont signalés.

- **Ce que ça change** : l'IAST exige un agent dans le conteneur ; sur la pile du cours, il alourdit l'image de recette et ne couvre que les parcours testés.

### Test hybride SAST + DAST

SAST explique l'origine du défaut, DAST prouve qu'il est atteignable ; le croisement relie un `fichier:ligne` à une URL et un paramètre. Ce rapprochement reste heuristique : rien ne prouve que les deux signalements désignent le même défaut.

- **Ce que ça change** : SAST et DAST gardent chacun leur seuil bloquant ; le croisement sert à prioriser la file de correction, jamais à débloquer une fusion. Un secret en dur, invisible pour DAST, bloque sur le seul seuil SAST.

### RASP

RASP (Runtime Application Self-Protection) s'exécute dans l'application et bloque une attaque au moment de l'appel, par exemple une requête qui tente une injection. Il protège l'exécution, pas la conception : il intervient trop tard pour corriger la cause.

- **Ce que ça change** : le RASP reste un dernier recours, jamais une raison de repousser une correction.

Le tableau suivant place chaque contrôle sur l'étape où il s'exécute ; un point signifie que le contrôle n'y tourne pas.

```text
           commit   construction   image publiée   recette   production
revue      x        .              .               .         .
secrets    x        .              .               .         .
SAST       x        .              .               .         .
SCA        .        x              x               .         .
signature  .        .              x               .         .
DAST       .        .              .               x         .
IAST       .        .              .               x         .
RASP       .        .              .               .         x
```

## Chaîne d'approvisionnement et artefacts

### Gestion de versions du code

Un VCS (Version Control System) conserve le code et son histoire, mais la sécurité dépend de qui peut réécrire cette histoire et pousser sur la branche protégée. Une branche protégée sans revue obligatoire et sans signature de commit reste une convention.

- **Cas réel** : la porte dérobée de xz-utils (CVE-2024-3094, mars 2024) est passée par un compte devenu co-mainteneur depuis 2022 ; la charge vivait dans des fichiers ajoutés comme données de test, et l'historique des commits seul n'a rien révélé.

### Politique de gestion des secrets

Un secret vit dans un coffre et le pipeline l'injecte au moment de l'exécution ; il n'apparaît ni dans le dépôt, ni dans le journal de construction. La politique fixe la durée de vie, le périmètre d'usage et la procédure de rotation.

- **Cas réel** : entre le 31 janvier et le 1er avril 2021, le script d'envoi de Codecov a été modifié pour exfiltrer les variables d'environnement des chaînes d'intégration de ses clients ; la compromission a été révélée le 15 avril 2021.
- **Ce que ça change** : tout identifiant présent dans un journal est révoqué, pas seulement effacé.

### SBOM

Un SBOM (Software Bill of Materials) énumère les composants d'un artefact avec leurs versions et leurs identifiants. Deux formats normalisés coexistent : SPDX (Software Package Data Exchange, ISO/IEC 5962:2021) et CycloneDX (ECMA-424).

- **Ce que ça change** : le SBOM se génère à la construction et s'archive avec l'image. Sans inventaire, aucun de vos composants ne se rattache à une CVE (Common Vulnerabilities and Exposures, identifiant public d'une vulnérabilité).

### Signature cryptographique des artefacts

La signature d'un artefact prouve l'identité du processus de construction, pas l'intention de son auteur. Sigstore et son client cosign signent une image avec une identité OIDC (OpenID Connect) de courte durée et versent la preuve dans un journal public vérifiable.

- **Cas réel** : SolarWinds (décembre 2020) a diffusé une mise à jour signée par le certificat légitime de l'éditeur ; la signature a authentifié une construction compromise.

### Vérification de la chaîne d'approvisionnement

Vérifier signifie refuser à l'exécution un artefact dont la provenance ne correspond pas à la construction attendue, et non consulter un rapport. SLSA range cette garantie en niveaux, de la construction non tracée à la construction durcie dont la provenance est signée.

- **Ce que ça change** : la politique d'admission devient un contrôle bloquant ; un artefact non vérifié ne démarre pas, même en recette.

Le contrôle d'admission lit dans le registre l'artefact et sa provenance ; la signature seule ne dit pas à partir de quelle construction l'artefact a été produit.

- **Cas réel** : l'artefact xz-utils 5.6.1 (CVE-2024-3094, mars 2024) contenait du code absent du dépôt Git ; seule une provenance liée au commit attendu refuse cet artefact.

```text
commit --> construction --> SBOM --> signature --> registre
                                                       |
                                                       v
                                             contrôle d'admission
                                                       |
                                                       v
                                             déploiement ou refus
```

### Risque fournisseur et remédiation

Un fournisseur se traite comme une dépendance : on suit ses avis, on teste ses mises à jour et on garde une solution de remplacement. Le risque se mesure au délai entre la publication de l'avis et la version déployée.

- **Ce que ça change** : un VEX (Vulnerability Exploitability eXchange) permet à un éditeur de déclarer qu'une vulnérabilité publiée ne l'affecte pas, ce qui évite une correction inutile.

### Traiter une CVE PHP critique de bout en bout

CVE-2024-4577, enregistrée le 9 juin 2024, permet une injection d'arguments dans `php-cgi` sous Windows lorsque le serveur emploie certaines pages de code ; elle touche 8.1.\* avant 8.1.29, 8.2.\* avant 8.2.20 et 8.3.\* avant 8.3.8. La pile du cours, sous Linux avec Python/Flask, n'est pas concernée : c'est la méthode qui se transpose. Le traitement tient en six étapes, et l'inventaire décide du reste.

- **Cas réel** : les correctifs 8.1.29, 8.2.20 et 8.3.8 sont sortis le 6 juin 2024, avant l'enregistrement ; la date de l'avis ne fixe donc pas le délai de correction.
- **Ce que ça change** : le délai de réponse dépend de l'inventaire disponible, pas de la gravité annoncée.

```text
1  avis        2024-06 : injection d'arguments dans php-cgi sous Windows
2  inventaire  SBOM : php-cgi présent ? quelle version ?
3  exposition  hébergement Windows en mode CGI ?
4  correctif   8.1.29, 8.2.20 ou 8.3.8
5  preuve      version installée relevée, test de non-régression vert
6  suivi       délai avis -> correctif mesuré, règle de détection ajoutée
```

## Pipeline CI/CD comme surface d'attaque

### Vecteurs d'attaque d'un pipeline CI

Un pipeline exécute du code venu d'une demande de fusion : fichier de construction modifié, test qui lit les variables d'environnement, dépendance installée au premier lancement. Chaque étape est une entrée non fiable qui hérite des droits de la tâche.

- **Cas réel** : CVE-2024-23897 (janvier 2024) laissait lire des fichiers du contrôleur Jenkins par l'interface en ligne de commande ; corrigée en 2.442, LTS 2.426.3 et 2.440.1.

```text
demande de fusion --> [tâche sans secret] --> construction, SAST, SCA
                              |
                              v
                    [tâche de publication]  secret + signature
                              |
                              v
                           registre --> [contrôle d'admission] --> déploiement
```

### Stratégie d'optimisation de la sécurité du CI

Trois leviers, dans cet ordre : réduire ce que la tâche peut atteindre, réduire ce qu'elle peut lire, journaliser ce qu'elle fait. Une tâche qui construit une demande de fusion n'a besoin ni du secret de publication, ni d'un accès au registre.

- **Ce que ça change** : le secret de publication n'existe que dans la tâche de publication ; ailleurs, il est absent et non « protégé ».

### Sécurité du CD et contrôles de déploiement cloud

Le déploiement transforme un artefact en état observé ; les contrôles portent donc sur l'état cible, pas sur la promesse du pipeline. Cet état comprend les identités et les règles réseau, que le fournisseur ne corrige pas à votre place. On décrit l'état, on le compare à une politique, on refuse l'écart.

- **Ce que ça change** : sur la pile du cours, le contrôle lit la configuration rendue par `docker compose config` et la compare à une politique versionnée.

### Architecture de confiance zéro du pipeline

La confiance zéro (zero trust), décrite dans le NIST SP 800-207 (août 2020), refuse la confiance liée à la position réseau : chaque composant prouve son identité et son droit à chaque appel. Un agent Jenkins joint le contrôleur avec un secret qui lui est propre et qui se révoque, jamais un mot de passe partagé.

- **Ce que ça change** : une tâche compromise ne peut pas se faire passer pour une autre ; la compromission reste locale.

### Durcissement de l'hôte et des conteneurs

Les référentiels CIS (Center for Internet Security) donnent les contrôles attendus sur l'hôte et sur le moteur de conteneurs. Chaque contrôle nomme la valeur attendue et la commande qui la relève ; sans la commande, il n'existe pas.

- **Ce que ça change** : un contrôle CIS qu'aucune commande n'exécute rejoint la liste datée des risques acceptés, au lieu de rester dans une grille de conformité.

### Infrastructure as Code

Un fichier décrit l'infrastructure, donc il se relit, se teste et se versionne comme du code. Sa sécurité se contrôle par une politique exécutable, pas par une relecture humaine.

- **Ce que ça change** : un Dockerfile est du code d'infrastructure ; il passe un analyseur statique, par exemple `hadolint`, avant la revue.

## Déploiement et risque continu

### Gestion continue du risque de déploiement

Chaque déploiement porte un risque que l'on peut nommer : population exposée, surface modifiée, réversibilité. Le risque se traite par la taille du lot et par la vitesse de retour arrière, pas par une approbation supplémentaire.

- **Ce que ça change** : on mesure le délai de retour arrière et le taux d'échec par déploiement ; une approbation ne mesure rien.

### Validation de sécurité par déploiement canari

Un déploiement canari expose une fraction du trafic à la nouvelle version et compare des signaux de santé et de sécurité avant la généralisation. Ces signaux se choisissent d'avance : erreurs, latence, refus d'autorisation.

- **Ce que ça change** : sans seuil d'abandon écrit avant le déploiement, le canari ne décide rien ; la clôture ne fixe aucun seuil, elle documente les seuils révisés.

```text
étape          part du trafic   critère d'abandon (valeurs d'exemple)
préparation    0 %              retour arrière testé en recette
canari         1 %              erreurs 5xx > 1 % pendant 5 min
canari élargi  25 %             latence p95 (95e centile) > 800 ms
généralisation 100 %            retour arrière automatique sinon
clôture        100 %            aucun : seuils révisés, incident documenté
```

### Mécanisme de retour arrière automatisé

Le retour arrière doit être une commande exécutée en une minute, testée en recette et déclenchable par une alerte. Il échoue le plus souvent sur une migration de schéma non réversible.

- **Ce que ça change** : une livraison qui exige une migration irréversible passe par une étape en deux temps, avec une version compatible des deux côtés.

## Détection, réponse et automatisation

### Détection et réponse à l'exécution

La détection à l'exécution observe le comportement — processus lancé, fichier ouvert, connexion sortante — et non la signature d'un fichier. Sous Linux, Falco applique des règles aux appels système et alerte sur un shell ouvert dans un conteneur.

- **Ce que ça change** : la règle de détection se versionne et se teste comme du code, avec un cas qui doit alerter et un cas qui doit rester silencieux.

```text
1  journal               collecte normalisée de l'hôte et des conteneurs
2  corrélation           deux sources relient le même identifiant
3  alerte                règle versionnée, testée par un cas qui doit alerter
4  triage                faux positif écarté, escalade sinon
5  confinement           action réversible : isoler, révoquer, bloquer
6  retour d'expérience   procédure et seuils ajustés, règle rejouée
```

### Recherche de menaces et automatisation de la réponse à incident

La recherche de menaces part d'une hypothèse d'attaquant et la confronte aux journaux disponibles. La réponse s'automatise sur les actions réversibles : isoler un conteneur, révoquer un jeton, bloquer une adresse.

- **Ce que ça change** : on mesure le MTTD (Mean Time To Detect) et le MTTR (Mean Time To Repair, temps moyen de réparation) par type d'alerte, jamais en moyenne globale.

### SIEM

SIEM (Security Information and Event Management) centralise les journaux, les normalise et corrèle les événements de sources différentes. Un journal non collecté ne peut pas être corrélé après l'incident.

- **Ce que ça change** : la collecte s'écrit comme du code — source, format, rétention, règle de corrélation — et se verse au dépôt.

### SOAR

SOAR (Security Orchestration, Automation and Response) exécute des procédures qui enchaînent les outils : enrichir une alerte, ouvrir une tâche, isoler un service. La procédure automatise une décision déjà écrite ; elle ne la prend pas.

- **Ce que ça change** : toute action irréversible, comme la suppression de données ou le blocage d'un compte administrateur, reste soumise à une validation humaine.

### Automatisation de la sécurité pilotée par l'IA

L'IA (intelligence artificielle) s'emploie sur trois tâches : trier les alertes, regrouper les vulnérabilités d'une même cause, proposer un cas de test de non-régression. Le gain vient du tri, pas de la découverte.

- **Ce que ça change** : une suggestion de LLM (Large Language Model) n'entre dans le pipeline que si un test la valide ; les journaux envoyés au modèle sont filtrés.

### DevSecOps agentique

Un agent exécute des actions dans la chaîne — lire un rapport, ouvrir une correction, relancer une construction — et se traite comme un compte de service. Droits minimaux, journal de ses appels, révocation possible à tout moment.

- **Ce que ça change** : un agent autorisé à modifier la politique de sécurité annule le contrôle qu'elle porte ; son périmètre s'arrête à la production de propositions.
