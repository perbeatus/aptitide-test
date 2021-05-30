FROM postgres:11.12
COPY . /fixture-data/
COPY ./load-fixture.sql /docker-entrypoint-initdb.d/
WORKDIR /fixture-data/
RUN tar -xzf db-fixture.tar.gz