from random import randint, choice,  random
from math import copysign, pi, sin, cos, log10

class Action():
    def __init__(self, move, spawn):
        self.move = move
        self.spawn = spawn


class Robot():

    def __init__(self, world, loc, name):
        self.id = world.get_next_id()
        self.food = world.spawnCost - 10
        self.onFood = False
        self.name = name
        self.location = loc
        self.moveThreshold = randint(0, 200)
        self.world = world
        self.action = [[0, 0], False]
        self.direction = random() * 2 * pi

    def spawn(self):
        newbot = Robot(self.world, self.location, self.name)
        newbot.moveThreshold = max(self.moveThreshold + randint(-1, 1), 1)
        if random() < .02:
            newbot.name = self.world.get_next_name()
        return newbot

    def act(self, grid, location):


        move = None
        spawnThreshold = self.world.spawnCost * 2
        if self.food > self.moveThreshold or not self.onFood:
#             move = [randrange(2*self.moveAmount) - self.moveAmount for d in range(self.world.worldDim)]
            self.direction += choice([-1 * pi / 10, 0, pi / 10])
            self.direction %= pi * 2
            signs = [int(copysign(1, thing)) for thing in [sin(self.direction), cos(self.direction)]]
            if random() < sin(self.direction)/cos(self.direction):
                move = [signs[0], 0]
            else:
                move = [0,signs[1]]
#             print self.id,'move', move
        else:
            move = [0] * self.world.worldDim
#             print self.id,'no move'

        spawn = self.food > spawnThreshold and self.onFood
        self.action = (move, spawn)
        return (move, spawn)

#         if self.food > self.moveThreshold and self.move == [0]*worldDim:
#             print 'lazy', self.food, self.moveThreshold, self.move


    def __str__(self):
        idWidth = int(ceil(log10(self.world.maxId)))
        return "bot {} '{}' f: {:3} loc:({}), move: ({}), dir: {:3.1f} thresh: {:3}, onFood: {}, spawn: {}"\
            .format(str(self.id).rjust(idWidth), self.name.upper(), self.food, ','.join(['{:3}'.format(l) for l in self.location]), \
                     ','.join(['{:3}'.format(l) for l in self.action[0]]), self.direction, \
                    self.moveThreshold, '1' if self.onFood else '0', '1' if self.action[1] else '0')
