import time


# This file only consists of the lof function which is supposed to log every activity Mothy undertake and it's details
# not that it would be happening except for the admin commands
#
# structure:
# log function
# ~ create string to write to the guild specific log file
#
# logging works like this rn:
#   1. call log function with new_entry=True to start a new line with timestamp in front of the line
#   2. call log function with new_entry=False (left to default) as often as required to add new information to the
#   same entry without creating a new line and without a timestamp; might rework how this works later
#


def log(string, guild, new_entry=False):
    now = time.gmtime()
    # file = open('./log/{}-{}-{}'.format(now.tm_year, now.tm_mon, now.tm_mday), 'ta')
    file = open('./data/guildspecific/' + str(guild) + '/log/{}-{}-{}'.format(now.tm_year, now.tm_mon, now.tm_mday), 'ta')
    if new_entry:
        file.write('\n{}:{}:{} '.format(now.tm_hour, now.tm_min, now.tm_sec) + string)
    else:
        file.write(string)
    file.close()
