class McCoord:
    def __init__(self, name=None, coord=None):
        if name is None and coord is None:
            return
        self.name = name
        if len(coord.split(',')) == 3:
            self.x = int(coord.split(',')[0])
            self.y = int(coord.split(',')[1])
            self.z = int(coord.split(',')[2])
            self.len = 3
        elif len(coord.split(',')) == 2:
            self.x = int(coord.split(',')[0])
            self.z = int(coord.split(',')[1])
            self.len = 2
        else:
            self.name = self.name + 'ERROR at coordinate input!'
            self.len = -1

    def __str__(self):
        if self.len == 3:
            return '{}, {}, {}'.format(self.x, self.y, self.z)
        elif self.len == 2:
            return '{}, \\NA/, {}'.format(self.x, self.z)
        else:
            return 'INVALID'

    def store(self, guild_id):
        f = open('./data/guildspecific/{}/mc/coord'.format(guild_id), 'ta')
        if self.len == 3:
            f.write('{}:'.format(self.len) + self.name + ':{},{},{}\n'.format(self.x, self.y, self.z))
        elif self.len == 2:
            f.write('{}:'.format(self.len) + self.name + ':{},{}\n'.format(self.x, self.z))
        f.close()

    def read(self, guild_id, name=None):
        f = open('./data/guildspecific/{}/mc/coord'.format(guild_id), 'tr')
        if name is None:
            msg = ''
            for line in f:
                msg += line.split(':')[1] + ': ' + line.split(':')[2]
            f.close()
            return msg
        else:
            # since the length can't normally be negativ this is my exceptions flag
            self.len = -1
            for line in f:
                if name.lower() in line.lower():
                    strs = line.split(':')
                    self.len = int(strs[0])
                    self.name = strs[1]
                    self.x = int(strs[2].split(',')[0])
                    self.y = int(strs[2].split(',')[1])
                    self.z = int(strs[2].split(',')[2])
            f.close()
            return self
