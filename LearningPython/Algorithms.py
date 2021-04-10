### Data Structures ###
graph1 = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

arr1 = [3, 0, -3, 2, 1, -1]
arr2 = [2, 3, 4, -2, -5]
arr3 = [-2, -2, 1, 3, 4]

string1 = 'abcde'
string2 = 'Helko'

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

### DFS ###
def DFS(graph, node):
    visited = []
    DFSIteration(graph, node, visited)
    return visited


def DFSIteration(graph, node, visited):
    if node not in visited:
        visited.append(node)
        for neighbor in graph[node]:
            DFSIteration(graph, neighbor, visited)


print(DFS(graph1, 'A'))
print(DFS(graph1, 'E'))

### biggest opposite numbers o(n)###

def FindBiggestOpposite(array):
    biggest = -1
    dict = {}
    for number in array:
        dict[number] = True
        if (-1*number) in dict:
            if abs(number) > biggest:
                biggest = abs(number)

    if biggest != -1:
        return biggest
    else:
        return None


print(FindBiggestOpposite(arr1))
print(FindBiggestOpposite(arr2))
print(FindBiggestOpposite(arr3))


### string encrypt and decrypt ###
def StringEncrypt(string, key):
    res = ''
    for char in string:
        res += key[(ord(char.lower()) - 97)]
    return res

def StringDecrypt(string, key):
    res = ''
    for char in string:
        index = key.index(char)
        res += chr(index + 97)
    return res

print(StringEncrypt(string1, string2))
print(StringDecrypt('Hello', string2))

