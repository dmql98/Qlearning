from copy import copy, deepcopy
import csv


# use this to read the .csv table file
# generate different tables:
#   map:            map for agent to explore
#   qTable :        qTable
#   startingPoint:  the starting point of the agent
#   policy:         policy


class Table:
    def __init__(self, filename):
        self.map = readCSV(filename)
        self.qTable = generateQTable(filename)
        self.startingPoint = getStartingPoint(filename)
        self.policy = generatePolicy(filename)
        self.wormholes = getWormHoles(filename)

    # # =========================================================================================================
    # # Not gonna use this part, just for file reading test.
    # def printMap(self):
    #     for x in self.map:  # outer loop
    #         for i in x:  # inner loop
    #             print(i, end="\t")  # print the elements
    #         print('')

    # def printQTable(self):
    #     for x in self.qTable:  # outer loop
    #         for i in x:  # inner loop
    #             print(i, end="\t")  # print the elements
    #         print('')

    # def printMaxQTable(self):
    #     for x in self.qTable:  # outer loop
    #         for i in x:  # inner loop
    #             if isinstance(i, list):
    #                 print(max(i), end="\t")  # print the elements
    #             else:
    #                 print(i, end="\t")  # print the elements
    #         print('')
    # # =========================================================================================================


# read CSV file
def readCSV(file):
    data = []
    with open(file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            tempList = []
            for value in row:
                if value == '':
                    tempList.append('')
                elif value == 'S':
                    tempList.append(int(0))
                elif value == 'X':
                    tempList.append('X')
                elif not value.lstrip("-").isdigit():
                    tempList.append(int(0))
                else:
                    tempList.append(int(value))
            data.append(tempList)
    return data


def generateQTable(file):
    data = []
    with open(file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            tempList = []
            for value in row:
                if value == '0':
                    tempList.append([0.0, 0.0, 0.0, 0.0])
                elif value == 'S':
                    tempList.append([0.0, 0.0, 0.0, 0.0])
                elif value == 'X':
                    tempList.append('X')
                elif not value.lstrip("-").isdigit():
                    tempList.append([0.0, 0.0, 0.0, 0.0])
                else:
                    tempList.append(int(value))
            data.append(tempList)
    return data


def generatePolicy(file):
    data = []
    with open(file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            tempList = []
            for value in row:
                if value == '0':
                    tempList.append('?')
                elif value == 'S':
                    tempList.append('?')
                elif value == 'X':
                    tempList.append('X')
                elif not value.lstrip("-").isdigit():
                    tempList.append('?')
                else:
                    tempList.append(int(value))
            data.append(tempList)
    return data


# get the starting point of the agent
def getStartingPoint(file):
    P = []
    x = 0
    y = 0
    with open(file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            x += 1
            y = 0
            for value in row:
                y += 1
                if value == 'S':
                    P.append(x - 1)
                    P.append(y - 1)

    return P


def getWormHoles(file):
    P = {}
    x = 0
    y = 0
    with open(file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            x += 1
            y = 0
            for value in row:
                y += 1
                if value != 'S' and value != 'X' and not value.lstrip("-").isdigit():
                    if value in P.keys():
                        temp = P.get(value)
                        temp.append(x - 1)
                        temp.append(y - 1)
                        P.update({value: temp})
                    else:
                        P[value] = [x-1, y-1]

    return P
