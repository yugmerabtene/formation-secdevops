# Jenkins du lab J1-M2 : Jenkins LTS, clients Docker et outils de contrôle.
# Les versions sont figées par des arguments de construction.
FROM docker:29.1.3 AS dockercli
FROM aquasec/trivy:0.58.1 AS trivy

FROM jenkins/jenkins:2.580.2-jdk21

USER root

ARG GITLEAKS_VERSION=8.28.0
ARG HADOLINT_VERSION=2.12.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*

COPY --from=dockercli /usr/local/bin/docker /usr/local/bin/docker
COPY --from=dockercli /usr/local/libexec/docker/cli-plugins/docker-buildx \
    /usr/local/libexec/docker/cli-plugins/docker-buildx
COPY --from=trivy /usr/local/bin/trivy /usr/local/bin/trivy

RUN curl -fsSL "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz" \
        | tar -xz -C /usr/local/bin gitleaks \
    && curl -fsSL -o /usr/local/bin/hadolint "https://github.com/hadolint/hadolint/releases/download/v${HADOLINT_VERSION}/hadolint-Linux-x86_64" \
    && chmod 0755 /usr/local/bin/gitleaks /usr/local/bin/trivy /usr/local/bin/hadolint

RUN jenkins-plugin-cli --plugins workflow-aggregator credentials-binding

USER jenkins
