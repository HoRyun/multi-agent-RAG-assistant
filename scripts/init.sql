-- WHY: pgvector binary is installed in the image but the extension must be
--      explicitly enabled per database before vector columns can be used.
CREATE EXTENSION IF NOT EXISTS vector;
