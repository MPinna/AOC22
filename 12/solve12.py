from pprint import pprint
import time
from math import floor
from datetime import timedelta
import networkx as nx

INPUT_FILENAME ="input"
MINITEST_FILENAME ="minitest.txt"
TEST2_FILENAME ="test2.txt"

PART = 1

DEBUG = False

def debug_print(s: str):
    if(DEBUG):
        print(s)


class Heightmap():

    def __init__(self):
        self.height, self.width = 0, 0
        self.graph = nx.DiGraph()
        self.start_coords = [0, 0]
        self.end_coords = [0, 0]

    def add_edges_to_node(self, node_row: int, node_col: int):
        node_id = str(node_row) + "," + str(node_col)
        node_value = self.graph.nodes[node_id]["value"]
        
        # only adding edges to node UP and node LEFT
        # so it can be done while inserting the nodes in build_graph()
        if node_row > 0: # UP
            node_above_id = str(node_row - 1) + "," + str(node_col)
            node_above_value = self.graph.nodes[node_above_id]["value"]
            debug_print(f"\t    {node_above_value}")
            delta = ord(node_above_value) - ord(node_value)
            if delta < 2: # if destination is not too high
                self.graph.add_edge(node_id, node_above_id, weight=1)
            if -1*delta < 2: # if current position is not too high 
                self.graph.add_edge(node_above_id, node_id, weight=1)


        if node_col > 0: # LEFT
            node_left_id = str(node_row) + "," + str(node_col - 1)
            node_left_value = self.graph.nodes[node_left_id]["value"]
            delta = ord(node_left_value) - ord(node_value)
            if delta < 2: # if destination is not too high
                self.graph.add_edge(node_id, node_left_id, weight=1)
            if -1*delta < 2: # if current position is not too high 
                self.graph.add_edge(node_left_id, node_id, weight=1)

    def print_full_graph(self):
        #TODO fix edges print
        board = [[" " for i in range(self.width*2 - 1)] for j in range(self.height*2 - 1)]

        for i in range(len(board)):
            for j in range(len(board[0])):
                if i % 2 == 0 and j % 2 == 0:
                    node_id = str(i//2) + "," + str(j//2)
                    board[i][j] = str((self.graph.nodes[node_id]["value"])).upper()
                elif i % 2 == 0 and j % 2 == 1: # left and right
                    node_left_id = node_id = str(i//2) + "," + str((j - 1)//2)
                    node_right_id = node_id = str(i//2) + "," + str((j + 1)//2)
                    if self.graph.has_edge(node_left_id, node_right_id):
                        board[i][j] = "-"
                elif i % 2 == 1 and j % 2 == 0: # up and down
                    node_above_id = node_id = str((i-1)//2) + "," + str((j)//2)
                    node_below_id = node_id = str((i+1)//2) + "," + str(j//2)
                    if self.graph.has_edge(node_above_id, node_below_id):
                        board[i][j] = "|"

        for row in board:
            print("" + "".join(row) + "")
                    
        
    def build_graph(self, raw_heightmap: list):
        self.height = len(raw_heightmap)
        self.width = len(raw_heightmap[0])

        for row in range(self.height):
            for col in range(self.width):
                node_id = str(row) + "," + str(col)
                self.graph.add_node(node_for_adding=node_id)
                node_value = raw_heightmap[row][col]
                if(node_value == 'S'): # mark start point
                    self.start_coords = row, col
                    node_value = 'a'
                elif(node_value == 'E'): # mark end point
                    self.end_coords = row, col
                    node_value = 'z'

                self.graph.nodes[node_id]["value"] = node_value

                self.add_edges_to_node(row, col)

    def get_shortest_path_length(self):
        start_id = str(self.start_coords[0]) + "," + str(self.start_coords[1])
        end_id = str(self.end_coords[0]) + "," + str(self.end_coords[1])
        print(f"Searching path from {start_id} to {end_id}")
        length = -1
        try:
            length = nx.shortest_path_length(self.graph, start_id, end_id)
        except nx.NetworkXNoPath:
            print('No path')
        return length

    def get_shortest_path_from_bottom(self):
        bottom_nodes = [n for n, attrs in self.graph.nodes(data=True) if attrs['value']=="a"]

        min_path = None
        end_id = str(self.end_coords[0]) + "," + str(self.end_coords[1])

        for node in bottom_nodes:
            try:
                path = nx.shortest_path_length(self.graph, node, end_id)
            except nx.NetworkXNoPath:
                continue
            if min_path == None:
                min_path = path
            else:
                if path < min_path:
                    min_path = path
        return min_path
        


if __name__ == "__main__":
    with open(INPUT_FILENAME) as input_f:
        raw_heightmap = input_f.read().splitlines()

    start_time = time.monotonic()
    g = Heightmap()
    g.build_graph(raw_heightmap)
    len = g.get_shortest_path_length()

    end_time = time.monotonic()

    print(f"Shortest path length is {len}")
    d = timedelta(seconds=end_time - start_time)
    print(f"Part 1 took {d} s to execute")
    pt_2_start = time.monotonic()
    min_len = g.get_shortest_path_from_bottom()
    pt_2_end = time.monotonic()
    print(f"Shortest path from bottom is {min_len}")
    d = timedelta(seconds=pt_2_end - pt_2_start)
    print(f"Part 2 took {d} s to execute")
