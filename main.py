from Agent import Agent
from Table import Table


print('input here:')
## get the input from user
# filename = input("Enter file name: ")
# action = input("Enter reward for each action(non-positive): ")
# gamma =  input("Enter Gamma: ")
# runTime = input("How many seconds to run for: ")
# P = input("Enter P(action succeeds) : ")
filename = 'map.csv'
action = 0.04
gamma = 0.9
runTime = 20.0
P = 0.9
print('===========================')

# init
table = Table(filename)
agent = Agent(table.startingPoint, table.map, table.qTable, table.policy, action, gamma, P, runTime)

# Test output
print('===========================')
print('place agent into the map')
agent.printMap()# this is the table with agent on it

print('===========================', '\n Qtable')
agent.printQTable()

# moving test
print('===========================  \n MovingTest' )
agent.takeAction(agent.currentLocation, 0) # 0: Up, 1:Down, 2:Left, 3:Right
agent.takeAction(agent.currentLocation, 0)
agent.printMap()
# print the current agent location on map and if it is terminated
print('agent location: ', agent.location, '//  terminated?', agent.terminated(agent.location, agent.map))



# final result
print('===========================', '\n Policy')
agent.printPolicy()

print('===========================', '\n Heatmap')
agent.printHeatmap()





