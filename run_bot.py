import discord
import markovify
from os import path
import os
import sys

client = discord.Client()

# the channel id to restrict sending messages to
botspam_channel_id = int(sys.argv[1])

@client.event
async def on_message(message):
    if message.channel.id != botspam_channel_id:
        return
    
    if message.author == client.user:
        return

    if not client.user.mentioned_in(message):
        return
    
    if len(message.mentions) != 2:
        print("mentioned count was: %s" % len(message.mentions))
        return

    target = message.mentions[1]
    if target == client.user:
        target = message.mentions[0]

    serialized_target = "chains/%s" % target.id

    if not path.exists(serialized_target):
        print("target %s for message %s doesn't exist" % (serialized_target, message))
        return

    model = None
    with open(serialized_target) as f:
        json = f.readlines()[0]
        model = markovify.Text.from_json(json)

    tries = 0
    max_tries = 15
    # sometimes the chain will generate a None message
    while tries < max_tries:
        sentence = model.make_sentence()
        if sentence is not None:
            await message.channel.send(sentence, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
            return
        tries += 1

    print("exceeded max tries")
    return


client.run(os.environ['DISCORD_TOKEN'])
