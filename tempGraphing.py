from preProcessing import eqno
from preProcessing import output
from preProcessing import paraBreak
from preProcessing import exten
from preProcessing import results
import numpy as np
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

# DP solution to finding all common substrings (Starting from largest w/o duplicates)
# Taking in 2 equations, will create a matrix showing matching substring
def LongestCommonSubstring(equation1, equation2):
    # Matrix of size length of first equation X length of second equation
    Matrix = [ [0] * len(equation2) for i in range(len(equation1))]
    # Populating Matrix
    for i in range(len(equation1)):
        for j in range(len(equation2)):
            if equation1[i] == equation2[j]:
                if i == 0 or j == 0:
                    Matrix[i][j] = 1
                else:
                    Matrix[i][j] = Matrix[i-1][j-1]+1
            else:
                Matrix[i][j] = 0
    # Finding max substring lengths
    # maxi holds max value in matrix, subLen arr holds all common substring lengths, brk boolean for checking when to break
    maxi = np.amax(Matrix)
    subLen = []
    brk = False
    while maxi > 2:
        # Double For Loop for finding substr with max length
        for i in range(len(equation1)):
            for j in range(len(equation2)):
                # Once found, iterate through area of matrix to see if occupied by any previous substring
                if Matrix[i][j] == maxi:
                    for x in range(i-maxi-1, i):
                        for y in range(j-maxi-1, j):
                            # If space is reserved by any other substring set values to all -1 AND BREAK !!!
                            if Matrix[x][y] == -1:
                                brk == True
                                break
                        # Break to get out of row for loop after iterating through substring area of matrix
                        if brk == True:
                            break
                    # If break boolean was never changed to True, that means no other substring occupied
                    # the current area. Then, add substring length to substring array
                    if brk == False:
                        subLen.append(maxi)
                    # Always set substring area to -1 since has been added to list/already occupied by another substring
                    for x in range(i-int(maxi)-1, i):
                        for y in range(j-int(maxi)-1, j):
                            Matrix[x][y] = -1
                    brk = True
                    break
                else:
                    continue
            if brk == True:
                break
        brk = False
        maxi = np.amax(Matrix)
    # Once Matrix has been iterated, calculate percentage of equation that was shared
    # Change current % after further trials
    if np.sum(subLen)/len(equation1) > 0.25:
        return True
    elif np.sum(subLen)/len(equation2) > 0.25:
        return True
    else:
        return False
# Main Graphing
counter = 0                                                 # Counting number of elements between intervals
adjList = directGraph()                                     # Create Adjacency List Object            
G = nx.DiGraph()                                            # Create Directed Graph
for i in range(len(eqno)):
    if eqno[i][0] == 1:                                         # If scanning through paragraph before first equation, skip since no prior equations for linkage
        continue
    edgeFlag = False                                            # Boolean to check if an edge has been added. If none for an equation, check cosine similarity with all equations before it
    for idx in range(eqno[i][0]-1):                                 # Scanning for possible edges ex. 1 to 3; 1 to 7 (-1 since not looking for current equation number)
        counter = 0                                                 # Counter for number of words between paragraphs/equations
        eqNum = str(eqno[idx][0])                                   # eqNum = current possible edge
        for j in range (paraBreak[i][1]+1, eqno[i][1]-1):           # Iterating through the strings between start and actual equation ex. 433 to 573; 573 to 643
            # counter += 1                                            # Increment word counter
            if (j >= 2 and eqNum in output[j]) and ('equationlink' in output[j-1]) and ('Fig' not in output[j-2]):         # If correct eq number is in curr element/ 'edgee' marker in previous element/ 'equationlink' is NOT in element before that                         
                if bfs(eqno[idx][0], eqno[i][0], adjList) == False:         # If there is no path between the two edges,
                    edgeFlag = True                                         # Edge was added so true
                    adjList.addEdge(eqno[idx][0], eqno[i][0])               # Create an edge
                    G.add_edge(eqno[idx][0], eqno[i][0])                    # Edge from idx to i
        for j in range (eqno[i][1]+1, exten[i][1]):                 # Iterating through the strings between each equation ex. 433 to 573; 573 to 643
            if (j >= 2 and eqNum in output[j]) and ('equationlink' in output[j-1]) and ('Fig' not in output[j-2]):          # If correct eq number is in curr element/ 'edgee' marker in previous element/ 'equationlink' is NOT in element before that                         
                if bfs(eqno[idx][0], eqno[i][0], adjList) == False:         # If there is no path between the two edges,
                    edgeFlag = True
                    adjList.addEdge(eqno[idx][0], eqno[i][0])               # Create an edge
                    G.add_edge(eqno[idx][0], eqno[i][0])                    # Edge from idx to i
    # If no previous edges were added for an equation (node), look for cosine similarity. If greater then 0.5 (arbitrary similarity), add edge
    if edgeFlag == False:
        baseEquation = str(results[i])                                      # change curr mathML element to string
        for idx in range(eqno[i][0]-1):                                     # Scanning for possible edges ex. 1 to 3; 1 to 7 (-1 since not looking for current equation number)
            compareEquation = str(results[idx])                             # Change possible edge equation mathML to vector
            if LongestCommonSubstring(baseEquation, compareEquation) == True:         # If similarity is greater then arbitrary percentage,
                if bfs(eqno[idx][0], eqno[i][0], adjList) == False:
                    adjList.addEdge(eqno[idx][0], eqno[i][0])               # Create an edge
                    G.add_edge(eqno[idx][0], eqno[i][0])                    # Edge from idx to i
# Draw graph and put onto png
nx.draw_shell(G, with_labels = True)                                        # Taking graph G, add labels
plt.savefig("DerivationTree.png")                                           # Output onto DerivationTree.png
# seedEq(adjList)
# Debugging 
# adjList.printGraph()
 
# TODO LIST:
#               - Collecting dataset on MLP group repo (Article ID, equation ID, adjacency list, who labelled it)
#               - Wait to receive mathml converter. Then fix longest common subsequence checking similar substrings
#               - Create script for getting texts with 10+ documents
#               - Find longest path in DAG by dynamic programming to figure out root of tree
#               - Fix error with BFS.
#               - Seed equation (Currently wrong): Conclusion should hold analysis ONLY so find see equation based on outgoing directed edges?? Also, if i take out equation which causes most subgraphs???
#               - overleaf
#               - Ideas for miscellaneous edges: Incorporating grammar (transition words) 
#               - If paragraph before equation has capital letter with no period before, equationlink, Fig, eq, parabreak then equation is of important has a name, so shouldnt be any incoming edge
#               - Make longest Common Substring a DP function 

# Finished:
#               - Tried running sumedh mathml -> equation tree converter
#               - Searched internet for alternatives
#               - Longest Common Substring Equation (Turn into DP function?)
#               - Overleaf