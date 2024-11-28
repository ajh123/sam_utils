from typing import List, Optional
import tkinter as tk
from tkinter import Canvas

class Node:
    def __init__(self, name: str):
        self.name = name
        self.neighbour_links: List['Link'] = []

    def __str__(self):
        return self.name

    def all_neighbours(self) -> List['Node']:
        result = []
        for link in self.neighbour_links:
            result.append(link.right)
        return result

    def get_weight_to(self, target: 'Node'):
        if target not in self.all_neighbours():
            raise ValueError("Target node is not a neighbour")
        for link in self.neighbour_links:
            if link.right == target:
                if isinstance(link, WeightedLink):
                    return link.weight
                else:
                    return 1
        return None


class Link:
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right


class WeightedLink(Link):
    def __init__(self, left: Node, right: Node, weight: int):
        super().__init__(left, right)
        self.weight = weight


class Graph:
    def __init__(self):
        self.nodes: List[Node] = []
    
    def add_node(self, node: Node) -> Node:
        self.nodes.append(node)
        return node

    def make_link(self, left: Node, right: List[Node], weight: Optional[List[int]] = None):
        if weight is not None:
            r_size = len(right)
            w_size = len(weight)
            if r_size != w_size:
                raise ValueError("Right node list and weight lits must be same length")

        for i in range(0, len(right)):
            node = right[i]
            w = weight[i] if weight is not None else None
            if w is None:
                left.neighbour_links.append(Link(left, node))
            else:
                left.neighbour_links.append(WeightedLink(left, node, w))

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
            for neighbour in current.all_neighbours():
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
                for neighbour in current.all_neighbours():
                    new_path = path[:]
                    new_path.append(neighbour)
                    queue.append(new_path)
                    if neighbour == target:
                        return new_path
                visited[current] = True
        return None

    def dfs_all(self, start: Node) -> Optional[List[Node]]:
        stack: List[Node] = []
        path: List[Node] = []
        visited = {}

        for node in self.nodes:
            visited[node] = False

        stack.append(start)

        while stack:
            current = stack.pop(0)
            if not visited[current]:
                visited[current] = True
                path.append(current)

            for neighbour in current.all_neighbours():
                if not visited[neighbour]:
                    stack.append(neighbour)
        return path

    def dfs_search(self, start: Node, target: Node) -> Optional[List[Node]]:
        if start == target:
            return None
        stack: List[List[Node]] = []
        path: List[Node] = []
        visited = {}

        for node in self.nodes:
            visited[node] = False

        stack.append([start])

        while stack:
            path = stack.pop()
            current = path[-1]
            if not visited[current]:
                visited[current] = True

            for neighbour in current.all_neighbours():
                new_path = path[:]
                new_path.append(neighbour)
                if neighbour == target:
                    return new_path
                if not visited[neighbour]:
                    stack.append(new_path)
        return None
    
    def dijkstra(self, start: Node, target: Node):
        distances = {}
        vistited = {}
        predecessors = {}
        for node in self.nodes:
            distances[node] = float("inf")
            vistited[node] = False
            predecessors[node] = None
        distances[start] = 0
        for _ in range(len(graph.nodes)):
            min_d = float("inf")
            cNode: Optional[Node] = None
            for node in distances:
                if not vistited[node] and distances[node] < min_d:
                    min_d = distances[node]
                    cNode = node
            if cNode is None or cNode == target:
                break
            vistited[cNode] = True
            for node in self.nodes:
                if node in cNode.all_neighbours() and not vistited[node]:
                    alt = distances[cNode] + cNode.get_weight_to(node)
                    if alt < distances[node]:
                        distances[node] = alt
                        predecessors[node] = cNode
        cur = target
        path = []
        while cur is not None:
            path.insert(0, cur)
            cur = predecessors[cur]
            if cur == start:
                path.insert(0, start)
                break
        return path


class GraphVisualizer:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.node_positions = {}
        self.window = tk.Tk()
        self.window.title("Graph Visualizer")
        self.canvas = Canvas(self.window, width=800, height=600, bg="white")
        self.canvas.pack()

    def draw_graph(self):
        self._calculate_positions()
        self._draw_edges()
        self._draw_nodes()
        self.window.mainloop()

    def _calculate_positions(self):
        # Simple circular layout for nodes
        import math
        radius = 200
        center_x = 400
        center_y = 300
        num_nodes = len(self.graph.nodes)
        angle_step = 2 * math.pi / num_nodes

        for i, node in enumerate(self.graph.nodes):
            angle = i * angle_step
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self.node_positions[node] = (x, y)

    def _draw_nodes(self):
        for node, (x, y) in self.node_positions.items():
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue")
            self.canvas.create_text(x, y, text=str(node))

    def _draw_edges(self):
        for node in self.graph.nodes:
            for link in node.neighbour_links:
                x1, y1 = self.node_positions[link.left]
                x2, y2 = self.node_positions[link.right]
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)
                if isinstance(link, WeightedLink):
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2

                    label = str(link.weight)
                    lw = len(label) * 16
                    lsx = mid_x - lw
                    lex = mid_x + lw 


                    self.canvas.create_rectangle(lsx, mid_y, lex, mid_y, )
                    self.canvas.create_text(mid_x, mid_y, text=label, fill="red")



if __name__ == "__main__":
    graph = Graph()
    London = graph.add_node(Node("London"))
    Manchester = graph.add_node(Node("Manchester"))
    York = graph.add_node(Node("York"))
    Liverpool = graph.add_node(Node("Liverpool"))
    Glasgow = graph.add_node(Node("Galsgow"))
    Southhampton = graph.add_node(Node("Southhampton"))
    graph.make_link(London, [Manchester, York, Glasgow], [8, 5, 1])
    graph.make_link(Manchester, [York, Glasgow], [10, 8])
    graph.make_link(York, [London, Liverpool], [1, 5])
    graph.make_link(Liverpool, [Manchester, York, Glasgow], [6, 4, 1])
    graph.make_link(Glasgow, [Liverpool], [10])
    graph.make_link(London, [Southhampton], [1])
    graph.make_link(Manchester, [Southhampton], [5])
    graph.make_link(York, [Southhampton], [3])
    graph.make_link(Liverpool, [Southhampton], [4])
    graph.make_link(Glasgow, [Southhampton], [2])

    print("=== BFS All ===")
    bfs_all = graph.bfs_all(London)
    for node in bfs_all:
        print(node)
    print("=== DFS All ===")
    dfs_all = graph.dfs_all(London)
    for node in dfs_all:
        print(node)
    print("=== BFS Search ===")
    bfs_search = graph.bfs_search(Liverpool, London)
    for node in bfs_search:
        print(node)
    print("=== DFS Search ===")
    dfs_search = graph.dfs_search(Liverpool, London)
    for node in dfs_search:
        print(node)
    print("=== Dijkstra ===")
    dijkstra = graph.dijkstra(Liverpool, London)
    for node in dijkstra:
        print(node)

    visualizer = GraphVisualizer(graph)
    visualizer.draw_graph()