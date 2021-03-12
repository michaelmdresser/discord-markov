import discord
import sqlite3
import time
import os
import sys

client = discord.Client()

async def build_db_for_channel(list_of_channels):
    await client.wait_until_ready()

    start = time.time()

    print("connecting to db")
    con = sqlite3.connect('messages.db')
    cur = con.cursor()

    print("creating table")
    cur.execute('''CREATE TABLE IF NOT EXISTS messages
    (channel_id text, author_id text, id text, content text)
    ''')
    con.commit()

    print("beginning read")
    total = 0;
    # the first input of argv is the program itself, so start at 1
    for channel_id_raw in list_of_channels[1:]:
        channel_id = int(channel_id_raw)
        print("getting channel ", channel_id)
        channel = client.get_channel(channel_id)
        if channel is None:
            raise Exception("Error with channel ID ", str(channel_id))
        else:
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
            total += processed
            print("finished getting messages from channel ", channel_id, ", total processed ", processed)
    duration = time.time() - start
    print("Total processed:", total)
    print("Final duration:", duration)
    return

# https://stackoverflow.com/questions/63846749/how-to-send-message-without-command-or-event-discord-py
# once the task is done, you can ctrl-c this process
if len(sys.argv) >=1:
    client.loop.create_task(build_db_for_channel(sys.argv))
    client.run(os.environ["DISCORD_TOKEN"])
else:
    print("No channels were input in Command Line")
