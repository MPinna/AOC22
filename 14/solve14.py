import re
from numpy import sign
INPUT_FILENAME ="input"
TEST1_FILENAME ="test1.txt"

PART = 2

DEBUG = False

SAND_SOURCE_X = 500
SAND_SOURCE_Y = 0

def debug_print(x: str):
    if DEBUG:
        print(x)

def parse_path(path: str):
    coords = []
    pairs = re.split("->", path)
    for pair in pairs:
        x, y = list(map(int,pair.split(",")))
        coords.append([x,y])
    debug_print("[parse_path]")
    debug_print(coords)
    return coords

class Scan:

    def __init__(self):
        self.sand_source_X = SAND_SOURCE_X
        self.sand_source_Y = SAND_SOURCE_Y
        self.width = 0
        self.height = 0
        self.slice = [[]]
        self.resting_sand_units = 0

    def print_slice(self):
        for row in range(self.height):
            print("".join(self.slice[row][self.sand_source_X - 70:self.sand_source_X + 70]))

    def get_size_from_coords(self, coords: list, part=PART):
        for pair in coords:
            x, y = list(map(int,pair.split(",")))
            if x > self.width:
                self.width = x
            if y > self.height:
                self.height = y
    
        self.height += 1
        self.width += 1
        if(part == 2):
            self.height += 2
            self.width *= 2

        self.slice = [["." for i in range(self.width)] for j in range(self.height)]
        print(f"Slice correctly build: W: {self.width}, H: {self.height}")
        
    def build_paths(self, paths: list, part=PART):
        for path in paths:
            coords = parse_path(path)
            for c in range(1, len(coords)):
                startX, startY= coords[c - 1]
                endX, endY = coords[c]
                assert startX == endX or startY == endY, f"Path direction is not horizontal nor vertical"
                debug_print(f"Building path from {startX},{startY} to {endX},{endY}")
                x_increment = sign(endX - startX)
                y_increment = sign(endY - startY)

                if x_increment == 0: # move vertically
                    for i in range(startY, endY + y_increment, y_increment):
                        debug_print(f"Setting cell at {i},{startX} to #")
                        self.slice[i][startX] = "#"
                else: # y_increment == 0, move horizontally
                    for i in range(startX, endX + x_increment, x_increment):
                        debug_print(f"Setting cell at {startY},{i} to #")
                        self.slice[startY][i] = "#"
        if(part == 2):
            debug_print(f"Building floor...")
            for c in range(len(self.slice[0])):
                self.slice[self.height - 1][c] = "#"


    def produce_sand_units(self):

        while(True): # as long as sand units keep coming to rest
            current_x, current_y = self.sand_source_X, self.sand_source_Y
            debug_print(f"Dropping sand unit n. {self.resting_sand_units + 1}")

            # self.print_slice()
            # input()
            while(True): # as long as the single sand unit can keep falling down
                if current_y ==  self.height - 1 : # sand falls down into the void
                    return self.resting_sand_units
                if self.slice[current_y + 1][current_x] not in "#o":
                    current_y += 1 # go down 
                    continue
                else: # go down left.
                    if current_x == 0: # sand has started to fall down-left into the void
                        return self.resting_sand_units
                    else:
                        if self.slice[current_y + 1][current_x - 1] not in "#o":
                            current_y += 1 # go down 
                            current_x -= 1 # go left
                            continue
                        else:
                            if current_x == self.width - 1: # sand falls down-right into the void
                                return self.resting_sand_units
                            if self.slice[current_y + 1][current_x + 1] not in "#o": # go down right
                                current_y += 1 # go down 
                                current_x += 1 # go right
                                continue
                            else: # can't go anywhere
                                self.slice[current_y][current_x] = 'o'
                                self.resting_sand_units += 1
                                break

    def produce_sand_units_v2(self):
        while(True): # as long as sand units keep coming to rest
            current_x, current_y = self.sand_source_X, self.sand_source_Y
            debug_print(f"Dropping sand unit n. {self.resting_sand_units + 1}")

            # self.print_slice()
            # input()
            while(True): # as long as the single sand unit can keep falling down
                if current_y ==  self.height - 1 :
                    print("This should not happen")
                    exit()
                    return self.resting_sand_units
                if self.slice[current_y + 1][current_x] not in "#o":
                    current_y += 1 # go down 
                    continue
                else: # go down left.
                    if current_x == 0: # sand has started to fall down-left into the void
                        print("Sand is falling to the left, this should not happen in part 2")
                        return self.resting_sand_units
                    else:
                        if self.slice[current_y + 1][current_x - 1] not in "#o":
                            current_y += 1 # go down 
                            current_x -= 1 # go left
                            continue
                        else:
                            if current_x == self.width - 1: # sand falls down-right into the void
                                print("Sand is falling to the right, this should not happen in part 2")
                                return self.resting_sand_units
                            if self.slice[current_y + 1][current_x + 1] not in "#o": # go down right
                                current_y += 1 # go down 
                                current_x += 1 # go right
                                continue
                            else: # can't go anywhere
                                self.slice[current_y][current_x] = 'o'
                                self.resting_sand_units += 1
                                if current_x == self.sand_source_X and current_y == self.sand_source_Y:
                                    print("Flow has stopped")
                                    return self.resting_sand_units
                                break

if __name__ == "__main__":
    with open(INPUT_FILENAME) as input_f:
        problem_input = input_f.read()
        paths = problem_input.splitlines()
        coords = re.split('\n|->', problem_input)

    # remove last empty line
    coords.pop()

    scan = Scan()
    scan.get_size_from_coords(coords, PART)
    scan.build_paths(paths, PART)
    if PART == 1:
        resting_units = scan.produce_sand_units()
        print(f"A total of {resting_units} units have come to rest")
    else:
        resting_units = scan.produce_sand_units_v2()
        print(f"A total of {resting_units} units have come to rest")