import psycopg2
import openai

# Configure your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def create_embeddings(texts):
    texts = [text[:8191] for text in texts]
    response = openai.Embedding.create(input=texts, model="text-embedding-ada-002")
    return [data['embedding'] for data in response['data']]


# Connect to the PostgreSQL database
conn = psycopg2.connect("dbname=rags")
cur = conn.cursor()

try:
    # Query id and body from the post table
    cur.execute("SELECT id, body FROM post where PostTypeId = 1")
    posts = cur.fetchall()

    # Process each post
    batch_size = 1000
    for i in range(0, len(posts), batch_size):
        batch = posts[i:i + batch_size]
        ids, bodies = zip(*batch)

        # Create embeddings for the current batch
        embeddings = create_embeddings(bodies)

        # Insert the embeddings into the embedding_search table
        for post_id, embedding in zip(ids, embeddings):
            cur.execute("""
                INSERT INTO embedding_search (post_id, embedding)
                VALUES (%s, %s)
            """, (post_id, embedding))

    # Commit the transaction
    conn.commit()

finally:
    # Close the database connection
    cur.close()
    conn.close()
