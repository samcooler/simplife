#coding: utf-8
from world import World
from robot import Robot
import time, random, string, os

from collections import Counter


numSteps = 20000

sleep = .0
displayInterval = 1.0/5
lastDisplayTime = time.time()

# TODO:
# 3D
     
if __name__ == '__main__':
    print 'go'
    
    while(True):
        w = World()
        allDoneCount = 0
        endNow = False
        step = 0
        while(True):
            step += 1
            display = False
            if time.time() - lastDisplayTime > displayInterval:
                os.system('clear')
                display = True
            
            # occlude bots
            w.grid.reset()
            for bot in w.robots:
                w.grid.set(bot.location,bot.name)
            
            
            # feed the bots
            bot.onFood = False
            for bot in w.robots:
#                 print bot.location, food
                if w.grid.foodGrid[bot.location[0]][bot.location[1]] >= w.foodEatingRate:
                    amount = w.foodEatingRate
                    
                    bot.food += amount
                    w.grid.foodGrid[bot.location[0]][bot.location[1]] -= amount
                    w.foodEaten += amount
                    if w.grid.foodGrid[bot.location[0]][bot.location[1]] <= 0:
                        
                        if w.foodEaten > w.foodClump * w.foodStartValue:
                            w.foodEaten -= w.spawn_food(w.foodEaten / w.foodStartValue)
                    bot.onFood = True
                    
                # act the bots
                move, spawn = bot.act(w.grid, bot.location)
                newLocation = [(bot.location[d] + move[d]) % w.worldLen for d in range(w.worldDim)]
                
                foodNeeded = sum(map(abs, move))
                
                if not w.grid.get(newLocation) and bot.food >= foodNeeded and foodNeeded > 0:
                    bot.food -= sum(move)
                    
                    # spawn the bots
                    if spawn and bot.food > w.spawnCost:
                        bot.food -= w.spawnCost
                        newbot = bot.spawn()
                        newbot.location = newLocation
                        w.robots.append(newbot)
                        
                    else:
                    # move the bots 
                        bot.location = newLocation
                
                allDone = False
                
    
                # remove dead bots
                w.remove_dead_robots()
                    
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
            if display:
                lastDisplayTime = time.time()
                
                print w.grid
                print 'Step', step, 'bot count', len(w.robots), 'foods eaten', w.foodEaten
         
         
#                 if len(w.robots):
#                     varCounter = Counter()
#                     for bot in w.robots:
# #                         varCounter['{} t{:2} a{:2}'.format(bot.name, bot.moveThreshold, bot.moveAmount)] += 1
#                         print bot
#                     count = 0
#                     for varsc in sorted(varCounter, key=varCounter.get, reverse=True):
#                         if count < 10:
#                             print varsc, varCounter[varsc]
#                         count += 1
                     
#                     
#                     print 'Average thresh:',sum([bot.moveThreshold for bot in w.robots])*1.0/len(w.robots)
#                     print 'Average amount:',sum([bot.moveAmount for bot in w.robots])*1.0/len(w.robots)
#                     print 'average move:',sum([bot.action[0][0] for bot in w.robots])*1.0/len(w.robots), sum([bot.action[0][1] for bot in w.robots])*1.0/len(w.robots)

                
            
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
        
#         if step == numSteps - 1:
#             for bot in w.robots:
#                 print(str(bot))
#             break   
        
    print 'Done'