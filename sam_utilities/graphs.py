from typing import List, Optional

class Node:
    def __init__(self, name: str):
        self.name = name
        self.neighbours: List[Node] = []
    
    def __str__(self):
        return self.name

class Graph:
    def __init__(self):
        self.nodes: List[Node] = []
    
    def add_node(self, node: Node) -> Node:
        self.nodes.append(node)
        return node

    def make_link(self, left: Node, right: List[Node]):
        for node in right:
            left.neighbours.append(node)

    def bfs_all(self, start: Node) -> List[Node]:
        queue: List[Node] = []
        path = []
        visited = {}
        for node in self.nodes:
            visited[node] = False
        
        visited[start] = True
        queue.append(start)

        while queue:
            current = queue.pop(0)
            path.append(current)
            for neighbour in self.nodes[self.nodes.index(current)].neighbours:
                if not visited[neighbour]:
                    visited[neighbour] = True
                    queue.append(neighbour)
        return path


    def bfs_search(self, start: Node, target: Node) -> Optional[List[Node]]:
        if start == target:
            return None
        queue = [[start]]
        path: List[Node] = []
        visited = {}
        for node in self.nodes:
            visited[node] = False
        
        while queue:
            path = queue.pop(0)
            current = path[-1]
            if not visited[current]:
                for neighbour in self.nodes[self.nodes.index(current)].neighbours:
                    new_path = path[:]
                    new_path.append(neighbour)
                    queue.append(new_path)
                    if neighbour == target:
                        return new_path
                visited[current] = True
        return None



if __name__ == "__main__":
    graph = Graph()
    node1 = graph.add_node(Node("Node1"))
    node2 = graph.add_node(Node("Node2"))
    node3 = graph.add_node(Node("Node3"))
    node4 = graph.add_node(Node("Node4"))
    node5 = graph.add_node(Node("Node5"))
    graph.make_link(node1, [node2, node3, node5])
    graph.make_link(node2, [node3])
    graph.make_link(node3, [node1, node4])
    graph.make_link(node4, [node2])
    graph.make_link(node5, [node4])

    bfs_all = graph.bfs_all(node1)
    for node in bfs_all:
        print(node)
    print("===")
    bfs_search = graph.bfs_search(node4, node1)
    for node in bfs_search:
        print(node)