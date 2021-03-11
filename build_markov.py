import markovify
import time
import sqlite3

con = sqlite3.connect('messages.db')
cur = con.cursor()

# limit chain generation to users who have sent more than 100 messages
cur.execute('SELECT author_id, COUNT(*) count FROM messages GROUP BY author_id HAVING COUNT(*) > 100')

top_users = cur.fetchall()


def markov_messages(messages):
    # as_text = '\n'.join(messages)
    # text_model = markovify.Text(as_text, well_formed=False)

    # "sentences" are a single message, and each item in
    # the sentence is space-delimited
    # 
    # this seems to work very well for discord messages
    parsed = list(map(lambda x: x.split(" "), messages))

    text_model = markovify.Text(None, parsed_sentences=parsed, well_formed=False)
    compiled = text_model.compile()
    return compiled

for row in top_users:
    author_id = row[0]
    cur.execute('SELECT content FROM messages WHERE author_id=?', (author_id,))
    messages = list(map(lambda x: x[0], cur.fetchall()))

    chain = markov_messages(messages)

    model_json = chain.to_json()

    with open("chains/%s" % author_id, mode="w") as f:
        f.write(model_json)
    
