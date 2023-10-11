DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'debug') THEN
    CREATE USER debug WITH PASSWORD 'debug';
  END IF;
END $$;

ALTER ROLE debug SET client_encoding TO 'utf8';
ALTER ROLE debug SET default_transaction_isolation TO 'read committed';
ALTER ROLE debug SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE helpme TO debug;

-- Connect to the database and create the PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
