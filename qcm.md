Le DevSecOps consiste à intégrer la sécurité dès le départ et à chaque étape du cycle de développement logiciel (CI/CD). L'objectif est de casser le silo traditionnel où la sécurité n'intervenait qu'à la toute fin, juste avant la mise en production. [1] (https://www.stephane-robert.info/docs/devops/fondamentaux/devsecops/), [2] (https://elearning.rousseltm.fr/article/fr/devsecops-securiser-la-chaine-logicielle-de-bout-en-bout-380)
Voici l'explication claire et synthétique de tous les concepts clés de cette démarche :

🔄 Les Principes Fondamentaux

• Shift Left (Glissement à gauche) : C'est le principe fondateur du DevSecOps. Il consiste à déplacer les tests de sécurité le plus tôt possible dans le cycle de développement (à "gauche" sur la frise chronologique : dès la phase d'écriture du code). Corriger une faille au moment où le développeur tape son code coûte infiniment moins cher et prend moins de temps que de la corriger une fois l'application déployée. [1] (https://blent.ai/lexique/devsecops), [2] (https://www.stephane-robert.info/docs/devops/fondamentaux/devsecops/)
• Blocking Gate (Barrière bloquante) : C'est un mécanisme automatisé dans la chaîne CI/CD qui interrompt immédiatement le pipeline (le déploiement ou la fusion du code) si un seuil de sécurité n'est pas respecté (par exemple : détection d'une vulnérabilité critique ou d'un mot de passe exposé). [1] (https://www.stephane-robert.info/docs/devops/fondamentaux/devsecops/)
• Policy as Code (La conformité par le code) : Consiste à définir les règles de sécurité, de conformité et de gouvernance sous forme de fichiers de code (fichiers YAML, Rego, etc.). Cela permet d'automatiser et de versionner la validation des infrastructures (comme bloquer un serveur cloud si son accès est configuré comme "public par défaut"). [1] (https://elearning.rousseltm.fr/article/fr/devsecops-securiser-la-chaine-logicielle-de-bout-en-bout-380), [2] (https://wearedevops.fr/roles/devsecops/concepts)

🔍 Les Outils de Test (SAST, SCA, DAST)

Pour appliquer le Shift Left, on utilise trois types de scans complémentaires tout au long de la chaîne :

Concept / Outil	Ce qu'il fait	Quand l'exécuter ?	Exemple concret
SAST (Static Application Security Testing)	Analyse le code source "à froid" sans l'exécuter pour trouver des erreurs de logique.	Pendant le développement ou à la soumission du code.	Détecter que l'application accepte des injections SQL ou contient une clé API écrite en dur.
SCA (Software Composition Analysis)	Analyse le code tiers et les librairies open-source importées pour y déceler des failles connues.	Dès la construction (Build) de l'application.	Alerter que la version d'une bibliothèque de log importée contient une faille critique (type Log4Shell).
DAST (Dynamic Application Security Testing)	Analyse l'application "à chaud" (en cours d'exécution) en simulant des attaques externes.	Sur un environnement de staging ou de pré-production.	Tester si les formulaires web ou les APIs résistent à des attaques de type Cross-Site Scripting (XSS).


📦 La Sécurité de la Supply Chain (Chaîne d'approvisionnement)

• SBOM (Software Bill of Materials) : C'est la "liste des ingrédients" complète de votre logiciel. Il s'agit d'un fichier standardisé (formats CycloneDX ou SPDX) généré automatiquement qui recense absolument toutes les dépendances, sous-dépendances et composants utilisés dans l'application. [1] (https://www.youtube.com/watch?v=z7mBMbEben8), [2] (https://wearedevops.fr/roles/devsecops/concepts)
• SLSA (Supply-chain Levels for Software Artifacts) : Prononcé "Salsa", c'est un référentiel de sécurité (framework) de l'industrie. Il définit des niveaux d'exigence croissants pour garantir qu'un morceau de code ou qu'un conteneur n'a pas été modifié ou falsifié entre le moment où le développeur l'a écrit et le moment où il est déployé (traçabilité et intégrité de la chaîne de build). [1] (https://blent.ai/lexique/devsecops), [2] (https://wearedevops.fr/roles/devsecops/concepts)
• Dependency Confusion (Confusion de dépendances) : C'est un type d'attaque informatique très astucieux. Un attaquant publie un package malveillant sur un registre public (comme npm ou PyPI) en lui donnant exactement le même nom qu'une bibliothèque interne et privée de votre entreprise. Si vos outils de build sont mal configurés, ils risquent de télécharger la version publique piratée à la place de votre version interne.

🔐 Authentification & Identité

• OIDC (OpenID Connect) : C'est un protocole d'authentification moderne basé sur OAuth 2.0. En DevSecOps, il est massivement utilisé pour éliminer le besoin de stocker des mots de passe ou des clés secrètes à long terme dans vos pipelines CI/CD. Par exemple, GitHub Actions peut utiliser OIDC pour s'authentifier de manière éphémère et sécurisée auprès d'AWS ou d'Azure afin de déployer des ressources. [1] (https://wearedevops.fr/roles/devsecops/concepts)

