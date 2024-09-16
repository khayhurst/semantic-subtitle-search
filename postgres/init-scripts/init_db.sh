#!/bin/bash

# Create the database if it does not exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO \$$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_database WHERE datname = '$POSTGRES_DB'
        ) THEN
            CREATE DATABASE $POSTGRES_DB;
        END IF;
    END
    \$$;
EOSQL

# Run all SQL scripts against the new database
for f in /docker-entrypoint-initdb.d/*.sql; do
    echo "Running $f..."
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$f"
done
