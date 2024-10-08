
# This is installing the pgvector extension for postgres
# Source: https://www.thestupidprogrammer.com/blog/docker-with-postgres-and-pgvector-extension/
FROM postgres:15-bullseye

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-all \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN git clone https://github.com/pgvector/pgvector.git

WORKDIR /tmp/pgvector
RUN make
RUN make install