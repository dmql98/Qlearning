from Agent import Agent
from Table import Table


print('input here:')
## get the input from user
filename = input("Enter file name: ")
action = float(input("Enter reward for each action(non-positive): "))
learningRate = float(input("Enter learning rate: "))
gamma =  float(input("Enter Gamma: "))
runTime = float(input("How many seconds to run for: "))
P = float(input("Enter P(action succeeds) : "))
# filename = 'map.csv'
# action = -0.04
# gamma = 0.9
# learningRate = 0.1
# runTime = 1.0
# P = 0.9
print('===========================================')

# init
table = Table(filename)
agent = Agent(table.startingPoint, table.map, table.qTable, table.policy, action, learningRate, gamma, P, runTime)

# # Test output
print('===========================================')
print('place agent into the map, A for agent')
agent.printMap()# this is the table with agent on it




# exploring test
print('===========================================  \n Learning..............' )
agent.explore()



# print the current agent location on map and if it is terminated
# print('agent current location: ', agent.currentLocation, '//  terminated?', agent.terminated())

# print('===========================', '\n Qtable')
# agent.printMaxQTable()

# final result
print('===========================================', '\n Policy')
agent.printPolicy()

print('===========================================', '\n Heatmap')
# agent.printHeatmapVisitTimes()
# print('total visit', agent.getHeatmapTotalVisits())
agent.printHeatmapPercent()

print('===========================================')
agent.printMeanReward()
