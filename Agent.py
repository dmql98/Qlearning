import math
import random
import time
import numpy
from copy import deepcopy


class Agent:
    def __init__(self, startLocation, map, qTable, policy, actReword, learningRate, gamma, actSucP, runTime, wormholes):
        self.actions = [0, 1, 2, 3]  # Up, Down, Left, Right
        self.policyDirections = ['^', 'v', '<', '>']
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
        self.wormholes = wormholes

        self.currentLocation = deepcopy(startLocation)
        self.rewordsRecord = []
        self.totalReword = 0

        self.rightMove = 0
        self.totalMoves = 0
        self.movedTwice = 0
        self.movedBackward = 0

    # need to implement
    def learn(self):
        while (time.time() - self.startTime) < self.totalRuntime:
            if (time.time() - self.startTime) < self.totalRuntime * 0.2:
                self.explore()
            else:
                self.exploit()

        # while (time.time() - self.startTime) < self.totalRuntime:
        #     #Explore or exploit and pass in the percentage of time that agent is exploring
        #     self.exploreOrExploit(0.4)

    def exploreOrExploit(self, chance):
        self.currentLocation = deepcopy(self.startLocation)
        reword = 0.0
        while not self.terminated():
            # If action = 0 then explore
            # If action = 1 then exploit
            explore = random.uniform(0, 1) < chance
            if explore:
                nextAct = random.choice(self.actions)
            else:
                nextAct = self.getBestActionFromQtable(self.currentLocation)

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

    def exploit(self):
        self.currentLocation = deepcopy(self.startLocation)
        reword = 0.0
        while not self.terminated():
            nextAct = self.getBestActionFromQtable(self.currentLocation)

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
        while not self.terminated():
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

    # update Policy tabel based on current Q-Table
    def updatePolicy(self):
        x = 0
        y = 0
        for row in self.qTable:
            x += 1
            y = 0
            for value in row:
                y += 1
                if isinstance(value, list) and value != [0.0, 0.0, 0.0, 0.0]:
                    self.policy[x - 1][y - 1] = self.policyDirections[self.getBestActionFromQtable([x - 1, y - 1])]

    # Print the policy table.
    def printPolicy(self):
        self.updatePolicy()
        for x in self.policy:  # outer loop
            for i in x:  # inner loop
                print(i, end="\t")  # print the elements
            print('')

    def updateHeatMap(self, currentLocation):
        x = currentLocation[0]
        y = currentLocation[1]
        if self.map[x][y] == 0:
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
                    totalVists += self.heatMap[x - 1][y - 1]
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
                    tmpValue = deepcopy(self.heatMap[x - 1][y - 1])
                    self.heatMap[x - 1][y - 1] = str(round(tmpValue / totalVisit * 100)) + '%'

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
        print('Mean Reward per Trial:', round(self.totalReword / len(self.rewordsRecord), 2))

    # update
    def updateQTable(self, prelocation, nextAct):
        cx = prelocation[0]
        cy = prelocation[1]
        nx = self.currentLocation[0]
        ny = self.currentLocation[1]

        nextLocationList = deepcopy(self.qTable[nx][ny])
        currentList = deepcopy(self.qTable[cx][cy])
        # When in regular spot
        if isinstance(self.qTable[nx][ny], list):
            currentValue = deepcopy(self.qTable[cx][cy][nextAct])
            self.qTable[cx][cy][nextAct] = round(
                currentValue + self.learningRate * (self.actReword + self.gamma * max(nextLocationList) - currentValue),
                2)
        # When in Terminal Spot
        elif isinstance(self.qTable[nx][ny], int):
            currentValue = deepcopy(self.qTable[cx][cy][nextAct])
            self.qTable[cx][cy][nextAct] = round(
                currentValue + self.learningRate * (self.actReword + self.gamma * nextLocationList - currentValue), 2)

    def outOfGrid(self, row, col):
        if (row < 0 or col < 0) or (row >= len(self.map) or col >= len(self.map[0]) or self.map[row][col] == 'X'):
            return True
        else:
            return False

    def checkWormhole(self, x, y):
        for key in self.wormholes:
            if self.wormholes.get(key)[0] == x and self.wormholes.get(key)[1] == y:
                return [self.wormholes.get(key)[2], self.wormholes.get(key)[3]]
            if self.wormholes.get(key)[2] == x and self.wormholes.get(key)[3] == y:
                return [self.wormholes.get(key)[0], self.wormholes.get(key)[1]]
        return []

    def moveUp(self, location):
        if not self.outOfGrid(location[0] - 1, location[1]):
            location[0] -= 1  # move
        # if stepping into wormhole
        if len(self.checkWormhole(location[0], location[1])) > 0:
            newLocation = self.checkWormhole(location[0], location[1])
            location[0] = newLocation[0]
            location[1] = newLocation[1]
        self.location = location  # update location

    def moveDown(self, location):
        if not self.outOfGrid(location[0] + 1, location[1]):
            location[0] += 1  # move
        # if stepping into wormhole
        if len(self.checkWormhole(location[0], location[1])) > 0:
            newLocation = self.checkWormhole(location[0], location[1])
            location[0] = newLocation[0]
            location[1] = newLocation[1]
        self.location = location  # update location

    def moveRight(self, location):
        if not self.outOfGrid(location[0], location[1] + 1):
            location[1] += 1  # move
        # if stepping into wormhole
        if len(self.checkWormhole(location[0], location[1])) > 0:
            newLocation = self.checkWormhole(location[0], location[1])
            location[0] = newLocation[0]
            location[1] = newLocation[1]
        self.location = location  # update location

    def moveLeft(self, location):
        if not self.outOfGrid(location[0], location[1] - 1):
            location[1] -= 1  # move
        # if stepping into wormhole
        if len(self.checkWormhole(location[0], location[1])) > 0:
            newLocation = self.checkWormhole(location[0], location[1])
            location[0] = newLocation[0]
            location[1] = newLocation[1]
        self.location = location  # update location

    def getMoveUpLocation(self, currentLocation):
        nextLocation = deepcopy(currentLocation)
        if not self.outOfGrid(nextLocation[0] - 1, nextLocation[1]):
            nextLocation[0] -= 1  # move
        return nextLocation

    def getMoveDownLocation(self, currentLocation):
        nextLocation = deepcopy(currentLocation)
        if not self.outOfGrid(nextLocation[0] + 1, nextLocation[1]):
            nextLocation[0] += 1  # move
        return nextLocation

    def getMoveRightLocation(self, currentLocation):
        nextLocation = deepcopy(currentLocation)
        if not self.outOfGrid(nextLocation[0], nextLocation[1] + 1):
            nextLocation[1] += 1  # move
        return nextLocation

    def getMoveLeftLocation(self, currentLocation):
        nextLocation = deepcopy(currentLocation)
        if not self.outOfGrid(nextLocation[0], nextLocation[1] - 1):
            nextLocation[1] -= 1  # move
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
        # do the right action the given percent of time
        if (random.uniform(0, 1) < self.actSucP):
            self.rightMove += 1
            doingAction = action
            self.move(doingAction, currentLocation, 1)
        # if the right action cannot be completed
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

    def terminated(self):
        if ((self.map[self.currentLocation[0]][self.currentLocation[1]]) == 0):
            return False
        else:
            return True
