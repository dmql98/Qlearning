from Agent import Agent
from Table import Table


print('input here:')
## get the input from user
# filename = input("Enter file name: ")
# action = float(input("Enter reward for each action(non-positive): "))
# learningRate = float(input("Enter learning rate: "))
# gamma =  float(input("Enter Gamma: "))
# runTime = float(input("How many seconds to run for: "))
# P = float(input("Enter P(action succeeds) : "))
filename = 'test_map.tsv'
action = -0.04
gamma = 0.9
learningRate = 0.1
runTime = 5.0
P = 0.0

print('Reading Filename: ', filename)
print('Reward Per Action: ', action)
print('Gamma: ', gamma)
print('How Many Seconds to Run For: ', runTime)
print('P(Action Succeeds/Transition Model: ', P)
print('Learning Rate: ', learningRate)
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
agent.learn()



# print the current agent location on map and if it is terminated
# print('agent current location: ', agent.currentLocation, '//  terminated?', agent.terminated())

print('===========================', '\n Qtable')
agent.printMaxQTable()
print()
agent.printQTable()

# final result
print('===========================================', '\n Policy')
agent.printPolicy()

print('===========================================', '\n Heatmap')
# agent.printHeatmapVisitTimes()
# print('total visit', agent.getHeatmapTotalVisits())
agent.printHeatmapPercent()

print('===========================================')
agent.printMeanReward()

# print("Did the Correct Thing: ", agent.rightMove/agent.totalMoves)
# print("Moved Twice: ", agent.movedTwice/agent.totalMoves)
# print("Moved Backward: ", agent.movedBackward/agent.totalMoves)
