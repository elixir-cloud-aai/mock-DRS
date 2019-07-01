##### BASE IMAGE #####
FROM ubuntu:16.04

##### METADATA #####
LABEL base.image="ubuntu:16.04"
LABEL version="1.1"
LABEL software="mock-DRS"
LABEL software.version="1.0"
LABEL software.description="Microservice implementing the Global Alliance for Genomics and Health (GA4GH) Data Repository Schema (DRS) API specification."
LABEL software.website="https://github.com/elixir-europe/mock-DRS"
LABEL software.documentation="https://github.com/elixir-europe/mock-DES"
LABEL software.license="https://github.com/elixir-europe/mock-DRS/blob/master/LICENSE"
LABEL software.tags="General"
LABEL maintainer.lab="Zavolan Lab"
LABEL maintainer.license="https://spdx.org/licenses/Apache-2.0"

## Install system resources & dependencies
RUN apt-get update \
  && apt-get install -y build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev zlib1g-dev openssl libffi-dev python3-dev python3-setuptools git wget curl nodejs

## Install Python
RUN wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz \
  && tar xJf Python-3.6.0.tar.xz \
  && cd Python-3.6.0 \
  && ./configure \
  && make altinstall \
  && ln -s /Python-3.6.0/python /usr/local/bin \
  && cd .. \
  && python -m pip install --upgrade pip setuptools wheel virtualenv

## Copy sepc files
COPY ./ /specs

## install requirememnts
CMD pip install -r requirements.txt

## Run connexion stub in the specs folder to make a mock
CMD cd /specs
## run a stub of the mock service using connexion
## CMD connexion run --stub -d -v specs schema.data_repository_service.cd0186f.openapi.yaml
