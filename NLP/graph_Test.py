from find_Eq import eqno
from find_Eq import output
import networkx as nx
import matplotlib.pyplot as plt

# Counters for third for-loop
initialEq = 1                                             
standardRange = 1                                         

G = nx.DiGraph()                                            # Create Directed Graph
for i in range(len(eqno)):                                  # Iterating through all the equations
    if (isinstance(eqno[i][0], str)):
        initialEq += 1
        continue
    for idx in range(eqno[int(i)][0]):                       # Scanning for possible edges ex. 1 to 3; 1 to 7
        temp = str(eqno[idx][0]) + ')'                       # Added only 1 parantheses because some initial parantheses are cut off
        if (initialEq > 1):                                  # Greater then 0 means there were sub equations ex. 1a, 1b
            initialEq -= 1                                   
            standardRange = initialEq                        # Decrement and update counter
        for j in range (eqno[i-standardRange][1]+1, eqno[i][1]-1):          # Iterating through the strings between each equation ex. 433 to 573; 573 to 643
            # test = output[j]                                               
            if temp in output[j]:                                           # If equation # is within lines; add edge
                G.add_edge(eqno[idx][0], eqno[i][0])                        # Edge from idx to i
    initialEq = 1
    standardRange = 1

nx.draw_shell(G, with_labels = True)                                        # Taking graph G, add labels
plt.savefig("DerivationTree.png")                                           # Output onto DerivationTree.png

# TODO LIST: 
# D3 javascript work on figuring out tree
# Seperate output array into paragraphs
# Ideas for miscellaneous edges
# Check for other ways to draw graph
# Find result equation??? seed equation
# Look for ways to parse Latex Equations




