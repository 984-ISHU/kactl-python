"""
 * Author: chilli
 * Date: 2019-05-17
 * Source: Wikipedia
 * Description: To obtain a maximum independent set of a graph, find a max
 * clique of the complement. If the graph is bipartite, see MinimumVertexCover.
"""

# For maximum independent set:
# 1. For general graphs: find maximum clique of complement graph
#    Use MaximumClique on the complement adjacency matrix
# 2. For bipartite graphs: use MinimumVertexCover
#    Independent set = all vertices - minimum vertex cover
