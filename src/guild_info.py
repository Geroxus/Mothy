import os


# This file provides all the functions needed to operate the guild info list and is a pure backend utilities file
# preliminarily finished; but will become completely redone when I understand Databases
# the structure goes as follows:
# Settings class
#
# coroutine functions
#
# regular functions
#
#
# Settings
#   is a class to save all guild relevant information in the cache so that Mothy may use those without opening files
#   might rethink this though since many guild would the take up a lot of ram
#   also the structure is not optimal, reminds of a struct in C not what any Class would be capable of
#   TODO instead of separate functions implement them as member functions of Settings class
#   TODO rename Settings class, that name is no good
#       list of ideas:
#           GuildSettings
# register
#   iff Mothy is being invited to a new guild or Data may have gone lost for whatever reason this coroutine creates
#   the standard settings file in the guild specific folder as well as all required folders
#
# load
#   loads information from settings files into respective objects of class Setting
#   returns those objects so that in the main file the information may be stored in a list for further usage
#
# get_prefix
#   searches the whole list it received from the main file for a guild with the same id as the guild which got relayed
#   TODO all information about a guild are not required only just the ID
#
# get_admin_prefix
#   same as get_prefix but returns a different entry from the Settings object
#
# get_operators
#   same as get_prefix but returns list of integers which correspond to the operator IDs


class Settings:
    def __init__(self, guild_id, prefix, admin_prefix, operator_list):
        self.guild_id = guild_id
        self.prefix = prefix
        self.admin_prefix = admin_prefix
        self.operator_list = operator_list


async def register(guild):
    os.makedirs('./data/guildspecific/{}/mc'.format(guild.id))
    os.makedirs('./data/guildspecific/{}/log'.format(guild.id))
    f = open('./data/guildspecific/{}/settings'.format(guild.id), 'tw')
    f.write('prefix\"!\"\n')
    f.write('admin_prefix\"!-\"\n')
    f.write('operator_list=\"{}'.format(guild.owner.id))
    f.close()


def load(guild):
    f = open('./data/guildspecific/{}/settings'.format(guild.id), 'tr')
    prefix = f.readline().split('\"')[1]
    admin_prefix = f.readline().split('\"')[1]
    operator_list = []
    # loads the raw op list string and turns it into an actual list of ids
    for op in f.readline().split('\"')[1].split(','):
        operator_list.append(int(op))
    f.close()
    return Settings(guild.id, prefix, admin_prefix, operator_list)


def get_prefix(guild, guild_info_list):
    for entry in guild_info_list:
        if entry.guild_id == guild.id:
            return entry.prefix


def get_admin_prefix(guild, guild_info_list):
    for entry in guild_info_list:
        if entry.guild_id == guild.id:
            return entry.admin_prefix


def get_operators(guild, guild_info_list):
    for entry in guild_info_list:
        if entry.guild_id == guild.id:
            return entry.operator_list


# this function is basically useless but will be left in the program for further use, might remove if not applicable
# def is_operator(guild, guild_info_list, member):
#     for entry in guild_info_list:
#         if entry.guild_id == guild.id:
#             if member in entry.operator_list:
#                 return True
#             return False
