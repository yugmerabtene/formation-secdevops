• **Shift Left (Glissement à gauche)** : C'est le principe fondateur du DevSecOps. Il consiste à déplacer les tests de sécurité le plus tôt possible dans le cycle de développement (à « gauche » sur la frise chronologique : dès la phase d'écriture du code, de la conception et de la revue de code). Au lieu de subir un audit de sécurité en fin de projet, les failles sont détectées au plus vite, quand leur correction coûte le moins cher.

• **Shift Right (Glissement à droite)** : Complémentaire du Shift Left, il s'agit de maintenir la sécurité en production et en exploitation : supervision, détection d'intrusion, gestion des vulnérabilités en continu, tests de résilience et réponse à incident. La sécurité ne s'arrête pas au déploiement.

• **« Security as Code » (sécurité as code)** : Les politiques, contrôles et tests de sécurité sont décrits sous forme de code versionné (Infrastructure as Code sécurisée, politiques OPA/Rego, règles SAST/DAST, pipelines de conformité). Cela rend la sécurité reproductible, auditable et automatisable.

• **Automatisation dans la CI/CD** : Intégration d'outils de sécurité directement dans le pipeline : analyse statique (SAST), analyse dynamique (DAST), analyse des dépendances (SCA), scan de conteneurs et d'images, analyse des secrets, tests d'infrastructure as code (IaC scanning). Chaque commit déclenche des contrôles automatiques.

• **Défense en profondeur** : Multiplication des couches de protection (code, dépendances, build, artefact, déploiement, runtime, réseau, identité) plutôt qu'un contrôle unique en bout de chaîne.

• **Culture et collaboration** : DevSecOps casse le silo entre développement, opérations et sécurité. La sécurité devient la responsabilité partagée de toutes les équipes, avec formation, « security champions » et boucles de feedback rapides.

• **Conformité et traçabilité** : Les contrôles automatisés produisent des preuves d'audit continues (SBOM, journaux, rapports de scan), facilitant la conformité réglementaire (ISO 27001, RGPD, SOC 2, etc.).

• **Gestion des risques et priorisation** : Toutes les alertes ne se valent pas ; le DevSecOps s'appuie sur la criticité, l'exploitabilité et le contexte métier pour prioriser les corrections (scoring CVSS, EPSS, politiques de « break the build » sur les seuils critiques).

• **Supply chain security** : Sécurisation de la chaîne d'approvisionnement logicielle : vérification des dépendances, signature des artefacts (Sigstore/cosign), SBOM, protection contre les attaques de type SolarWinds ou Log4Shell.

Souhaitez-vous que je poursuive avec une section sur les outils concrets (SAST, DAST, SCA, secrets scanning, etc.), un exemple de pipeline DevSecOps étape par étape, ou les bénéfices/limites de la démarche ?
