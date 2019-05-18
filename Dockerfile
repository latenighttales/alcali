FROM python:3.7-stretch
# Upgrade System and Install dependencies
RUN apt-get update && \
  apt-get upgrade -y -o DPkg::Options::=--force-confold && \
  apt-get install -y -o DPkg::Options::=--force-confold netcat
RUN useradd -u 2000 -ms /bin/bash -d /opt/alcali alcali
USER alcali
ENV PYTHONUNBUFFERED=1 PATH="/opt/alcali/.local/bin:${PATH}"
WORKDIR /opt/alcali/code
COPY . /opt/alcali/code

RUN pip install --user -U setuptools
RUN pip install --user .
