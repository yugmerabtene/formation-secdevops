# Formation SecDevOps

Formation de trois jours (18 heures) pour découvrir et adopter une culture
SecDevOps : automatiser les tests de sécurité dans un processus agile,
surveiller et améliorer en continu la sécurité des architectures DevOps,
implémenter des contrôles de sécurité dès les premières étapes du cycle de
développement.

## Objectifs pédagogiques

- Automatiser les tests de sécurité dans un processus agile.
- Surveiller et améliorer en continu la sécurité des architectures DevOps.
- Implémenter des contrôles de sécurité dès les premières étapes du cycle de
  développement.

## Public et prérequis

Développeurs, ingénieurs DevOps et SRE, QA, ingénieurs sécurité, chefs de projet
techniques. Niveau intermédiaire : bases du développement, Git, Linux, CI/CD et
conteneurs. Des notions de sécurité applicative sont un plus.

Le poste de travail doit permettre d'exécuter Docker en local : voir
[prerequis.md](prerequis.md).

## Programme

### Jour 1 — Introduction et principes de SecDevOps (6 heures)

Cours : [jour-01.md](jour-01.md)

| Module | Durée | Contenu |
| --- | --- | --- |
| J1-M1 Introduction à SecDevOps et sécurité agile | 1 h 30 | Principes DevOps et extension vers SecDevOps. Pourquoi intégrer la sécurité dans les environnements DevOps. Étude de cas : analyse d'une faille de sécurité dans un environnement agile. |
| J1-M2 Contrôles de sécurité dans les pipelines DevOps | 2 h | Identification des points critiques à sécuriser. Meilleures pratiques pour intégrer des contrôles de sécurité. Lab : mise en œuvre de contrôles de sécurité dans un pipeline fictif. |
| J1-M3 Création et surveillance d'une architecture sécurisée | 2 h 30 | Concevoir une architecture sécurisée dès le départ. Surveillance continue et gestion des alertes de sécurité. Lab : simulation de la surveillance d'un système. |

### Jour 2 — Outils et automatisation des tests de sécurité (6 heures)

Cours : [jour-02.md](jour-02.md)

| Module | Durée | Contenu |
| --- | --- | --- |
| J2-M1 Automatisation des tests de sécurité | 3 h | Outils d'analyse de sécurité : OWASP ZAP, SonarQube, Trivy. Automatisation des tests statiques et dynamiques dans les pipelines CI/CD. Lab : intégration de tests de sécurité automatisés dans un pipeline Jenkins. |
| J2-M2 Gestion des vulnérabilités et remédiations | 3 h | Détection et suivi des vulnérabilités avec des outils comme Snyk. Résolution des problèmes identifiés et mise à jour continue. Lab : analyse des vulnérabilités d'une application existante. |

### Jour 3 — Culture SecDevOps et gestion continue (6 heures)

Cours : [jour-03.md](jour-03.md)

| Module | Durée | Contenu |
| --- | --- | --- |
| J3-M1 Culture SecDevOps et sensibilisation des équipes | 2 h | Promouvoir une culture de sécurité au sein des équipes DevOps. Collaboration entre développeurs, équipes QA et sécurité. Lab : ateliers collaboratifs sur la sécurité intégrée. |
| J3-M2 Approches avancées pour SecDevOps | 2 h 30 | Intégration de l'intelligence artificielle dans les tests de sécurité. Analyse des journaux et prévention des menaces en temps réel. Lab : mise en place d'un tableau de bord de surveillance. |
| J3-M3 Bonnes pratiques pour un développement agile sécurisé | 1 h 30 | Implémentation des principes du Shift-left Security. Planification des mises à jour et maintenance continue. Lab : élaboration d'un plan de sécurité pour un projet agile. |

## Labs

Les lab se font sur un poste de travail, avec Docker en local, Jenkins en
conteneur et une application Python/Flask. Ils s'enchaînent d'un module au
suivant : le livrable d'un lab sert au lab ou au module suivant.

| Journée | Dossier |
| --- | --- |
| Jour 1 | [labs/lab-jour-01](labs/lab-jour-01) — J1-M1, J1-M2, J1-M3 et le corrigé de J1-M3 |
| Jour 2 | [labs/lab-jour-02](labs/lab-jour-02) — J2-M1, J2-M2 |
| Jour 3 | [labs/lab-jour-03](labs/lab-jour-03) — J3-M1, J3-M2, J3-M3 |
