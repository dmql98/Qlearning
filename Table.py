from copy import copy, deepcopy
import csv

class Table:
    def __init__(self, filename):
        self.map = readCSV(filename)
        self.qTable = generateQTable(filename)
        self.sP = getStartingPoint(filename)
        self.policy = generatePolicy(filename)


    # print different output
    def printMap(self):
        for x in self.map:  # outer loop
            for i in x:  # inner loop
                print(i, end="\t")  # print the elements
            print('')
    
            
    def printQTable(self):
        for x in self.qTable:  # outer loop
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
                    tempList.append([0.0, 0.0 ,0.0 ,0.0])
                elif value == 'S':
                    tempList.append([0.0, 0.0 ,0.0 ,0.0])
                elif value == 'X':
                    tempList.append('X')
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
                     P.append(x-1)
                     P.append(y-1)

    return P