from htmlFindEq import eqno
from htmlFindEq import output
from htmlFindEq import paraBreak
import networkx as nx
import matplotlib.pyplot as plt

# Class for Adjacency List for Directed Graphs
class directGraph:
    # Dictionary for directed graph representation
    def __init__(self):
        self.graph = {}

    # Function for adding directed edge
    def addEdge(self, node1, node2):
        # create an empty list for a key node
        if node1 not in self.graph:
            self.graph[node1] = []
        if node2 not in self.graph:
            self.graph[node2] = []
        self.graph[node1].append(node2)

    # Print graph
    def printGraph(self):
        print(self.graph)

    # Retrieve all directed edges
    def getEdges(self, node):
        if node in self.graph:
            return self.graph[node]
        else:
            return []

# BFS function for removing repetitive edges. (Ex. a->b->c then edge a->c would be unecessary)
# Return true if there is already a existing path. Else, false
def bfs(src, dest, directedGraph):
    visited = [src]
    que = [src]
    while que:
        node = que.pop(0)
        if node == dest:
            return True
        for i in directedGraph.getEdges(node):
            if i not in visited:
                visited.append(i)
                que.append(i)
    return False

# Calculating Seed Equation: Finding number of incoming x outgoing nodes
def seedEq(directedGraph):
    max = 0
    eqNum = 'NULL'
    for key, value in directedGraph.graph.items():
        tempMax = 0
        tempMax += len(value)
        for key1, value1 in directedGraph.graph.items():
            if key1 == key:
                continue
            else:
                for i in value1:
                    if key == i:
                        tempMax += 1
        if max < tempMax:
            max = tempMax
            eqNum = key
    print('Seed Equation: ', eqNum)

# Graphing
counter = 0                                                 # Counting number of elements between intervals
adjList = directGraph()                                     # Create Adjacency List Object            
G = nx.DiGraph()                                            # Create Directed Graph

for i in range(len(eqno)):
    if eqno[i][0] == 1:                                         # If scanning through paragraph before first equation, skip since no prior equations for linkage
        continue
    for idx in range(eqno[i][0]-1):                                 # Scanning for possible edges ex. 1 to 3; 1 to 7 (-1 since not looking for current equation number)
        counter = 0                                                 # Counter for number of words between paragraphs/equations
        eqNum = str(eqno[idx][0])                                   # eqNum = current possible edge
        for j in range (paraBreak[i][1]+1, eqno[i][1]-1):           # Iterating through the strings between each equation ex. 433 to 573; 573 to 643
            counter += 1                                            # Increment word counter
            # test = output[j]                                               
            if (eqNum in output[j]) and ('equationlink' in output[j-1]) and ('Fig' not in output[j-2]):         # If correct eq number is in curr element/ 'edgee' marker in previous element/ 'equationlink' is NOT in element before that                         
                if bfs(eqno[idx][0], eqno[i][0], adjList) == False:         # If there is no path between the two edges,
                    adjList.addEdge(eqno[idx][0], eqno[i][0])               # Create an edge
                    G.add_edge(eqno[idx][0], eqno[i][0])                    # Edge from idx to i
        # If number of words between equations is less then arbitrary number (20) 
        # and we are on last iteration of equations, 
        if counter < 20 and (idx+1 == eqno[i][0]-1):      
            # print(eqno[idx][0], ', ', eqno[i][0])                
            adjList.addEdge(eqno[idx][0], eqno[i][0])                       # Set manual edge between two equations. Ex. 6->7, 3->4
            G.add_edge(eqno[idx][0], eqno[i][0])                            # Set manual edge between two equations. Ex. 6->7, 3->4
nx.draw_shell(G, with_labels = True)                                        # Taking graph G, add labels
plt.savefig("DerivationTree.png")                                           # Output onto DerivationTree.png
seedEq(adjList)

# Debugging 
# adjList.printGraph()

# Done this week: - parsed lots of documents to find ways to seperate paragraphs (\n (fail), seperate by S1, p1 (overly complicated), found all class names to be same)
#                 - Created adjacency list Class and bfs variation to make sure a->b->c and a->c doesnt exist
#                 - Calculating Seed Equation (temporary solution)
#                 - Created miscellaneous edge between edges that are close together ex 3->4 or 6->7
#
# TODO LIST:    - Think of ideas for using pre trained Machine Learning model for finding identical texts from conclusion to different areas of text
#               - Ideas for miscellaneous edges: if equations close together, add edge. Incorporating grammar (transition words), Seperate output array into paragraphs
#               - Figure out how to store mathML components 
#               - D3 Tree
#               - If paragraph before equation has capital letter with no period before, equationlink, Fig, eq, parabreak then equation is of important has a name, so shouldnt be any incoming edge
#
# Questions:    - Can i assume my algorithm will be used for papers with 10+ equations?
# has the most subgraphs
# increase paragraph to after equation