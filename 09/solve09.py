from numpy import sign

INPUT_FILENAME ="input"
TEST1_FILENAME ="test1.txt"
TEST2_FILENAME ="test2.txt"

ROPE_LEN = 10

PART = 1

DEBUG = True

def debug_print(debug_str: str):
    if(DEBUG):
        print(debug_str)

def parse_motion(motion: str):
    direction, amount = motion.split(" ")
    return direction, int(amount)

class Grid():

    def __init__(self):
        self._grid_width = 1
        self._grid_height = 1
        self._grid = [[]]
        self._knots = [dict.fromkeys(["x", "y"], 0) for j in range(ROPE_LEN)]

    def set_grid_info(self, motions: list):
        min_x, max_x, min_y, max_y = 0, 0, 0, 0
        current_x, current_y = 0, 0
        for motion in motions:
            direction, amount = parse_motion(motion)
            if direction == "U":
                current_y -= amount
                min_y = min(min_y, current_y)
            elif direction == "D":
                current_y += amount
                max_y = max(max_y, current_y)
            elif direction == "L":
                current_x -= amount
                min_x = min(min_x, current_x)
            elif direction == "R":
                current_x += amount
                max_x = max(max_x, current_x)
            
        self._grid_width = max_x - min_x + 1
        self._grid_height = max_y - min_y + 1
        for knot in self._knots:
            knot["x"] = -min_x
            knot["y"] = -min_y
    
    def print_grid(self):
        print("="*self._grid_width)
        for i in range(self._grid_height):
            row = ""
            for j in range(self._grid_width):
                tile = self._grid[i][j]
                for k in range(ROPE_LEN - 1, 0, -1):
                    if [i, j] == [self._knots[k]["y"], self._knots[k]["x"]]:
                        tile = str(k) 
                if [i, j] == [self._knots[0]["y"], self._knots[0]["x"]]:
                    tile = "H"
                row += tile
            print(row)
        print("="*self._grid_width)
        

    def move_head(self, direction, amount):
        assert direction in "DURL", f"Unexpected direction {direction} when moving head"
        head_x = self._knots[0]["x"] 
        head_y = self._knots[0]["y"] 
        for _ in range(amount): # for every step
            if(direction == "D"): # down
                self._knots[0]["y"] += 1
            elif(direction == "U"): # up
                self._knots[0]["y"] -= 1
            elif(direction == "R"): # right
                self._knots[0]["x"] += 1
            elif(direction == "L"): # left
                self._knots[0]["x"] -= 1
            # self.move_tail()
            self.move_body()
        return

    def move_tail(self):
        # print("Moving tail accordingly")
        delta_x = self._knots[0]["x"] - self._knots[ROPE_LEN - 1]["x"] 
        delta_y = self._knots[0]["y"] - self._knots[ROPE_LEN - 1]["y"] 
        # print(f"Delta x: {delta_x}, delta y: {delta_y}")
        if abs(delta_x) > 1: # if diagonal movement is needed
            self._knots[ROPE_LEN - 1]["x"] += sign(delta_x) # update tail x
            self._knots[ROPE_LEN - 1]["y"] += delta_y # update tail y
        if abs(delta_y) > 1: # if diagonal movement is needed
            self._knots[ROPE_LEN - 1]["y"] += sign(delta_y) # update tail y
            self._knots[ROPE_LEN - 1]["x"] += delta_x # update tail x

        tail_x, tail_y = self._knots[ROPE_LEN - 1]["x"], self._knots[ROPE_LEN - 1]["y"]
        # print(f"Tail is now at: {tail_x},{tail_y}")
        # print("Before:" + self._grid[self._knots[ROPE_LEN - 1]["y"]][self._knots[ROPE_LEN - 1]["x"]])
        # print(f"Marking tail position {self._knots[ROPE_LEN - 1]['x']},{self._knots[ROPE_LEN - 1]['y']} as visited")
        self._grid[self._knots[ROPE_LEN - 1]["y"]][self._knots[ROPE_LEN - 1]["x"]] = "#"
        # self.print_grid()
        return

    def move_body(self):
        for i in range(1, ROPE_LEN):
            delta_x = self._knots[i - 1]["x"] - self._knots[i]["x"] 
            delta_y = self._knots[i - 1]["y"] - self._knots[i]["y"] 
            if abs(delta_x) > 1 or abs(delta_y) > 1: # if diagonal movement is needed
                self._knots[i]["x"] += sign(delta_x) # update tail x
                self._knots[i]["y"] += sign(delta_y) # update tail y
            if(i == ROPE_LEN - 1):
                self._grid[self._knots[i]["y"]][self._knots[i]["x"]] = "#"
        


    def build_grid(self, motions: list):
        self.set_grid_info(motions)
        print("Grid info set.")
        print(f"Grid is W {self._grid_width} x H {self._grid_height}.")
        head_x = self._knots[0]["x"] 
        head_y = self._knots[0]["y"] 
        print(f"Head and tail are at: {head_x},{head_y}")
        print("Building grid...")
 
        # WRONG! This creates a shallow list and updating a single element messes up
        # the whole thing

        # https://stackoverflow.com/questions/62480060/changing-value-of-a-2d-array-element-changes-the-complete-column

        # self._grid = [
        #                 ["."]*self._grid_width
        #             ]*self._grid_height

        # CORRECT

        self._grid = [["." for i in range(self._grid_width)] for j in range(self._grid_height)]
        for motion in motions:
            direction, amount = parse_motion(motion)
            self.move_head(direction, amount)


    def count_visited_positions(self):
        return sum(row.count("#") for row in self._grid)


if __name__ == "__main__":
    with open(INPUT_FILENAME) as input_f:
        motions = input_f.read().splitlines()
    g = Grid()
    print("START")
    g.build_grid(motions)
    visited_positions = g.count_visited_positions()
    print(f"The tail visited {visited_positions} positions")