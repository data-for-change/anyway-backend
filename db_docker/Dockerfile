FROM postgres:12

ENV POSTGIS_MAJOR 3
ARG POSTGRES_PASSWORD
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ARG POSTGRES_USER
ENV POSTGRES_USER=${POSTGRES_USER}
ARG POSTGRES_DB
ENV POSTGRES_DB=${POSTGRES_DB}  

RUN apt-get update \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts \
           postgis \
      && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/postgis.sh
COPY ./update-postgis.sh /usr/local/bin
