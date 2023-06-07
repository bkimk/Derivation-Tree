# this program generate a random directed graph and store it into edges.txt and nodes.txt
from random import randint
import networkx as nx
import matplotlib.pyplot as plt

# replace number with number of nodes from mathematical text
node_num = 30

# generate a scale_free_graph, adjust (a, b, g) to generate the proper graph for test
#                                alpha, beta, gamma
g = nx.scale_free_graph(node_num, 0.05, 0.15, 0.8)
# alpha - Probability for adding a new node connected to an existing node chosen randomly according to the in-degree distribution.
# beta - Probability for adding an edge between two existing nodes. One existing node is chosen randomly according the in-degree 
#        distribution and the other chosen randomly according to the out-degree distribution.
# gamma - Probability for adding a new node connected to an existing node chosen randomly according to the out-degree distribution.
# could use randint() to generate random number of nodes or random (a, b, g)


# break out the usual triangle of (0, 1, 2), otherwise easy to find mothervertex
rand1 = randint(0,2)
rand2 = randint(0,2)
if (rand1 == rand2):
    rand2 = (rand2 + 1) % 2         # if two random number are the same, change one
if (g.has_edge(rand1, rand2)):
    g.remove_edge(rand1, rand2)
elif (g.has_edge(rand2, rand1)):
    g.remove_edge(rand2, rand1)


# write edges into file
edgefile = open("messy_edges.txt", "wb")
nx.write_edgelist(g, edgefile)
edgefile.close()
# the wirted data have form node1 node2 {}
# {} need to be delete

infile = open("messy_edges.txt", "r")
outfile = open("edges.txt", "w")

unwanted = ['{', '}']
lines = infile.readlines()
for line in lines:
        outfile.write(''.join(i for i in line if not i in unwanted))

infile.close()
outfile.close()


# write nodes to node file
nodefile = open("nodes.txt", "wb")
i = 0
while i < node_num:
    nodefile.write(str(i).encode() + "\n".encode('ascii'))
    i+=1
nodefile.close()


# used for visualizing the graph
pos = nx.spring_layout(g, scale = 5)
nx.draw(g, pos, with_labels = True)
plt.show()