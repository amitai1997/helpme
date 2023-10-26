FROM postgis/postgis:16-3.4

# Copy the initialization script into the Docker image
COPY ./compose/local/postgres/init-script.sql /docker-entrypoint-initdb.d/

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
