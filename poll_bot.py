import config
import discord

client = discord.Client()

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
        

client.run(config.discord_token)