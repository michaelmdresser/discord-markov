# discord-markov
Generate bad clones of the denizens of your Discord server

## Usage

> Channel IDs and User IDs can be obtained by turning
> developer mode on in Discord and then right-clicking
> a user or channel and clicking "Copy ID"

Dependencies:
``` sh
pip3 install markovify
```

Create a bot. Add it to your server with message send
and read message history permissions. Set the environment variable `DISCORD_TOKEN` to a bot token with those permissions.


Build the database of channel messages. Run with as many channels as you want, separated by spaces; run again to update database. Is rate-limited, so it will take a while.
``` sh
python3 build_msg_db.py CHANNEL_ID_TO_READ_MESSAGES_FROM_1 CHANNEL_ID_TO_READ_MESSAGES_FROM_2... 
```

Build the markov chains and serialize in the `chains/` directory.
``` sh
mkdir chains
python3 build_markov.py
```

You can test a chain with:

``` sh
python3 test_markov.py USER_ID
```

Run the bot:
``` sh
python3 run_bot.py ONLY_CHANNEL_ID_TO_READ_AND_SEND_TO
```

To queue up a bot message, @mention the bot in discord as well as 1 or 2 other members of the guild.
``` sh
@Markov-bot @michaelm
@Markov-bot @michaelm @dresser
```