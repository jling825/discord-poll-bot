#TODO: add option to close poll manually
#TODO: add option to close poll with time limit
#TODO: track all active polls
#TODO: add embed thumbnail option
#TODO: display one pass/fail message
#TODO: impliment "!strawpoll" command
#TODO: impliment "!alternativevote" command
#TODO: impliment "!singletransferrablevote" command

import config
import messages
import send_ping

import os
import discord

# set default intents
intents = discord.Intents.default()
intents.reactions = True
intents.members= True

client = discord.Client(intents=intents)

# set data
poll = discord.Embed()
poll_options = []
embed_message = ""
options_message = ""
status_message = ""
running_locally = False
running_online = False

# get Discord token
try:
    bot_token = config.bot_token  # from local config.py
    running_locally = True
except:
    bot_token = os.environ['bot_token']  # from repl.it secret
    running_online = True
    send_ping.ping()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # Configure bot
    elif message.content == '!whitelist':
        if not message.channel.id in messages.whitelist:
            messages.whitelist.append(message.channel.id)
            global status_message
        await message.channel.send(messages.help)
        status_message = await message.channel.send(content="[PASS] Channel whitelisted.")

    elif not message.channel.id in messages.whitelist:
        return

    elif message.content == '!blacklist':
        messages.whitelist.remove(message.channel.id)
        await status_message.edit(content="[PASS] Channel blacklisted.")

    elif not message.content.startswith(tuple(messages.commands)):
        await status_message.edit(content="[FAIL] Unrecognized command: \"{0}\"".format(message.content))
        #await message.channel.send(messages.help)

    elif message.content == '!status':
        await status_message.edit(content="[PASS] Local instance detected: {0} | Online instance detected: {1}".format(running_locally, running_online))

    # poll embed setup
    elif message.content == '!newpoll':
        poll.title = message.author.name + "'s Poll"
        poll.description = ""
        poll.url = ""
        poll.clear_fields()
        poll.color = 0x808080
        global embed_message
        global options_message
        embed_message = await message.channel.send(embed=poll)
        options_message = await message.channel.send("Options:")
        status_message = await message.channel.send(content="[PASS] New poll started.")

    elif message.content.startswith('!polltitle'):
        try:
            poll.title = message.content.split(' ', 1)[1]
            await embed_message.edit(embed=poll)
            await status_message.edit(content="[PASS] Poll title updated.")
        except IndexError:
            await status_message.edit(content="[FAIL] Poll title cannot be empty.")
        except AttributeError:
            await status_message.edit(content="[FAIL] Cannot update title. No poll to edit.")
    
    elif message.content.startswith('!polldesc'):
        try:
            poll.description = message.content.split(' ', 1)[1]
            await embed_message.edit(embed=poll)
            await status_message.edit(content="[PASS] Poll description updated.")
        except IndexError:
            try:
                poll.description = ""
                await embed_message.edit(embed=poll)
                await status_message.edit(content="[PASS] Poll description removed.")
            except AttributeError:
                await status_message.edit(content="[FAIL] Cannot update description. No poll to edit.")
        except AttributeError:
            await status_message.edit(content="[FAIL] Cannot update description. No poll to edit.")
        

    elif message.content.startswith('!pollurl'):
        try:
            if "https://" in message.content.split(' ', 1)[1]:
                poll.url = message.content.split(' ', 1)[1]
            else:
                poll.url = "https://" + message.content.split(' ', 1)[1]
            await embed_message.edit(embed=poll)
            await status_message.edit(content="[PASS] Poll url updated.")
        except IndexError:
            try:
                poll.url = ""
                await embed_message.edit(embed=poll)
                await status_message.edit(content="[PASS] Poll url removed.")
            except AttributeError:
                await status_message.edit(content="[FAIL] Cannot update url. No poll to edit.")
        except AttributeError:
            await status_message.edit(content="[FAIL] Cannot update url. No poll to edit.")

    # poll options setup
    elif message.content.startswith('!polladd'):
        try:
            poll_options.append(message.content.split(' ', 1)[1])
            await options_message.edit(content="Options: {0}".format(poll_options))
            await status_message.edit(content="[PASS] Poll option added.")
        except IndexError:
            await status_message.edit(content="[FAIL] Poll option cannot be empty.")
        except AttributeError:
            await status_message.edit(content="[FAIL] Cannot add poll option. No poll to edit.")

    elif message.content.startswith('!polldrop'):
        try:
            poll_options.remove(message.content.split(' ', 1)[1])
            await options_message.edit(content="Options: {0}".format(poll_options))
            await status_message.edit(content="[PASS] Poll option removed.")
        except IndexError:
            await status_message.edit(content="[FAIL] Poll option cannot be empty.")
        except ValueError:
            await status_message.edit(content="[FAIL] Cannot remove poll option. Option does not exist.")
        except AttributeError:
            await status_message.edit(content="[FAIL] Cannot remove poll option. No poll to edit.")

    # start tally
    elif message.content == '!tally':
        try:
            await options_message.delete()
            poll.color = 0x0cb7e5
            poll.add_field(name='✅',value="Voted Yes:")
            poll.add_field(name='❔',value="Voted Maybe:")
            poll.add_field(name='❌',value="Voted No:")
            await embed_message.edit(embed=poll)
            await embed_message.add_reaction('✅')
            await embed_message.add_reaction('❔')
            await embed_message.add_reaction('❌')
            await status_message.edit(content="[PASS] New tally started.")
        except AttributeError:
            await status_message.edit(content="[FAIL] Cannot start tally.  No poll available.")

    if message.author != client.user:
        await message.delete()

@client.event
async def on_reaction_add(reaction, user):
    embed_message = reaction.message
    # update embeds for tallys
    if embed_message.author == client.user and embed_message.embeds[0].color.value == 0x0cb7e5:
        
        for i in range(len(embed_message.embeds[0].fields)):
            if embed_message.embeds[0].fields[i].name == reaction.emoji:
                new_value = embed_message.embeds[0].fields[i].value.split('\n')[0]
                reaction_users = await reaction.users().flatten()

                for user in reaction_users:
                    if user != client.user:
                        new_value += "\n" + user.name

                poll = embed_message.embeds[0].set_field_at(index=i,name=reaction, value=new_value)
                await embed_message.edit(embed=poll)
    else:
        return

@client.event
async def on_reaction_remove(reaction, user):
    embed_message = reaction.message
    # update embeds for tallys
    if embed_message.author == client.user and embed_message.embeds[0].color.value == 0x0cb7e5:

        for i in range(len(embed_message.embeds[0].fields)):
            if embed_message.embeds[0].fields[i].name == reaction.emoji:
                new_value = embed_message.embeds[0].fields[i].value.split('\n')[0]
                reaction_users = await reaction.users().flatten()

                for user in reaction_users:
                    if user != client.user:
                        new_value += "\n" + user.name

                poll = embed_message.embeds[0].set_field_at(index=i,name=reaction, value=new_value)
                await embed_message.edit(embed=poll)
    else:
        return

client.run(bot_token)