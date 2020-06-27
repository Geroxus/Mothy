from src import send
from src.log import log

admin_prefix_len = 2


# This is the main file for all admin commands; that are to configure mothy for the respective server
# the structure goes as follows:
# admin method
# ~ if condition that tests every message for a prepromted substring after it removed the admin prefix
# ~ ~ script to be executed upon if condition returning True
# ~ ~ return False except when the server_info needs to be updated, this is a control flag and is being used in bot.py
#
#
# executable commands are:
# 1 alias:
#   creates an alias for a user in the alias data as a string: format is: "name:mention string"
#
# 2 love:
#   make Mothy tell the Member with respective alias that Mothy loves them
#   TODO it works even if no member with an alias exists, this needs a "Sorry, I don't know any <name>" msg
#   TODO add functionality to love members with their mentions
#   TODO remove invoking msg and only show the love msg maybe
#
# 3 say:
#   makes Mothy share any registered reaction from /data/msgs/reactions
#
# TODO 4 submit_reaction
#   a function that enables operators to submit a reaction to me<the developer> so that I can review add it
#   submission should be saved in a guild  specific file
#
# 5 add operator:
#   lets existing operators add new operators to the guild specific settings file
#   new operators will just be appended to the file
#   TODO learn SQL or anything similar and re-build the settings file as a database of settings instead so that it saves
#       storage capacity, adds administration ability and is more well organized; also that will improve on Mothys
#       functionality and versatility
#
# TODO 6 remove operator
#   lets the server owner/any operator remove operators from the operators list, requires the Database implementation
#   and will be tackled after that
#
# 7 change:
#   lets operators change ANY guild specific setting if they know the respective names, that is even remove the all
#   operators from the list and make Mothy unmanageable TODO change that
#   the format is: <prefix>change:<setting line name>"<new setting context
#       theoretically the second " is not needed but will be recommended anyways
#   TODO not happy with how this works yet, need to work that out


async def admin(message, client):
    if message.content[admin_prefix_len:].startswith('alias'):
        alias = message.content.split('\"')[1]
        f = open('./data/guildspecific/{}/aliases'.format(message.guild.id), 'ta')
        f.write('\n' + alias + ':' + message.mentions[0].mention)
        f.close()
        log('New alias \"{}\" created for ' + message.mentions[0].name, message.guild.id, True)
        return False

    if message.content[admin_prefix_len:].startswith('love'):
        name = message.content[9:]
        mention = ''
        f = open('./data/guildspecific/{}/aliases'.format(message.guild.id), 'tr')
        for line in f:
            if name in line:
                mention = line.split(':')[1]
        f.close()
        await message.channel.send('I love you! ' + mention)
        log('Love got shared with ' + client.get_user(int(mention[2:-1])).name, message.guild.id, True)
        return False

    if message.content[admin_prefix_len:].startswith('say'):
        await send.reactions(message, message.content[6:])
        log('I shared ' + message.content[6:], message.guild.id, True)
        return False

    if message.content[admin_prefix_len:].startswith('add operator'):
        f = open('./data/guildspecific/{}/settings'.format(message.guild.id), 'ta')
        f.write(',{}'.format(message.mentions[0].id))
        f.close()
        log('I added ' + message.mentions[0].name + ' to op list\n', message.guild.id, True)
        return False

    if message.content[admin_prefix_len:].startswith('change'):
        f = open('./data/guildspecific/{}/settings'.format(message.guild.id), 'tr')
        settings_file = []
        for line in f:
            settings_file.append(line)
        f.close()

        keyword = message.content.split(':')[1].split('"')[0].strip()
        # whats after the : and before the first " without ANY whitespaces
        for line in settings_file:
            if line.startswith(keyword):
                settings_file[settings_file.index(line)] = keyword + '"' + message.content.split('"')[1] + '"\n'

        f = open('./data/guildspecific/{}/settings'.format(message.guild.id), 'tw')
        for line in settings_file:
            f.writelines(line)
        f.close()
        log('changed ' + keyword + ' to "' + message.content.split('"')[1] + '"', message.guild.id, True)
        return True
