
import random
from copy import deepcopy
from operator import truediv


class Agent:
    def __init__(self, startLocation, map, qTable, policy, actReword, gamma, actSucP, runTime):
        self.actions = [0, 1, 2, 3] # Up, Down, Left, Right
        
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

        

    # need to implement
    def learn(self):
        x = 1 # doesn't mean anything






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
    

    def takeAction(self, currentLocation, action):
        if action == 0:  # Up
            self.moveUp(currentLocation)
        elif action == 1: # Down
            self.moveDown(currentLocation)
        elif action == 2: # Left
            self.moveLeft(currentLocation)
        elif action == 3: # Right
            self.moveRight(currentLocation)
            


    def terminated(self, location, map):
        if ((map[location[0]][location[1]]) == 0):
            return False
        else:
            return True
        