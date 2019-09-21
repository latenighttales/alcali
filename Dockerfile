FROM python:3.7-stretch

MAINTAINER Matt Melquiond

# Used in travis
ARG USER_ID=1000

# Upgrade System and Install dependencies
RUN apt-get update && \
  apt-get upgrade -y -o DPkg::Options::=--force-confold && \
  apt-get install -y -o DPkg::Options::=--force-confold netcat

# Upgrade pip
RUN pip install --upgrade pip

# Create unprivileged user
RUN useradd -u ${USER_ID} -ms /bin/bash -d /opt/alcali alcali

# Set default user
USER alcali

# Add env var and fix path
ENV PYTHONUNBUFFERED=1 PATH="/opt/alcali/.local/bin:${PATH}"

# Copy project
COPY --chown=alcali . /opt/alcali/code

# Set work directory
WORKDIR /opt/alcali/code

# Install dependencies
RUN pip install --user -U setuptools

# Install project
RUN pip install --user . mysqlclient psycopg2

EXPOSE 8000

ENTRYPOINT ["/opt/alcali/code/docker/utils/entrypoint.sh"]
