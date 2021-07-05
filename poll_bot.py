import os
import config
import discord

# get Discord token
try:
    bot_token = config.bot_token # from local config.py
    print("Getting token from congif.py")
except:
    bot_token = os.environ['bot_token'] # from repl.it secret
    print("Getting token from repl.it secret")

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

    if message.content.startswith('!startpoll'):
        split_msg = message.content.split(' ',1)
        if len(split_msg) == 1:
            await message.channel.send('Accepting voting options for ' + message.author.name + '\'s poll')
        else:
            await message.channel.send('Accepting voting options for ' + split_msg[1])
        

client.run(bot_token)