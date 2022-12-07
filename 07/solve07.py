import networkx as nx
from matplotlib import pyplot as plt

INPUT_FILENAME = "input"

PART = 2
TOTAL_SPACE = 70000000
REQUIRED_SPACE = 30000000

DEBUG = False


def parse_ls_command(to_parse: str) -> list:
    command, *content = to_parse.splitlines() # hehe nice unpacking operator
    assert(command == "ls"), f"ls command expected, got: {command}"
    return content


class AOC_FileSystem:

    def __init__(self):
        self.tree = nx.DiGraph()
        self.has_root = False
        self.pwd = None

    def show_graph_image(self):
        if(DEBUG):
            plt.tight_layout()
            nx.draw_networkx(self.tree, arrows=True)
            plt.show()

    def change_directory(self, dest: str):
        if (not self.has_root) and dest == "/": # base case when starting to build
            self.tree.add_node("/")
            self.tree.nodes["/"]["type"] = "dir"
            self.tree.nodes["/"]["size"] = 0
            self.has_root = True
            self.pwd = dest
        elif(dest == ".."):
            if(self.pwd != "/"): # "cd .." when pwd is / should have no effect
                self.pwd = list(self.tree.predecessors(self.pwd))[0]
        else:
            dest_full_path = self.pwd + dest + "/"
            assert dest_full_path in list(self.tree.nodes()), f"cd: {dest_full_path}: no such file or directory"
            self.pwd = dest_full_path

    def add_content_of_dir(self, content: list):
        self.show_graph_image()
        entry: str
        for entry in content:
            info, entry_name = entry.split(" ")
            full_path: str = self.pwd + f"{entry_name}"
            
            if info == "dir":
                full_path += "/"
                self.tree.add_node(full_path)
                self.tree.nodes[full_path]["type"] = "dir"
                self.tree.nodes[full_path]["size"] = 0

            else: # it's a file
                size = int(info)
             
                self.tree.add_node(full_path)
                self.tree.nodes[full_path]["type"] = "file"
                self.tree.nodes[full_path]["size"] = size
                
                slash_indices = [i for i in range(len(full_path)) if full_path[i] == "/"]
                for index in slash_indices:
                    target_dir = full_path[:index + 1]
                    self.tree.nodes[target_dir]["size"] += size
            
            self.tree.add_edge(self.pwd, full_path)

    def build_FS(self, terminal_output: str):
        for part in terminal_output:
            if(part.startswith("cd")):
                dest = part.split(" ")[1]
                self.change_directory(dest)
            elif(part.startswith("ls")):
                content = parse_ls_command(part)
                self.add_content_of_dir(content)

        self.show_graph_image()
        assert nx.is_tree(self.tree), f"Error during construction of FS. Not a tree"
        print("FS tree correctly built")


    def find_small_directories(self, max_size=100000):
        small_directories = [entry for entry in list(self.tree.nodes(data=True))
                                                if entry[1]["type"] == "dir"
                                                and entry[1]["size"] < max_size
                            ]
        return small_directories
    
    def find_big_directories(self, min_size):
        big_directories = [entry for entry in list(self.tree.nodes(data=True))
                                        if entry[1]["type"] == "dir"
                                        and entry[1]["size"] > min_size
                            ]
        return big_directories
        
    def find_dir_to_delete(self, required_space=REQUIRED_SPACE):
        free_space = TOTAL_SPACE - self.tree.nodes["/"]["size"]
        space_to_free = required_space - free_space

        to_delete = None
        for dir in self.find_big_directories(min_size=space_to_free):
            if(to_delete == None or dir[1]["size"] < to_delete[1]["size"]):
                to_delete = dir
        return to_delete
                

if __name__ == "__main__":

    with open(INPUT_FILENAME) as input_f:
        terminal_output = [command.lstrip()[:-1] for command in input_f.read().split("$")]

    AOC_FS = AOC_FileSystem()
    AOC_FS.build_FS(terminal_output)

    if(PART == 1):
        total_size = 0

        small_dirs = AOC_FS.find_small_directories()
        for dir in small_dirs:
            total_size += dir[1]["size"]

        print(f"The total size of small directories is: {total_size}")
    elif(PART == 2):
        to_delete = AOC_FS.find_dir_to_delete()
        name, size = to_delete[0], to_delete[1]["size"]
        print(f"You have to delete directory {name}, which has a size of {size} bytes")
