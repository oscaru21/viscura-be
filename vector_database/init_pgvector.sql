CREATE EXTENSION IF NOT EXISTS vector;
DROP TABLE IF EXISTS embeddings;
/*
An embedding created with CLIP (Contrastive Language–Image Pretraining) 
typically has 512 dimensions for both text and image embeddings
*/
CREATE TABLE contexts (
    id bigserial PRIMARY KEY, 
    event_id integer,
    content TEXT, 
    embedding vector(384)
);

CREATE TABLE images (
    id bigserial PRIMARY KEY, 
    event_id integer,
    norm float,
    embedding vector(512)
);

CREATE TABLE posts (
    id bigserial PRIMARY KEY,
    event_id INTEGER NOT NULL,
    caption TEXT,
    image_ids INTEGER[],
    user_id INTEGER
);

CREATE TABLE events (
    id bigserial PRIMARY KEY, 
    org_id integer,
    title TEXT, 
    description TEXT
);

CREATE TABLE feedbacks (
    id bigserial PRIMARY KEY, 
    post_id integer,
    event_id integer,
    feedback_status TEXT,
    feedback_comment TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- insert sample events some events
INSERT INTO events (title, description, org_id) VALUES ('Event 1', 'Event 1 description', 1);
INSERT INTO events (title, description, org_id) VALUES ('Event 2', 'Event 2 description', 1);
INSERT INTO events (title, description, org_id) VALUES ('Event 3', 'Event 3 description', 1);

INSERT INTO feedbacks (post_id, event_id, feedback_status, feedback_comment, created_at) VALUES (7, 7, 'Approved', 'good post, i like the content', '2024-10-31 17:54:28');
INSERT INTO feedbacks (post_id, event_id, feedback_status, feedback_comment, created_at) VALUES (17, 17, 'Rejected', 'bad post, i dont like the caption', '2024-11-01 11:13:28');
INSERT INTO feedbacks (post_id, event_id, feedback_status, feedback_comment, created_at) VALUES (27, 27, 'Pending', ' i like the content, but the lack of emojis is a pain in the ass','2024-10-31 07:04:28');
