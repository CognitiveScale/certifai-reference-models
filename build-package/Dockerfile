FROM registry.access.redhat.com/ubi8/python-36

LABEL release=1 \
  name="cortex-certifai-reference-model-server" \
  vendor="CognitiveScale" \
  version=1 \
  summary="Cortex Certifai Reference Model Server" \
  description="Reference Model Server for Cognitive Scale's Cortex Certifai" \
  com.cognitivescale.license_terms="https://www.cognitivescale.com/legal-information/"

USER root
RUN yum -y update-minimal --security --sec-severity=Important --sec-severity=Critical
USER default

COPY licenses /licenses
COPY dist/cortex-certifai-reference-model-server-*.zip \
       /tmp/

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir \
     $(find /tmp -name cortex-certifai-reference-model-server-*.zip)

USER root
RUN mkdir -p /app && chown -R default /app
USER default

EXPOSE 5111
CMD ["startCertifaiModelServer"]