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


Build the database of messages (currently supports only one channel, but you could run it again with a different channel ID). Is rate-limited, so it will take a while.
``` sh
python3 build_msg_db.py CHANNEL_ID_TO_READ_MESSAGES_FROM
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
