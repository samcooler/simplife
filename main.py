#coding: utf-8

import time, random, string, os

from collections import Counter

numRobots = 10
numSteps = 10000
foodEatingRate = 1
foodStartValue = 100
worldDim = 2
worldLen = 50
numFoods = int(0.3*worldLen ** 2)
deadFoodCount = 0
foodClump = 30
foodSpread = 4
sleep = .0
displayInterval = .1
lastDisplayTime = time.time()
spawnCost = 30
nameList = list(string.ascii_lowercase)
attritionRate = 0.3

# TODO:
# 3D

class Grid():
    def __init__(self):
        self.grid = [[None]*worldLen for i in range(worldLen)]
        self.foodGrid = [[0]*worldLen for i in range(worldLen)]
                

    def reset(self):
        self.grid = [[None]*worldLen for i in range(worldLen)]
        
    def set(self, location, value):
        # draw the bots
        self.grid[location[0]][location[1]] = value

        
    def get(self, location):
        return self.grid[location[0]][location[1]]
        
    def __str__(self):
        plot = ""
        
        for d1 in range(worldLen):
            plot += '|'
            for d2 in range(worldLen):
                char = ' ' 
                
                if self.foodGrid[d1][d2] > 300:
                    char = '#'
                elif self.foodGrid[d1][d2] > 100:
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
            
        
        topRow = '_'*(worldLen + 2)
        bottomRow = '‾'*(worldLen + 2)
        out = topRow + '\n'
        out += plot
        out += bottomRow
        return out


class World():
    def __init__(self):
        self.grid = Grid()
        self.spawn_food(numFoods)
        self.nameList = list(string.ascii_lowercase)

        
        self.locations = [[i]*worldDim for i in range(0, worldLen, worldLen / numRobots)]

        self.robots = []
        self.spawn_robot(numRobots)

    def spawn_robot(self, count):
        for i in range(count):
            loc = [random.randint(0, worldLen - 1) for d in range(worldDim)]
            name = random.choice(self.nameList)
            self.nameList.remove(name)
            if len(self.nameList) == 0:
                self.nameList = list(string.ascii_lowercase)
            bot = Bot(loc, name)
            self.robots.append(bot)
            
    def spawn_food(self, count):

        
        for i in range(count / foodClump):
            locCenter = [random.randint(foodSpread, worldLen - foodSpread - 1) for d in range(worldDim)]
            
            for i in range(foodClump):
                loc = [random.randint(-1*foodSpread,foodSpread) for d in range(worldDim)]
                self.grid.foodGrid[loc[0]+locCenter[0]][loc[1]+locCenter[1]] += foodStartValue

class Bot():
    
    def __init__(self, loc, name):
        self.food = 20
        self.onFood = False
        self.name = name

        self.spawn = False
        self.location = loc
        self.moveThreshold = random.randint(0,100)
        self.moveAmount = random.randint(1,20)
        self.move = [0]*worldDim
    
    def act(self, grid, location):
        
        if self.food > self.moveThreshold:
            self.move = [random.randrange(2*self.moveAmount) - self.moveAmount for d in range(worldDim)]
            
        elif not self.onFood or self.move == [0]*worldDim:
            self.move = [random.randrange(3) - 1 for d in range(worldDim)]
        
#         print 'move', self.move        
        else:
            self.move = [0]*worldDim
#             print 'no move'

        self.spawn = self.food > (spawnCost + sum(self.move))
        
#         if self.food > self.moveThreshold and self.move == [0]*worldDim:
#             print 'lazy', self.food, self.moveThreshold, self.move
     
if __name__ == '__main__':
    print 'go'
    
    while(True):
        w = World()
        allDoneCount = 0
        endNow = False
        for step in range(numSteps):
            
            # occlude bots
            w.grid.reset()
            for bot in w.robots:
                w.grid.set(bot.location,bot.name)
            
            
            # feed the bots
            bot.onFood = False
            for bot in w.robots:
#                 print bot.location, food
                if w.grid.foodGrid[bot.location[0]][bot.location[1]] > foodEatingRate:
                    amount = foodEatingRate
                    
                    bot.food += amount
                    w.grid.foodGrid[bot.location[0]][bot.location[1]] -= amount
                    if w.grid.foodGrid[bot.location[0]][bot.location[1]] <= 0:
                        deadFoodCount += 1
                        if deadFoodCount > foodClump:
                            w.spawn_food(foodClump)
                            deadFoodCount -= foodClump
                    bot.onFood = True
                    
            # act the bots
            bot.act(w.grid, bot.location)
            newLocation = [(bot.location[d] + bot.move[d]) % worldLen for d in range(worldDim)]
            
            foodNeeded = sum(map(abs, bot.move))
            
            if not w.grid.get(newLocation) and bot.food >= foodNeeded and foodNeeded > 0:
                bot.food -= sum(bot.move)
                
                # spawn the bots
                if bot.spawn and bot.food > spawnCost:
                    bot.food -= spawnCost
                    newbot = Bot(bot.location, bot.name)
                    newbot.moveThreshold = max(bot.moveThreshold + random.randint(-1,1), 1)
                    newbot.moveAmount = max(bot.moveAmount + random.randint(-1,1), 1)
                    w.robots.append(newbot)
                else:
                    bot.spawn = False
                    
                # move the bots 
                bot.location = newLocation
                
                allDone = False
                
    
            # remove dead bots
            for bot in w.robots:
                if random.random() < attritionRate:
                    bot.food -= 1
                if bot.food <= 0:
                    w.robots.remove(bot)
                    
# #             rename if all bots have the same name
#             if len(set(bot.name for bot in w.robots)) == 1:
#                 
#                 
#                 for bot in w.robots:
#                     if not len(w.nameList):
#                         w.nameList = list(string.ascii_lowercase)
#                     name = random.choice(w.nameList)
#                     w.nameList.remove(name)
#                     bot.name = name
#             else:
#                 print set(bot.name for bot in w.robots)

                                            
    
            # display
            if time.time() - lastDisplayTime > displayInterval:
                lastDisplayTime = time.time()
                os.system('clear')
                
                print w.grid
                print 'Step', step, 'bot count', len(w.robots), 'foods eaten', deadFoodCount
         
         
                if len(w.robots):
                    varCounter = Counter()
                    for bot in w.robots:
                        varCounter['{} t{:2} a{:2}'.format(bot.name, bot.moveThreshold, bot.moveAmount)] += 1
                    count = 0
                    for varsc in sorted(varCounter, key=varCounter.get, reverse=True):
                        if count < 10:
                            print varsc, varCounter[varsc]
                        count += 1
                     
                    
                    print 'Average thresh:',sum([bot.moveThreshold for bot in w.robots])*1.0/len(w.robots)
                    print 'Average amount:',sum([bot.moveAmount for bot in w.robots])*1.0/len(w.robots)
                    print 'average move:',sum([bot.move[0] for bot in w.robots])*1.0/len(w.robots), sum([bot.move[1] for bot in w.robots])*1.0/len(w.robots)

                
            
            if len(w.robots) == 0:# or len(w.robots) > worldLen:
                print 'all bots dead'
                endNow = True
            
            if allDone:
                allDoneCount += 1
                if allDoneCount > 400:
                    print 'no movement'
                    endNow = True
            else:
                allDoneCount = 0
            
            time.sleep(sleep)
            if endNow:
                break
        
        print 'Stop'
#         if len(w.robots):

#         print [(bot.name,bot.moveThreshold, bot.moveAmount) for bot in w.robots]
        time.sleep(1)
        
        if step == numSteps - 1:
            for bot in w.robots:
                print bot.name.upper(),'f:', '{:3}'.format(bot.food), 'loc:',','.join([str(l) for l in bot.location]), 'move:', bot.move,'thresh',bot.moveThreshold, 'onFood:', bot.onFood, 'spawn:',bot.spawn
         
            break   
        
    print 'Done'