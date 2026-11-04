## 🔄 Principes fondamentaux

| Terme | Signification / Définition |
|---|---|
| **Shift Left** | Déplacer les contrôles de sécurité le plus tôt possible dans le cycle (conception, code, revue). |
| **Shift Right** | Maintenir la sécurité en production/exploitation (supervision, détection, réponse à incident). |
| **Security as Code** | Décrire politiques et contrôles de sécurité sous forme de code versionné et automatisable. |
| **Defense in Depth** | Défense en profondeur : multiplier les couches de protection. |
| **Break the Build** | Bloquer automatiquement le pipeline si un seuil de sécurité critique est franchi. |
| **Fail Fast** | Détecter et signaler une faille au plus vite pour corriger à moindre coût. |
| **Shared Responsibility** | La sécurité devient la responsabilité partagée de toutes les équipes (Dev, Ops, Sec). |
| **Continuous Security** | Sécurité continue, intégrée à chaque étape, pas un audit ponctuel. |
| **Security Champions** | Référents sécurité intégrés dans les équipes de développement. |

---

## 🧪 Types de tests et analyses de sécurité

| Acronyme | Signification | Rôle |
|---|---|---|
| **SAST** | Static Application Security Testing | Analyse statique du code source (sans exécution). |
| **DAST** | Dynamic Application Security Testing | Analyse dynamique de l'application en exécution (boîte noire). |
| **IAST** | Interactive Application Security Testing | Analyse interactive combinant instrumentation runtime et tests. |
| **SCA** | Software Composition Analysis | Analyse des dépendances et bibliothèques tierces (vulnérabilités, licences). |
| **RASP** | Runtime Application Self-Protection | Protection de l'application à l'exécution, détection d'attaques en temps réel. |
| **SAST/DAST/IAST/SCA** | (voir ci-dessus) | Les 4 familles majeures d'outils de test de sécurité. |
| **Secret Scanning** | — | Détection de secrets (clés, tokens, mots de passe) dans le code et les dépôts. |
| **IaC Scanning** | Infrastructure as Code Scanning | Analyse des fichiers d'infrastructure as code (Terraform, K8s…) pour détecter les mauvaises configurations. |
| **Container Scanning** | — | Scan des images de conteneurs (vulnérabilités, couches, secrets). |
| **Fuzzing** | Fuzz Testing | Tests par injection de données aléatoires pour trouver des failles. |
| **Pen Testing** | Penetration Testing | Test d'intrusion manuel ou automatisé. |
| **Threat Modeling** | — | Modélisation des menaces dès la conception (ex. STRIDE). |

---

## 🔐 Acronymes de sécurité et de gestion des risques

| Acronyme | Signification | Rôle |
|---|---|---|
| **CVE** | Common Vulnerabilities and Exposures | Identifiant unique d'une vulnérabilité publique. |
| **CWE** | Common Weakness Enumeration | Classification des types de faiblesses logicielles. |
| **CVSS** | Common Vulnerability Scoring System | Score de gravité d'une vulnérabilité (0–10). |
| **EPSS** | Exploit Prediction Scoring System | Probabilité d'exploitation d'une CVE. |
| **SBOM** | Software Bill of Materials | Inventaire des composants logiciels et dépendances. |
| **SCA** | (voir ci-dessus) | — |
| **STRIDE** | Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege | Méthode de modélisation des menaces. |
| **OWASP** | Open Worldwide Application Security Project | Référentiel et projets de sécurité applicative (ex. OWASP Top 10). |
| **MITRE ATT&CK** | — | Base de connaissances des tactiques et techniques d'attaque. |
| **CSPM** | Cloud Security Posture Management | Gestion de la posture de sécurité cloud. |
| **CWPP** | Cloud Workload Protection Platform | Protection des charges de travail cloud. |
| **SIEM** | Security Information and Event Management | Collecte et corrélation des journaux de sécurité. |
| **SOC** | Security Operations Center | Centre opérationnel de sécurité (surveillance). |
| **SOAR** | Security Orchestration, Automation and Response | Automatisation de la réponse à incident. |
| **IDS / IPS** | Intrusion Detection / Prevention System | Détection / prévention d'intrusion. |
| **WAF** | Web Application Firewall | Pare-feu applicatif web. |
| **IAM** | Identity and Access Management | Gestion des identités et des accès. |
| **MFA** | Multi-Factor Authentication | Authentification multifacteur. |
| **RBAC** | Role-Based Access Control | Contrôle d'accès basé sur les rôles. |
| **Zero Trust** | — | Modèle « ne jamais faire confiance, toujours vérifier ». |
| **mTLS** | Mutual TLS | Authentification mutuelle par certificats TLS. |
| **PKI** | Public Key Infrastructure | Infrastructure à clés publiques. |

---

## ⚙️ CI/CD et chaîne d'approvisionnement

| Acronyme | Signification | Rôle |
|---|---|---|
| **CI** | Continuous Integration | Intégration continue (build, tests automatisés). |
| **CD** | Continuous Delivery / Deployment | Livraison / déploiement continu. |
| **Pipeline** | — | Chaîne automatisée build → test → scan → déploiement. |
| **DevSecOps** | Development, Security, Operations | Intégration de la sécurité dans le DevOps. |
| **SBOM** | (voir ci-dessus) | — |
| **SLSA** | Supply-chain Levels for Software Artifacts | Framework de niveaux de sécurité de la chaîne logicielle. |
| **Sigstore / Cosign** | — | Outils de signature et vérification d'artefacts. |
| **SCM** | Source Code Management | Gestion de code source (Git…). |
| **IaC** | Infrastructure as Code | Infrastructure décrite en code (Terraform, Ansible…). |
| **GitOps** | — | Gestion déclarative de l'infrastructure via Git. |
| **Artifact Registry** | — | Dépôt d'artefacts (images, packages) sécurisé. |

---

## ☁️ Cloud, conteneurs et orchestration

| Acronyme | Signification | Rôle |
|---|---|---|
| **K8s** | Kubernetes | Orchestrateur de conteneurs. |
| **CSPM** | (voir ci-dessus) | — |
| **CWPP** | (voir ci-dessus) | — |
| **CNAPP** | Cloud-Native Application Protection Platform | Plateforme unifiée de protection cloud-native. |
| **OPA** | Open Policy Agent | Moteur de politiques (Rego) pour l'admission et la conformité. |
| **PSP / PSA** | Pod Security Policy / Pod Security Admission | Contrôles de sécurité des pods Kubernetes. |
| **Network Policy** | — | Règles de segmentation réseau dans Kubernetes. |
| **Secrets Management** | — | Gestion sécurisée des secrets (Vault, SOPS…). |

---

## 📜 Conformité, normes et frameworks

| Acronyme | Signification | Rôle |
|---|---|---|
| **ISO 27001** | — | Norme de management de la sécurité de l'information. |
| **RGPD / GDPR** | Règlement Général sur la Protection des Données | Conformité données personnelles. |
| **SOC 2** | System and Organization Controls 2 | Norme d'audit de sécurité des services. |
| **NIST** | National Institute of Standards and Technology | Référentiels (ex. NIST SSDF, CSF). |
| **SSDF** | Secure Software Development Framework (NIST) | Cadre de développement logiciel sécurisé. |
| **PCI DSS** | Payment Card Industry Data Security Standard | Norme de sécurité des données de cartes bancaires. |
| **HIPAA** | Health Insurance Portability and Accountability Act | Conformité santé (US). |
| **ANSSI** | Agence Nationale de la Sécurité des Systèmes d'Information | Recommandations et guides sécurité (France). |
| **EBIOS RM** | Expression des Besoins et Identification des Objectifs de Sécurité – Risk Manager | Méthode d'analyse de risques (ANSSI). |

---

## 🧠 Culture et organisation

| Terme | Signification |
|---|---|
| **DevSecOps** | Development + Security + Operations. |
| **Silo** | Cloisonnement organisationnel que le DevSecOps cherche à casser. |
| **Feedback Loop** | Boucle de rétroaction rapide entre équipes. |
| **Security Champions** | Référents sécurité dans les équipes Dev. |
| **Threat Modeling** | Modélisation des menaces dès la conception. |
| **Post-mortem / RCA** | Root Cause Analysis : analyse d'incident sans blâme. |
| **Blameless Culture** | Culture sans recherche de culpabilité (apprentissage). |

---

## 📌 En résumé (les essentiels à retenir)

- **Principes** : Shift Left, Shift Right, Security as Code, Defense in Depth, Break the Build, Shared Responsibility.
- **Tests** : SAST, DAST, IAST, SCA, Secret Scanning, IaC Scanning, Container Scanning, RASP, Fuzzing, Pen Testing.
- **Risques** : CVE, CWE, CVSS, EPSS, SBOM, OWASP, STRIDE, MITRE ATT&CK.
- **CI/CD & supply chain** : CI, CD, IaC, GitOps, SLSA, Sigstore/Cosign, Artifact Registry.
- **Cloud** : CSPM, CWPP, CNAPP, OPA, K8s.
- **Conformité** : ISO 27001, RGPD, SOC 2, NIST SSDF, PCI DSS, ANSSI/EBIOS RM.
- **Culture** : Security Champions, Feedback Loop, Blameless Culture.
