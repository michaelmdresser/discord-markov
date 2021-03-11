import discord
import sqlite3
import time
import os
import sys

# channel ID to read messages from
# currently only supports building db
# from a single channel, though this could
# easily be extended
general_channel_id = sys.argv[1]

client = discord.Client()

async def build_db_for_channel(channel_id):
    await client.wait_until_ready()

    start = time.time()

    print("getting channel")
    channel = client.get_channel(channel_id)
    if channel is None:
        raise Exception("channel is none")

    print("connecting to db")
    con = sqlite3.connect('messages.db')
    cur = con.cursor()

    print("creating table")
    cur.execute('''CREATE TABLE IF NOT EXISTS messages
    (channel_id text, author_id text, id text, content text)
    ''')
    con.commit()

    print("beginning read")
    processed = 0
    async for message in channel.history(limit=None):
        if processed % 1000 == 0:
            print("Processed:", processed)
            duration = time.time() - start
            print("Duration:", duration)
            print()

        cur.execute('INSERT INTO messages VALUES (?, ?, ?, ?)',
                    (message.channel.id, message.author.id, message.id, message.content))
        processed += 1
    con.commit()

    duration = time.time() - start
    print("Total processed:", processed)
    print("Final duration:", duration)
    return

# https://stackoverflow.com/questions/63846749/how-to-send-message-without-command-or-event-discord-py
# once the task is done, you can ctrl-c this process
client.loop.create_task(build_db_for_channel(general_channel_id))
client.run(os.environ["DISCORD_TOKEN"])
