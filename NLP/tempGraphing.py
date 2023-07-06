from htmlFindEq import eqno
from htmlFindEq import output
from htmlFindEq import paraBreak
import networkx as nx
import matplotlib.pyplot as plt

# Counters for third for-loop

# initialEq = 1                                             
# standardRange = 1                                         
G = nx.DiGraph()                                            # Create Directed Graph
for i in range(len(eqno)):
    if eqno[i][0] == 1:                                         # If scanning through paragraph before first equation, skip since no prior equations for linkage
        continue
    for idx in range(eqno[i][0]-1):                                 # Scanning for possible edges ex. 1 to 3; 1 to 7 (-1 since not looking for current equation number)
        eqNum = str(eqno[idx][0])                                   # eqNum = current possible edge
        for j in range (paraBreak[i][1]+1, eqno[i][1]-1):           # Iterating through the strings between each equation ex. 433 to 573; 573 to 643
            test = output[j]                                               
            if (eqNum in output[j]) and ('edgee' in output[j-1]) and ('Eq' in output[j-2]):         # If correct eq number is in curr element/ 'edgee' marker in previous element/ 'Eq' in element before that                                      # If equation # is within lines; add edge
                G.add_edge(eqno[idx][0], eqno[i][0])                        # Edge from idx to i
nx.draw_shell(G, with_labels = True)                                        # Taking graph G, add labels
plt.savefig("DerivationTree.png")                                           # Output onto DerivationTree.png


# TODO LIST: 

# Think of ideas for using pre trained Machine Learning model for finding identical texts from conclusion to different areas of text
# Ideas for miscellaneous edges: if equations close together, add edge. Incorporating grammar (transition words), Seperate output array into paragraphs
# Create adjacency matrix -> Do this in order to remove edges that were connected prior. FOr instance if 4->5->6 but 4->6, 4->6 edge should not exist
# Figure out how to store mathML components 