# This file is supposed to be the only one which interacts with the send function of the discord API!
# rn that is obviously not the case
# the structure goes as follows:
# coroutine functions
#
#
# dm_send
#   sends a string to the users dm consisting of everything in the specified file
#
# reactions
#   send a message to the same channel the invoking message is in consisting of the string in the line of the reactions
#   file which starts with what the reaction is called, it's name so to speak; the reaction name will not be send
#
# TODO
#   move all .send interactions to this file


async def dm_send(message, file):
    if not message.author.dm_channel:
        await message.author.create_dm()
    f = open('./data/msgs/' + file)
    msg = f.read()
    f.close()
    await message.author.dm_channel.send(msg)


async def reactions(message, reaction):
    f = open('./data/msgs/reactions')
    for line in f:
        if line.startswith(reaction):
            await message.channel.send(line[len(reaction):])
    f.close()
