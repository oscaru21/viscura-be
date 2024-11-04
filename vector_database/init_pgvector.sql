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

CREATE TABLE events (
    id bigserial PRIMARY KEY, 
    org_id integer,
    title TEXT, 
    description TEXT
);

-- insert sample events some events
INSERT INTO events (title, description, org_id) VALUES ('Event 1', 'Event 1 description', 1);
INSERT INTO events (title, description, org_id) VALUES ('Event 2', 'Event 2 description', 1);
INSERT INTO events (title, description, org_id) VALUES ('Event 3', 'Event 3 description', 1);