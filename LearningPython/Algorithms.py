### Data Structures ###
graph1 = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

### BFS ###

def BFS(graph, node):
    visited = []
    queue = []
    visited.append(node)
    queue.append(node)

    while len(queue) > 0:
        current = queue.pop(0)
        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.append(neighbor)
    return visited


print(BFS(graph1, 'A'))
print(BFS(graph1, 'E'))
