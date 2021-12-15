FROM ghcr.io/graalvm/graalvm-ce:latest

RUN microdnf --enablerepo ol8_codeready_builder install maven

ARG USER_ID
ARG GROUP_ID
RUN groupadd -u ${GROUP_ID} builder
RUN useradd -m -u ${USER_ID} -g ${GROUP_ID} builder

USER builder
