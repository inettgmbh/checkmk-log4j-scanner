FROM ghcr.io/graalvm/graalvm-ce:latest

RUN microdnf --enablerepo ol8_codeready_builder install maven
RUN gu install native-image

ARG USER_ID
ARG GROUP_ID
RUN groupadd -g ${GROUP_ID} builder
RUN useradd -m -u ${USER_ID} -g ${GROUP_ID} builder

USER builder
