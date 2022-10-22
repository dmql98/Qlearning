import random
import time
import numpy
from copy import deepcopy


class Agent:
    def __init__(self, startLocation, map, qTable, policy, actReword, gamma, actSucP, runTime):
        self.actions = [0, 1, 2, 3] # Up, Down, Left, Right
        self.policyDirections = ['^', 'v', '<', '>']

        self.startLocation = deepcopy(startLocation)
        self.map = deepcopy(map)
        self.qTable = deepcopy(qTable)
        self.policy = deepcopy(policy)
        self.heatMap = deepcopy(self.map)
        self.actReword = actReword
        self.gamma = gamma
        self.actSucP = actSucP
        self.totalRuntime = runTime

        self.currentLocation = deepcopy(startLocation)
        self.rewordsRecord = []

        

    # need to implement
    def learn(self):
        x = 1 # doesn't mean anything


    def explore(self):
        reword = 0.0
        while not self.terminated():
            randAct = random.choice(self.actions)
            self.takeAction(self.currentLocation, randAct)

            reword = round(reword + self.actReword, 2)

            print('=========================================', self.policyDirections[randAct])
            print('agent current location: ', self.currentLocation, '//  terminated?', self.terminated(), 'Point: ', reword)
            self.printMap()
        reword = round(reword + self.getTerminatedReword(self.currentLocation), 2)
        self.rewordsRecord.append(reword)
        print('Point', self.rewordsRecord[0])




    # print different output
    def printMap(self):
        tmp = deepcopy(self.map)
        tmp[self.currentLocation[0]][self.currentLocation[1]] = 'A'        
        for x in tmp:  # outer loop
            for i in x:  # inner loop
                print(i, end="\t")  # print the elements
            print('')
    
            
    def printQTable(self):
        for x in self.qTable:  # outer loop
            for i in x:  # inner loop
                print(i, end="\t")  # print the elements
            print('')

    def printPolicy(self):
        for x in self.policy:  # outer loop
            for i in x:  # inner loop
                print(i, end="\t")  # print the elements
            print('')

    def printHeatmap(self):
        for x in self.heatMap:  # outer loop
            for i in x:  # inner loop
                print(i, end="\t")  # print the elements
            print('')

    def printMaxQTable(self):
        for x in self.qTable:  # outer loop
            for i in x:  # inner loop
                if isinstance(i, list):
                    print(max(i), end="\t")  # print the elements
                else:
                    print(i, end="\t")  # print the elements
            print('')

            
    # update
    def updateQTable(self, location, array):
        x = location[0]
        y = location[1]
        self.qTable[x][y] = array

    def outOfGrid(self, row, col):
        if (row < 0 or col < 0) or (row >= len(self.map)  or col >= len(self.map[0]) or self.map[row][col] == 'X'):
            return True
        else:
            return False
        
    def moveUp(self, location):
        if not self.outOfGrid(location[0] - 1, location[1]):
            location[0] -= 1 # move
        self.location = location # update location
    
    def moveDown(self, location):
        if not self.outOfGrid(location[0] + 1, location[1]):
            location[0] += 1 # move
        self.location = location # update location
    

    def moveRight(self, location):
        if not self.outOfGrid(location[0], location[1] + 1):
            location[1] += 1 # move
        self.location = location # update location
    

    def moveLeft(self, location):
        if not self.outOfGrid(location[0], location[1] - 1):
            location[1] -= 1 # move
        self.location = location # update location
    
    # take the Action 0:Up, 1:Down, 2:Left, 3:Right
    def takeAction(self, currentLocation, action):
        if action == 0:  # Up
            self.moveUp(currentLocation)
        elif action == 1: # Down
            self.moveDown(currentLocation)
        elif action == 2: # Left
            self.moveLeft(currentLocation)
        elif action == 3: # Right
            self.moveRight(currentLocation)

    # getters        
    # get the index of the best action from Q-table
    def getActionFromQtable(self, currentLocation):
        x = currentLocation[0]
        y = currentLocation[1]
        input_list = self.qTable[x][y]
        bestAction = numpy.argmax(input_list)
        return bestAction
    
    def getTerminatedReword(self, currentLocation):
        x = currentLocation[0]
        y = currentLocation[1]
        finalReword = self.map[x][y]
        return finalReword
 
            
    def terminated(self):
        if ((self.map[self.currentLocation[0]][self.currentLocation[1]]) == 0):
            return False
        else:
            return True
        