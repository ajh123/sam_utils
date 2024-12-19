from typing import List, Optional
import tkinter as tk
from tkinter import Canvas, Scrollbar

class Node:
    def __init__(self, name: str, pos_x=None, pos_y=None):
        self.name = name
        self.neighbour_links: List['Link'] = []
        self.pos_x = pos_x
        self.pos_y = pos_y

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
                raise ValueError("Right node list and weight lists must be same length")

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
        # Initialize dictionaries to store distances, visited status, and predecessors of each node.
        distances = {}  # Shortest known distance to each node from the start.
        visited = {}    # Tracks whether a node has been visited.
        predecessors = {}  # Stores the preceding node for the shortest path to reconstruct the path later.

        # Initialize all nodes with default values.
        for node in self.nodes:
            distances[node] = float("inf")  # Set initial distances to infinity (unknown).
            visited[node] = False           # Mark all nodes as unvisited.
            predecessors[node] = None       # No predecessors at the start.

        # Set the distance to the start node to 0 since it's the starting point.
        distances[start] = 0

        # Iterate over all nodes to find the shortest path to each.
        for _ in range(len(graph.nodes)):
            min_d = float("inf")  # Initialize the minimum distance as infinity.
            cNode: Optional[Node] = None  # Variable to track the current node with the smallest distance.

            # Find the unvisited node with the smallest known distance.
            for node in distances:
                if not visited[node] and distances[node] < min_d:
                    min_d = distances[node]
                    cNode = node

            # If no unvisited nodes remain or we've reached the target, exit the loop.
            if cNode is None or cNode == target:
                break

            # Mark the current node as visited.
            visited[cNode] = True

            # Update distances for all unvisited neighbors of the current node.
            for node in self.nodes:
                if node in cNode.all_neighbours() and not visited[node]:
                    # Calculate the alternative distance to the neighbor through the current node.
                    alt = distances[cNode] + cNode.get_weight_to(node)
                    if alt < distances[node]:
                        # Update the distance and predecessor if the alternative distance is shorter.
                        distances[node] = alt
                        predecessors[node] = cNode

        # Reconstruct the shortest path from the target to the start using predecessors.
        cur = target
        path = []
        while cur is not None:
            path.insert(0, cur)  # Add the current node to the path.
            cur = predecessors[cur]  # Move to the predecessor.
            if cur == start:  # If the start node is reached, add it and stop.
                path.insert(0, start)
                break

        # Return the reconstructed path.
        return (path, distances[target])


class GraphVisualizer:
    def __init__(self, graph):
        self.graph = graph
        self.node_positions = {}
        self.window = tk.Tk()
        self.window.title("Graph Visualizer")

        self.canvas = Canvas(self.window, width=800, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.h_scroll = Scrollbar(self.window, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scroll = Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.canvas.bind("<MouseWheel>", self._zoom)
        self.canvas.bind("<ButtonPress-1>", self._start_pan)
        self.canvas.bind("<B1-Motion>", self._do_pan)

        self.scale = 1.0

    def draw_graph(self):
        self._calculate_positions()
        self._draw_graph()
        self.window.mainloop()

    def _calculate_positions(self):
        import math
        radius = 200
        center_x = 400
        center_y = 300
        num_nodes = len(self.graph.nodes)
        angle_step = 2 * math.pi / num_nodes

        for i, node in enumerate(self.graph.nodes):
            angle = i * angle_step
            if node.pos_x is None and node.pos_y is None:
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                self.node_positions[node] = (x, y)
            else:
                self.node_positions[node] = (node.pos_x, -node.pos_y)

    def _draw_graph(self):
        self.canvas.delete("all")
        self._draw_edges()
        self._draw_nodes()

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
                    self.canvas.create_text(mid_x, mid_y, text=str(link.weight), fill="red")

    def _zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.scale *= factor
        for node in self.node_positions:
            x, y = self.node_positions[node]
            self.node_positions[node] = (x * factor, y * factor)
        self._draw_graph()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _do_pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)



if __name__ == "__main__":
    graph = Graph()
    London = graph.add_node(Node("London", -0.118092, 51.509865))
    Manchester = graph.add_node(Node("Manchester", -2.244644, 53.483959))
    York = graph.add_node(Node("York", -1.080278, 53.958332))
    Liverpool = graph.add_node(Node("Liverpool", -2.983333, 53.400002))
    Glasgow = graph.add_node(Node("Glasgow", -4.251433, 55.860916))
    Southampton = graph.add_node(Node("Southampton", -1.404219, 50.902531))
    Birmingham = graph.add_node(Node("Birmingham", -1.890401, 52.486244))
    Oxford = graph.add_node(Node("Oxford", -1.257677, 51.752022))
    Windsor = graph.add_node(Node("Windsor", -0.607558, 51.481727))
    Carlisle = graph.add_node(Node("Carlisle", -2.944000, 54.890999))
    Edinburgh = graph.add_node(Node("Edinburgh", -3.188267, 55.953251))
    Leeds = graph.add_node(Node("Leeds", -1.549077, 53.800755))
    Bristol = graph.add_node(Node("Bristol", -2.587910, 51.454514))
    Newcastle = graph.add_node(Node("Newcastle", -1.617439, 54.978252))

    # Connecting cities with two-way connections
    graph.make_link(London, [Oxford, Windsor, Southampton, Bristol], [56, 25, 79, 118])
    graph.make_link(Manchester, [Liverpool, Leeds, Carlisle, Birmingham], [35, 44, 120, 86])
    graph.make_link(York, [Leeds, Newcastle, Birmingham], [24, 84, 132])
    graph.make_link(Liverpool, [Manchester, Birmingham, Bristol, Carlisle], [35, 98, 177, 122])
    graph.make_link(Glasgow, [Edinburgh, Carlisle], [47, 96])
    graph.make_link(Southampton, [London, Oxford, Windsor, Bristol], [79, 66, 71, 64])
    graph.make_link(Birmingham, [Oxford, Liverpool, Manchester, Leeds, York, Bristol], [85, 98, 86, 118, 132, 88])
    graph.make_link(Oxford, [London, Birmingham, Southampton], [56, 85, 66])
    graph.make_link(Windsor, [London, Southampton], [25, 71])
    graph.make_link(Carlisle, [Glasgow, Newcastle, Manchester, Liverpool], [96, 60, 120, 122])
    graph.make_link(Edinburgh, [Glasgow, Newcastle, Carlisle], [47, 121, 92])
    graph.make_link(Leeds, [Manchester, York, Birmingham, Newcastle], [44, 24, 118, 97])
    graph.make_link(Bristol, [London, Liverpool, Birmingham, Southampton, Oxford], [118, 177, 88, 64, 75])
    graph.make_link(Newcastle, [Carlisle, York, Edinburgh, Leeds], [60, 84, 121, 97])


    # print("=== BFS All ===")
    # bfs_all = graph.bfs_all(London)
    # for node in bfs_all:
    #     print(node)
    # print("=== DFS All ===")
    # dfs_all = graph.dfs_all(London)
    # for node in dfs_all:
    #     print(node)
    # print("=== BFS Search ===")
    # bfs_search = graph.bfs_search(Liverpool, London)
    # for node in bfs_search:
    #     print(node)
    # print("=== DFS Search ===")
    # dfs_search = graph.dfs_search(Liverpool, London)
    # for node in dfs_search:
    #     print(node)
    print("=== Dijkstra ===")
    dijkstra = graph.dijkstra(Glasgow, Southampton)
    for node in dijkstra[0]:
        print(node)
    print(f"Distance: {dijkstra[1]} miles")

    visualizer = GraphVisualizer(graph)
    visualizer.draw_graph()