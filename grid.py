#coding: utf-8

class Grid():
    def __init__(self, length, dimension):
        self.length = length
        self.dimension = dimension
        self.grid = [[None] * length for i in range(length)]
        self.foodGrid = [[0] * length for i in range(length)]


    def reset(self):
        self.grid = [[None] * self.length for i in range(self.length)]

    def set(self, location, value):
        # draw the bots
        self.grid[location[0]][location[1]] = value


    def get(self, location):
        return self.grid[location[0]][location[1]]

    def __str__(self):
        plot = ""

        for d1 in range(self.length):
            plot += '|'
            for d2 in range(self.length):
                char = ' '

                if self.foodGrid[d1][d2] > 2000:
                    char = '⁞'
                elif self.foodGrid[d1][d2] > 1000:
                    char = ':'
                elif self.foodGrid[d1][d2] > 0:
                    char = '.'
#                 if self.foodGrid[d1][d2] > 0:
#                     char = '{:1}'.format(int(self.foodGrid[d1][d2] / 20))
#
                if self.grid[d1][d2]:
                    if char != ' ':
                        char = self.grid[d1][d2].upper()
                    else:
                        char = self.grid[d1][d2]

                plot += char
            plot += '|\n'


        topRow = '_' * (self.length + 2)
        bottomRow = '‾' * (self.length + 2)
        out = topRow + '\n'
        out += plot
        out += bottomRow
        return out
