import discord
import markovify
from os import path
import os
import sys

client = discord.Client()

# the channel id to restrict sending messages to
botspam_channel_id = int(sys.argv[1])

def generate_message(targetID):
    serialized_user = "chains/%s" % targetID
    if not path.exists(serialized_user):
        print("target %s for message %s doesn't exist" % (serialized_user, message))
        return str("target %s for message %s doesn't exist" % (serialized_user, message))
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
        output_message = generate_message(target.id)
    else:
        filtered_message = filter(lambda x: x != client.user, message.mentions)
        target = next(filtered_message, None)
        secondary = next(filtered_message, None)
        # if you would like mentions instead of nicknames, uncomment these two lines and comment the two after them.
        # targetID = '<@'+str(target.id)+'>'
        # secondaryID = '<@'+str(secondary.id)+'>'
        targetID = target.display_name
        secondaryID = secondary.display_name
        # print(targetID, " ", secondaryID, " ")
        output_message = "" + targetID + ":\n\t" + generate_message(target.id) + '\n\n' + "" + secondaryID + ":\n\t" + generate_message(secondary.id)
        output_message += "\n\n" + targetID + ":\n\t" + generate_message(target.id) + '\n\n' + "" + secondaryID + ":\n\t" + generate_message(secondary.id)
    await message.channel.send(output_message, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))

client.run(os.environ['DISCORD_TOKEN'])
