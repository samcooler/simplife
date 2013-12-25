from grid import Grid
from robot import Robot

from random import randint, choice, random
import string

class World():

    foodEatingRate = 5
    foodStartValue = 1000
    worldDim = 2
    worldLen = 160
    foodRatio = 2
    numFoods = int(foodRatio * worldLen ** 2)
    foodEaten = 0
    foodClump = 50
    foodSpread = 3
    spawnCost = 30
    nameList = string.ascii_lowercase
    nameIndex = 0
    attritionRate = 0.2
    numRobots = 100
    maxId = 0

    def __init__(self):
        self.grid = Grid(self.worldLen, self.worldDim)
        self.spawn_food(self.numFoods)
        self.nameList = list(string.ascii_lowercase)


        self.locations = [[i] * self.worldDim for i in range(0, self.worldLen, self.worldLen / self.numRobots)]

        self.robots = []
        self.spawn_robot(self.numRobots)
        
    def get_next_id(self):
        self.maxId += 1
        return self.maxId
    
    def get_next_name(self):
        self.nameIndex += 1
        self.nameIndex %= len(self.nameList)
#         print self.nameList[-1]
        return self.nameList[self.nameIndex]

    def spawn_robot(self, count):
        for i in range(count):
            loc = [randint(0, self.worldLen - 1) for d in range(self.worldDim)]
            name = self.get_next_name()
            bot = Robot(self, loc, name)
            self.robots.append(bot)

    def spawn_food(self, count):
        amount = 0
        for i in range(count / self.foodClump):
            locCenter = [randint(self.foodSpread, self.worldLen - self.foodSpread - 1) for d in range(self.worldDim)]

            for j in range(self.foodClump):
                loc = [randint(-1 * self.foodSpread, self.foodSpread) for d in range(self.worldDim)]
                self.grid.foodGrid[loc[0] + locCenter[0]][loc[1] + locCenter[1]] += self.foodStartValue
                amount += self.foodStartValue
        return amount

    def remove_dead_robots(self):
        # remove dead bots
        for bot in self.robots:
            if random() < self.attritionRate:
                bot.food -= 1
            if bot.food <= 0:
                self.robots.remove(bot)
