# Jenkins du lab J2-M1 : reprend l'image du jour 1 et ajoute deux analyseurs.
# - sonar-scanner : copié depuis l'image officielle, avec son JRE embarqué ;
# - semgrep : installé dans un environnement virtuel dédié, version figée.
FROM sonarsource/sonar-scanner-cli:12.3.0.4285_8.1.0 AS scanner
FROM j1m2-jenkins:2.580.2

USER root

ARG SEMGREP_VERSION=1.168.0

COPY --from=scanner /opt/sonar-scanner /opt/sonar-scanner

RUN python3 -m venv /opt/semgrep \
    && /opt/semgrep/bin/pip install --no-cache-dir "semgrep==${SEMGREP_VERSION}" \
    && ln -s /opt/semgrep/bin/semgrep /usr/local/bin/semgrep \
    && ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/local/bin/sonar-scanner

USER jenkins
