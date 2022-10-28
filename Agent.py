from http.client import UnknownProtocol
import math
import random
import time
import numpy
from copy import deepcopy


class Agent:
    def __init__(self, startLocation, map, qTable, policy, actReword, learningRate, gamma, actSucP, runTime):
        self.actions = [0, 1, 2, 3] # Up, Down, Left, Right
        self.policyDirections = ['^', 'v', '<', '>']
        self.currentMode = 'explore'
        self.startTime = time.time()

        self.startLocation = deepcopy(startLocation)
        self.map = deepcopy(map)
        self.qTable = deepcopy(qTable)
        self.policy = deepcopy(policy)
        self.heatMap = deepcopy(self.map)
        self.actReword = actReword
        self.learningRate = learningRate
        self.gamma = gamma
        self.actSucP = actSucP
        self.totalRuntime = runTime
        self.totalCells = len(self.map) * len(self.map[0])

        # greedy epsilon
        self.exploreRate = 0.0

        self.exploreRecordMap = deepcopy(policy)

        self.currentLocation = deepcopy(startLocation)
        self.rewordsRecord = []
        self.totalReword = 0
        self.knownPlaces = 0

        self.reachAblePlace = 0
        self.getReachablePlace()

        self.exploreTime = 0


        self.rightMove = 0
        self.totalMoves = 0
        self.movedTwice = 0
        self.movedBackward = 0



    def learn(self):
        outputFile = open("data.txt", "a")
        HundredMSCounter = time.time()

        while (time.time() - self.startTime) < self.totalRuntime:
            # output data
            if time.time() - HundredMSCounter > 0.1:
                outputFile.write(str(round(self.totalReword/len(self.rewordsRecord), 2)))
                outputFile.write('\n')
                HundredMSCounter = time.time()

            
            if self.knownPlaces > (int(self.reachAblePlace * 0.8)):
                self.currentMode = 'exploit'

            else:
                self.currentMode = 'explore'
                if (time.time() - self.startTime) > self.totalRuntime * 0.2:
                    self.currentMode = 'exploit'
            
            # self.currentMode = 'exploit'


            if self.currentMode == 'explore':
                self.explore()
                self.exploreTime += 1

            else:
                self.exploit(self.exploreRate)
            

        

    # explore base on time
    # def learn(self):

    #     while (time.time() - self.startTime) < self.totalRuntime:
    #         if (time.time() - self.startTime) > self.totalRuntime * 0.2:
    #             self.exploit(self.exploreRate)
    #             # print('Exploit......')
    #         else:
    #             self.explore()
    #             # print('Explore!!')
    #             self.exploreTime += 1



    def exploit(self, exploreRate):
        self.currentLocation = deepcopy(self.startLocation)
        reword = 0.0
        while not self.terminated() and (time.time() - self.startTime) < self.totalRuntime:
            self.updateExploreRecord()

            rand = random.uniform(0, 1)
            if rand >= exploreRate:
                nextAct = self.getBestActionFromQtable(self.currentLocation)
            else:
                nextAct = random.choice(self.actions)

            
            preLocation = deepcopy(self.currentLocation)

            self.takeAction(self.currentLocation, nextAct)
            self.updateQTable(preLocation, nextAct)


            self.updateHeatMap(self.currentLocation)
            x = self.currentLocation[0]
            y = self.currentLocation[1]
            list = self.qTable[x][y]

            # Q-learning function
            reword = round(reword + self.actReword, 2)
            # print('=========================================', self.policyDirections[nextAct])
            # print('agent current location: ', self.currentLocation, '//  terminated?', self.terminated(), 'Point: ', reword)
            # self.printMap()
            # self.printMaxQTable()

        reword = round(reword + self.getTerminatedReword(self.currentLocation), 2)
        self.rewordsRecord.append(reword)
        self.totalReword += reword


    # now the agent will only randomly moving around the map
    def explore(self):
            self.currentLocation = deepcopy(self.startLocation)
            reword = 0.0
            while not self.terminated() and (time.time() - self.startTime) < self.totalRuntime:
                self.updateExploreRecord()

                nextAct = random.choice(self.actions)
                preLocation = deepcopy(self.currentLocation)

                self.takeAction(self.currentLocation, nextAct)
                self.updateQTable(preLocation, nextAct)

                self.updateHeatMap(self.currentLocation)
                x = self.currentLocation[0]
                y = self.currentLocation[1]
                list = self.qTable[x][y]

                # Q-learning function
                reword = round(reword + self.actReword, 2)
                # print('=========================================', self.policyDirections[nextAct])
                # print('agent current location: ', self.currentLocation, '//  terminated?', self.terminated(), 'Point: ', reword)
                # self.printMap()
                # self.printMaxQTable()

            reword = round(reword + self.getTerminatedReword(self.currentLocation), 2)
            self.rewordsRecord.append(reword)
            self.totalReword += reword

        # print(time.time() - self.startTime)
        # print('Point', self.rewordsRecord)
        # print('Point', max(self.rewordsRecord))




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

    def printVisitTable(self):
        for x in self.exploreRecordMap:  # outer loop
            for i in x:  # inner loop
                print(i, end="\t")  # print the elements
            print('')

    # update Policy tabel based on current Q-Table
    def updatePolicy(self):
        x = 0
        y = 0
        for row in self.qTable:
            x += 1
            y = 0
            for value in row:
                y += 1
                if isinstance(value, list) and (value != [0.0, 0.0, 0.0, 0.0]):
                        self.policy[x-1][y-1] = self.policyDirections[self.getBestActionFromQtable([x-1, y-1])]

    



    # Print the policy table.
    def printPolicy(self):
        self.updatePolicy()
        for x in self.policy:  # outer loop
            for i in x:  # inner loop
                print(i, end="\t")  # print the elements
            print('')

            
    def updateExploreRecord(self):
        x = self.currentLocation[0]
        y = self.currentLocation[1]
        if self.exploreRecordMap[x][y] == '?':
            self.exploreRecordMap[x][y] = 'V'
            self.knownPlaces += 1


    def updateHeatMap(self, currentLocation):
        x = currentLocation[0]
        y = currentLocation[1]
        if  self.map[x][y] == 0:
            self.heatMap[x][y] += 1


    def printHeatmapVisitTimes(self):
        for x in self.heatMap:  # outer loop
            for i in x:  # inner loop
                print(i, end="\t")  # print the elements
            print('')

    def getHeatmapTotalVisits(self):
        x = 0
        y = 0
        totalVists = 0
        for row in self.map:
            x += 1
            y = 0
            for value in row:
                y += 1
                if value == 0:
                    totalVists += self.heatMap[x-1][y-1]
        return totalVists

    def changeHeatmapIntoPercent(self):
        totalVisit = self.getHeatmapTotalVisits()
        x = 0
        y = 0
        for row in self.map:
            x += 1
            y = 0
            for i in row:
                y += 1
                if i == 0:
                    tmpValue = deepcopy(self.heatMap[x-1][y-1])
                    self.heatMap[x-1][y-1] = str(round(tmpValue/totalVisit * 100)) + '%'

    def printHeatmapPercent(self):
        self.changeHeatmapIntoPercent()
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

    def printMeanReward(self):
        if len(self.rewordsRecord) == self.exploreTime:
            print('The map is too large... Please give me more time')
            print('Or maybe, check if all the places in this map is accessable.')
        
        print('Total trails:', len(self.rewordsRecord))
        print('Total starting explore trails:', self.exploreTime)
        print('Mean Reward per Trial:', round(self.totalReword/len(self.rewordsRecord), 2))

    # update
    def updateQTable(self, preLocation, nextAct):
        cx = preLocation[0]
        cy = preLocation[1]
        nx = self.currentLocation[0]
        ny = self.currentLocation[1]

        nextLocationList = deepcopy(self.qTable[nx][ny])
        currentList = deepcopy(self.qTable[cx][cy])
        #When in regular spot
        if isinstance(self.qTable[nx][ny], list):
            currentValue = deepcopy(self.qTable[cx][cy][nextAct])
            self.qTable[cx][cy][nextAct] = round(currentValue + self.learningRate * (self.actReword + self.gamma * max(nextLocationList) - currentValue), 2)
        #When in Terminal Spot
        elif isinstance(self.qTable[nx][ny], int):
            currentValue = deepcopy(self.qTable[cx][cy][nextAct])
            self.qTable[cx][cy][nextAct] = round(currentValue + self.learningRate * (self.actReword + self.gamma * nextLocationList - currentValue), 2)

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


    def getMoveUpLocation(self, currentLocation):
        nextLocation = deepcopy(currentLocation)
        if not self.outOfGrid(nextLocation[0] - 1, nextLocation[1]):
            nextLocation[0] -= 1 # move
        return nextLocation

    def getMoveDownLocation(self, currentLocation):
        nextLocation = deepcopy(currentLocation)
        if not self.outOfGrid(nextLocation[0] + 1, nextLocation[1]):
            nextLocation[0] += 1 # move
        return nextLocation


    def getMoveRightLocation(self, currentLocation):
        nextLocation = deepcopy(currentLocation)
        if not self.outOfGrid(nextLocation[0], nextLocation[1] + 1):
            nextLocation[1] += 1 # move
        return nextLocation


    def getMoveLeftLocation(self, currentLocation):
        nextLocation = deepcopy(currentLocation)
        if not self.outOfGrid(nextLocation[0], nextLocation[1] - 1):
            nextLocation[1] -= 1 # move
        return nextLocation

    def getNextLocation(self, currentLocation, action):
        if action == 0:
            nextLocation = self.getMoveUpLocation(currentLocation)
            return nextLocation
        elif action == 1:
            nextLocation = self.getMoveDownLocation(currentLocation)
            return nextLocation
        elif action == 2:
            nextLocation = self.getMoveLeftLocation(currentLocation)
            return nextLocation
        elif action == 3:
            nextLocation = self.getMoveRightLocation(currentLocation)
            return nextLocation

    # take the Action 0:Up, 1:Down, 2:Left, 3:Right
    def takeAction(self, currentLocation, action):
        self.totalMoves += 1
        doingAction = -1
        #do the right action the given percent of time
        if(random.uniform(0,1) < self.actSucP):
            self.rightMove += 1
            doingAction = action
            self.move(doingAction, currentLocation, 1)
        #if the right action cannot be completed
        else:
            rand = random.uniform(0, 1)
            # half the time, move the agent two times in indicated direction
            if rand < 0.5:
                self.movedTwice += 1
                doingAction = action
                self.move(doingAction, currentLocation, 2)
            # half the time, move the agent backwards
            else:
                self.movedBackward += 1
                if action == 0:  # if up go down
                    doingAction = 1
                elif action == 1:  # if down go up
                    doingAction = 0
                elif action == 2:  # If Left Go Right
                    doingAction = 3
                elif action == 3:  # If right go left
                    doingAction = 2
                self.move(doingAction, currentLocation, 1)

        # self.move(action, currentLocation, 1)

        # if action == 0:  # Up
        #     self.moveUp(currentLocation)
        # elif action == 1: # Down
        #     self.moveDown(currentLocation)
        # elif action == 2: # Left
        #     self.moveLeft(currentLocation)
        # elif action == 3: # Right
        #     self.moveRight(currentLocation)

    def move(self, action, currentLocation, numTimes):
        for i in range(numTimes):
            if action == 0:  # Up
                self.moveUp(currentLocation)
            elif action == 1:  # Down
                self.moveDown(currentLocation)
            elif action == 2:  # Left
                self.moveLeft(currentLocation)
            elif action == 3:  # Right
                self.moveRight(currentLocation)

    # getters        
    # get the index of the best action from Q-table
    def getBestActionFromQtable(self, currentLocation):
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
    
    def getReachablePlace(self):
        for row in self.qTable:
            for value in row:
                if isinstance(value, list):
                    self.reachAblePlace += 1

    def terminated(self):
        if ((self.map[self.currentLocation[0]][self.currentLocation[1]]) == 0):
            return False
        else:
            return True

