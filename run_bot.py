import discord
import markovify
from os import path
import os
import sys

client = discord.Client()

# the channel id to restrict sending messages to
botspam_channel_id = int(sys.argv[1])

def generate_message(serialized_user):
    model = None
    with open(serialized_user) as f:
        json = f.readlines()[0]
        model = markovify.Text.from_json(json)
    tries = 0
    max_tries = 15
    # sometimes the chain will generate a None message
    while tries < max_tries:
        sentence = model.make_sentence()
        if sentence is not None:
            return sentence
        tries += 1
    print("exceeded max tries")
    return "Markov Genie has encountered an error! Maximum attempts at Sentence Generation reached without output"

@client.event
async def on_message(message):
    if message.channel.id != botspam_channel_id:
        return
    
    if message.author == client.user:
        return

    if not client.user.mentioned_in(message):
        return
    
    if len(message.mentions) != 2 and len(message.mentions) != 3:
        print("mentioned count was: %s" % len(message.mentions))
        return
    
    if len(message.mentions) == 2:
        target = message.mentions[1]
        if target == client.user:
            target = message.mentions[0]
        serialized_target = "chains/%s" % target.id
        if not path.exists(serialized_target):
            print("target %s for message %s doesn't exist" % (serialized_target, message))
            return
        output_message = generate_message(serialized_target)
    else:
        if message.mentions[0] == client.user:
            target = message.mentions[1]
            secondary = message.mentions[2]
        elif message.mentions[1] == client.user:
            target = message.mentions[0]
            secondary = message.mentions[2]
        else:
            target = message.mentions[0]
            secondary = message.mentions[2]
        # if you would like mentions instead of nicknames, uncomment these two lines and comment the two after them.
        # targetID = '<@'+str(target.id)+'>'
        # secondaryID = '<@'+str(secondary.id)+'>'
        targetID = target.nick
        secondaryID = secondary.nick
        serialized_target = "chains/%s" % target.id
        serialized_secondary = "chains/%s" % secondary.id
        if not path.exists(serialized_target):
            print("target %s for message %s doesn't exist" % (serialized_target, message))
            return
        if not path.exists(serialized_secondary):
            print("target %s for message %s doesn't exist" % (serialized_secondary, message))
            return
        output_message = "" + targetID + ": " + generate_message(serialized_target) + '\n' + "" + secondaryID + ": " + generate_message(serialized_secondary)
        output_message += "\n" + targetID + ": " + generate_message(serialized_target) + '\n' + "" + secondaryID + ": " + generate_message(serialized_secondary)
    await message.channel.send(output_message, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))

client.run(os.environ['DISCORD_TOKEN'])
