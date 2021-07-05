import config
import send_ping

import os
import discord

# get Discord token
try:
    bot_token = config.bot_token  # from local config.py
    execution_location = 'locally'
except:
    bot_token = os.environ['bot_token']  # from repl.it secret
    execution_location = 'online'

client = discord.Client()

# testing embeds
'''
@client.command()
async def embed(ctx, poll_title):
    embed=discord.Embed(title=poll_title)
'''


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!execution'):
        await message.channel.send('Currently executed ' + execution_location)

    if message.content.startswith('!startpoll'):
        split_msg = message.content.split(' ', 1)
        if len(split_msg) == 1:
            await message.channel.send('Accepting voting options for ' + message.author.name + '\'s poll')
        else:
            await message.channel.send('Accepting voting options for ' + split_msg[1])

send_ping.ping()  # disable this to test locally
client.run(bot_token)
