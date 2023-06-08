from find_Eq import eqno
from find_Eq import output
import networkx as nx
import matplotlib.pyplot as plt
  

G = nx.DiGraph()                                    # Create Directed Graph
for i in range(1,len(eqno)):                        # Iterating through all the equations
    for idx in range(1, i+1):                       # Scanning for possible edges ex. 1 to 3; 1 to 7
        temp = str(idx) + ')'                       # Added only 1 parantheses because some initial parantheses are cut off
        for j in range (eqno[i]+1, eqno[i+1]-1):        # Iterating through the strings between each equation ex. 433 to 573; 573 to 643
            test = output[j]                            # Debugging variable
            if temp in output[j]:                       # If equation # is within lines; add edge
                G.add_edge(idx, i+1)                    # Edge from idx to i+1

nx.draw_shell(G, with_labels = True)                          # Taking graph G, add labels
plt.savefig("DerivationTree.png")                       # Output onto DerivationTree.png




