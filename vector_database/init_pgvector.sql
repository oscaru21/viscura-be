CREATE EXTENSION IF NOT EXISTS vector;
/*
An embedding created with CLIP (Contrastive Language–Image Pretraining) 
typically has 512 dimensions for both text and image embeddings
*/
CREATE TABLE embeddings (
    id bigserial PRIMARY KEY, 
    event_id integer,
    content TEXT, 
    embedding vector(512)
);

CREATE TABLE images (
    id bigserial PRIMARY KEY, 
    event_id integer,
    norm float,
    embedding vector(512)
);
