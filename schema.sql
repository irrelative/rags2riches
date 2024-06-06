CREATE TABLE Post (
    Id SERIAL PRIMARY KEY,
    PostTypeId INT NOT NULL,
    CreationDate TIMESTAMP NOT NULL,
    Score INT NOT NULL,
    Body TEXT NOT NULL,
    OwnerUserId INT NOT NULL DEFAULT -1,
    LastActivityDate TIMESTAMP NOT NULL,
    ContentLicense TEXT NOT NULL,
    ViewCount INT,
    AcceptedAnswerId INT,
    ParentId INT,
    DeletionDate TIMESTAMP,
    OwnerDisplayName TEXT,
    LastEditorUserId INT,
    LastEditorDisplayName TEXT,
    LastEditDate TIMESTAMP,
    Title TEXT,
    Tags TEXT,
    AnswerCount INT,
    CommentCount INT,
    FavoriteCount INT,
    ClosedDate TIMESTAMP,
    CommunityOwnedDate TIMESTAMP
);

-- Example index on PostTypeId to speed up queries filtering by this column
CREATE INDEX idx_post_posttypeid ON Post (PostTypeId);

-- Example index on ParentId to speed up queries filtering by this column
CREATE TABLE embedding_search (
    id SERIAL PRIMARY KEY,
    post_id INT,
    embedding VECTOR(1536),
    FOREIGN KEY (post_id) REFERENCES Post(id)
);
