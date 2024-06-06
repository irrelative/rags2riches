import psycopg2

from openai import OpenAI

client = OpenAI()


def generate_embedding(text):
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    embedding = response.data[0].embedding
    return embedding

def search_pg_vector_db(embedding) -> str:
    conn = psycopg2.connect("dbname=rags")
    cur = conn.cursor()
    emb_str = ','.join([str(e) for e in embedding])
    cur.execute(f"SELECT post_id FROM embedding_search ORDER BY embedding <=> '[{emb_str}]' LIMIT 1")
    post_id = cur.fetchone()[0]
    cur.execute(f"SELECT body FROM post WHERE posttypeid = 2 AND ParentId = {post_id} ORDER BY score desc limit 3")
    answers = cur.fetchall()

    ans_str = '\n'.join([ans[0] for ans in answers])
    return ans_str


def is_question(text) -> bool:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Is this a question about history? {text}. Answer with yes or no only.",
            }
        ],
        model="gpt-3.5-turbo",
    )
    resp = chat_completion.choices[0].message.content
    return "yes" in resp.lower()


def answer_question(messages) -> str:
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
    )
    resp = chat_completion.choices[0].message.content
    return resp


def main():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful history chat bot.",
        }
    ]
    while True:
        inp = input("History chat bot, how can I help you today?")

        messages.append({
            "role": "user",
            "content": inp,
        })

        if is_question(inp):
            # Vectorize the input
            input_emb = generate_embedding(inp)
            context_data = search_pg_vector_db(input_emb)
            prompt = f"Question: {inp}\nContext: {context_data}\nAnswer the user's question using the context provdided."
            messages.append({
                "role": "user",
                "content": prompt,
            })

        response = answer_question(messages)
        messages.append({
            "role": "assistant",
            "content": response,
        })

        print(response)
        print('\n\n')


        # Ask LLM if input is a question about history
        # If yes, vectorize the input, and search against our pg vector db
            # Get match, use in LLM prompt to get response

        # Else, just send to LLM for response



if __name__ == '__main__':
    main()