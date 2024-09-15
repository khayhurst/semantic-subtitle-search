-- Create the 'vector' extension within the database that is set in the docker-compose.yml
-- Source: https://www.thestupidprogrammer.com/blog/docker-with-postgres-and-pgvector-extension/
CREATE EXTENSION IF NOT EXISTS vector;