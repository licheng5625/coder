


import networkx as nx
G=nx.Graph()




#elist=[('3','1',1.0),('3','2',1.0),('2','1',1.0),('2','5',1),('4','5',1),('6','4',1),('6','5',1),('6','7',1),('1','8',1),('9','8',1),('7','8',1),('7','9',1)]
elist=[ ('2','1',1.0),('2','5',1),('4','5',1),('6','4',1),('6','5',1),('6','7',1),('1','8',1),('7','8',1),('8','9',1),('7','9',1)]
G.add_weighted_edges_from(elist)
print(nx.betweenness_centrality(G,normalized=False))

print(nx.edge_betweenness_centrality(G,normalized=False))
print([p for p in nx.all_shortest_paths(G,'1','6')])