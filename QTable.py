from copy import copy, deepcopy
import csv
from re import template

from copy import copy, deepcopy
import csv
from re import template
from typing_extensions import Self

class QTable:
    def __init__(self, filename):
        self.qTable = readCSV(filename)


    def getQTable(self):
        return self.qTable


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

    def updateQTable(self, location, number):
        x = location[0]
        y = location[1]
        self.qTable[x][y] = number

    

# read CSV file
def readCSV(file):
    data = []
    with open(file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            tempList = []
            for value in row:
                if value == '0':
                    tempList.append([0,0,0,0])
                elif value == 'S':
                    tempList.append([0,0,0,0])
                elif value == 'X':
                    tempList.append('X')
                else:
                    tempList.append(int(value))
            data.append(tempList)
    return data

    
    