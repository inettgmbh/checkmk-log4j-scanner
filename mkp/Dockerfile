FROM debian:11

RUN apt-get update
RUN apt-get install -yV git python3 python3-pip
RUN python3 -m pip install --upgrade pip
ARG PYTHON_MKP_REPO
RUN pip install ${PYTHON_MKP_REPO}
