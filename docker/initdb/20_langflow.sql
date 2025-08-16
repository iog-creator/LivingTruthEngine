-- Idempotent Langflow DB setup
DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='langflow') THEN
    CREATE ROLE langflow LOGIN PASSWORD 'langflow';
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname='langflow') THEN
    CREATE DATABASE langflow OWNER langflow;
  END IF;
END $$;

ALTER DATABASE langflow OWNER TO langflow;

\connect langflow;

-- Extensions (skip if not available)
DO $$ BEGIN BEGIN
  CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EXCEPTION WHEN undefined_file THEN RAISE NOTICE 'uuid-ossp not available'; END; END $$;
DO $$ BEGIN BEGIN
  CREATE EXTENSION IF NOT EXISTS pgcrypto;
EXCEPTION WHEN undefined_file THEN RAISE NOTICE 'pgcrypto not available'; END; END $$;
DO $$ BEGIN BEGIN
  CREATE EXTENSION IF NOT EXISTS vector;
EXCEPTION WHEN undefined_file THEN RAISE NOTICE 'pgvector not available'; END; END $$;

ALTER SCHEMA public OWNER TO langflow;
GRANT ALL PRIVILEGES ON SCHEMA public TO langflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO langflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO langflow;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO langflow;
