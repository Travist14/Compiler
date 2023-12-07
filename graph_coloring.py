# https://www.geeksforgeeks.org/welsh-powell-graph-colouring-algorithm/

# takes in an adjacency list and two vertices and adds an edge between them
def addEdge(adj, v1, v2):
    adj[v1].append(v2)
    adj[v2].append(v1)
    return adj


# Assign the first color to the first vertex.
# For each of the remaining V-1 vertices, consider all colors and assign the smallest color which is not present to its adjacent vertices.
# If all the colors are assigned to the adjacent vertices, then assign a new color to the current vertex.
# Time Complexity: O(V^2 + E)
def greedy_coloring(adj, V):
    result = [-1] * V
    result[0] = 0

    available = [False] * V

    for u in range(1, V):
        for i in adj[u]:
            if result[i] != -1:
                available[result[i]] = True

        cr = 0
        while cr < V:
            if available[cr] == False:
                break
            cr += 1

        result[u] = cr

        for i in adj[u]:
            if result[i] != -1:
                available[result[i]] = False

    for u in range(V):
        print(f"Vertex {u}: Color {result[u]}")


# Time Complexity: O(V^2 + E + VlogV)
def welsh_powell_coloring(adj, V):
    result = [-1] * V
    degree = [len(i) for i in adj]
    color = [-1] * V
    available = [False] * V

    sorted_vertices = sorted(range(V), key=lambda x: degree[x], reverse=True) # sorts vertices by degree in descending order

    color[sorted_vertices[0]] = 0

    for u in sorted_vertices[1:]:
        for i in adj[u]:
            if color[i] != -1:
                available[color[i]] = True

        cr = 0
        while cr < V:
            if available[cr] == False:
                break
            cr += 1

        color[u] = cr

        for i in adj[u]:
            if color[i] != -1:
                available[color[i]] = False

    for u in range(V):
        print(f"Vertex {u}: Color {color[u]}")


def perform_graph_coloring():
    g1 = [[] for _ in range(5)]
    g1 = addEdge(g1, 0, 1)
    g1 = addEdge(g1, 0, 2)
    g1 = addEdge(g1, 1, 2)
    g1 = addEdge(g1, 1, 3)
    g1 = addEdge(g1, 2, 3)
    g1 = addEdge(g1, 3, 4)
    print("Coloring of graph 1 (Greedy)")
    greedy_coloring(g1, len(g1))

    g2 = [[] for _ in range(20)]
    g2 = addEdge(g2, 0, 1)
    g2 = addEdge(g2, 0, 2)
    g2 = addEdge(g2, 1, 2)
    g2 = addEdge(g2, 1, 4)
    g2 = addEdge(g2, 2, 4)
    g2 = addEdge(g2, 4, 3)
    g2 = addEdge(g2, 5, 6)
    g2 = addEdge(g2, 5, 15)
    g2 = addEdge(g2, 5, 8)
    g2 = addEdge(g2, 6, 7)
    g2 = addEdge(g2, 6, 8)
    g2 = addEdge(g2, 7, 8)
    g2 = addEdge(g2, 7, 9)
    g2 = addEdge(g2, 8, 9)
    g2 = addEdge(g2, 10, 11)
    g2 = addEdge(g2, 3, 12)
    g2 = addEdge(g2, 7, 12)
    g2 = addEdge(g2, 11, 14)
    g2 = addEdge(g2, 10, 14)
    g2 = addEdge(g2, 10, 6)
    g2 = addEdge(g2, 10, 5)

    print("\nColoring of graph 2 (Greedy)")
    greedy_coloring(g2, len(g2))

    print("\nColoring of graph 1 (Welsh-Powell)")
    welsh_powell_coloring(g1, len(g1))

    print("\nColoring of graph 2 (Welsh-Powell)")
    welsh_powell_coloring(g2, len(g2))


# TODO: liveness stuff, overlap, 
# 