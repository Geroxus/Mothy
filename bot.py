import os
import random

import discord

from src import send
from src import guild_info

from src.log import log
from src.mc import McCoord
from src.admin import admin

#
# The main file of my cute little Mothy!
# we rn are working at Version 0.6.2
#       admin access is created
#       TODO add an operator functionality for operators to create custom reactions for custom roles
#        example: <admin_prefix>add role:<role mention> to create react-able roles
#               : <admin_prefix>add reaction:<any substring until the mention sub string starts><role mention>
#                       creates reaction name automatically and sends the name back to the same channel
#        this needs a rework of:
#           the way Mothy saves reactions:
#               custom role reactions are guild specific, a new string of functions required to do this and a new file
#               /msgs/reactions stays since there are still reactions which are same for all guilds after all
#           the way Mothy handles reactions as a function:
#               needs to be a dynamic function rather than the hard coded stuff there is at this point in time
#               maybe save react-able roles with react-ratio or even a ration for every individual reaction?
#                <this screams for a Database please help>
#
#   TODO documentation for the main file
#   TODO documentation for mc file
#
#
#
# changed files:
# all
# TODO: add version keeping for every file and trace every change (so we can build a patch script later!!)
#  or better even ... scrap this I'll do git
#

client = discord.Client()


# Version numbers will soon be included in all files; non the less commented out until practically used


#  version = 0.6.1.2


guild_dirs_list = os.listdir(path='./data/guildspecific/')
guild_info_list = []  # a list of Objects of Class Setting from guild_info.py
admin_id = 235881341860708352  # this is my (Geroxus#0041) id so that I can have extra rights muhaha

f = open('./bot-token', 'tr')
BOTTOKEN = f.readline()
f.close()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    if BOTTOKEN.startswith('Njg3'):
        await client.change_presence(activity=discord.Game('http://www.scp-wiki.net/scp-079'), status=discord.Status.online)
    else:
        await client.change_presence(activity=discord.Game('Praise the L A M P'), status=discord.Status.online)
    # this returns all registered guilds at a startup! and checks for their respective sub-dirs
    for x in client.guilds:
        if str(x.id) in guild_dirs_list:
            print(x.name + ': True')
            guild_info_list.append(guild_info.load(x))
        else:
            print(x.name + ': False')
            await guild_info.register(x)
            guild_info_list.append(guild_info.load(x))


@client.event
async def on_guild_join(guild):
    if str(guild.id) in guild_dirs_list:
        print('We joined: ' + guild.name + ': True')
    else:
        print('We joined: ' + guild.name + ': False')
        await guild_info.register(guild)
        guild_info_list.append(guild_info.load(guild))


@client.event
async def on_message(message):
    if not message.author.bot:
        bot_prefix = guild_info.get_prefix(message.guild, guild_info_list)
        admin_bot_prefix = guild_info.get_admin_prefix(message.guild, guild_info_list)
        admin_list = guild_info.get_operators(message.guild, guild_info_list) + [admin_id]
        # commands
        if message.content.startswith(bot_prefix + 'help'):
            await send.dm_send(message, 'help_message')
            return

        if message.content.startswith(bot_prefix + 'commandslist'):
            await send.dm_send(message, 'commandslist')
            return

        if message.content.startswith(bot_prefix + 'features'):
            await send.dm_send(message, 'features_list')
            return

        # here the evil admin commands my be invoked
        if message.author.id in admin_list and message.content.startswith(admin_bot_prefix):
            if await admin(message, client):
                # returns True iff the guild info has been changed and therefore needs to be reloaded into the cache
                for entry in guild_info_list:
                    if entry.guild_id == message.guild.id:  # finds correct entry in guild_info_list
                        guild_info_list[guild_info_list.index(entry)] = guild_info.load(message.guild)  # actual reload

        # here are all the reactions for all chat-rooms
        serpent_role = discord.utils.find(lambda r: r.name == 'World Serpent', message.guild.roles)
        if serpent_role in message.author.roles:
            if random.randrange(0, 35) < 3:
                await send.reactions(message, 'serpent_role_reaction')
        else:
            if 'moth' in message.content.lower():
                ran_nr = random.randrange(0, 35)
                await send.reactions(message, 'moth_reaction_{}'.format(ran_nr))

        # this is the space for the offerings to lamp code
        if message.channel.name == 'offerings-to-lamp':

            if not message.attachments:
                log('{0} offered only words!'.format(message.author), message.guild.id, True)

                msg = message.content
                # whoever is to spread love may receive great gifts!
                if "love" in msg:
                    await message.channel.send(
                        'Because of your great offering Mothman has bestowed great luck upon you!\n'
                        '\t\t\t\t\t\t\t\t\t\t\t\t**R E J O I C E**')
                    return

                # in case the lamp is not in a good mood an offering might just be to humble
                if len(msg) < random.randrange(10, 50):
                    await message.channel.send('The **LAMP** is enraged by your pathetic offering!')
                    return

                await message.channel.send('Your offering has been received by thine god!')
            else:
                log('{0} brought {1} as an offering'.format(message.author, message.attachments[0].filename),
                    message.guild.id, True)

                if message.attachments[0].size > random.randrange(9000, 1000000):
                    await message.channel.send('The **LAMP** is pleased by thine offering of *data*')
                    return

        # here are all the mc commands!
        if message.content.startswith(bot_prefix + 'mc '):
            log('mc', message.guild.id, True)
            mc_cmd = message.content[4:]
            if mc_cmd.startswith('store'):
                log(' store', message.guild.id)
                new_coord = McCoord(mc_cmd.split(':')[0][6:], mc_cmd.split(':')[1])
                new_coord.store(message.guild.id)
                if new_coord.len != -1:
                    log(' successful for ' + new_coord.name, message.guild.id)
                    await message.channel.send('Successfully entered new coordinate: ' + new_coord.name)
                else:
                    log(' INVALID INPUT: (' + message.content + ')', message.guild.id)
                    await message.channel.send('I could not get that! I am sowwy UwU')
            elif mc_cmd.startswith('read'):
                log(' read', message.guild.id)
                if len(mc_cmd) > 4:
                    old_cord = McCoord().read(message.guild.id, mc_cmd[5:])
                else:
                    old_cord = McCoord().read(message.guild.id)
                await message.channel.send('{}'.format(old_cord))

client.run(BOTTOKEN)
