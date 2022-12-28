from time import sleep

INPUT_FILENAME ="input"
TEST1_FILENAME ="test1.txt"
TEST2_FILENAME ="test2.txt"

PART = 1
CLKS_FOR_NOP = 1
CLKS_FOR_ADD = 2

CRT_WIDTH = 40
CRT_HEIGHT = 6

def parse_add(instr: str):
    assert instr.startswith("addx"), f"Callind parse_add() with non-addx instruction"
    amount = int(instr.split(" ")[1])
    return amount


class Device():
    
    def __init__(self, target_strengths: list, width: int, height: int):
        self._clk = 0
        self._x = 1
        self._sprite = range(self._x - 1, self._x + 2)
        self._strength = 0
        self._target_strengths = dict.fromkeys(target_strengths, -1)
        self._width = width
        self._height = height
        self._image = [["." for i in range(self._width)] for j in range(self._height)]
        print(f"CLK: {self._clk}, X: {self._x}")

    def print_screen(self):
        print("="*len(self._image[0]))
        for row in self._image:
            print("".join(row))
        print("="*len(self._image[0]))

    def draw_pixel(self):
        row, col  = (self._clk - 1) // CRT_WIDTH, (self._clk - 1) % CRT_WIDTH
        print(f"row: {row}, col {col}")

        if col in self._sprite:
            self._image[row][col] = "#"
        self.print_screen()

    def update_strength(self):
        self._strength = self._clk * self._x
        if self._clk in self._target_strengths.keys():
            self._target_strengths[self._clk] = self._strength
    
    def get_strengths_sum(self):
        return sum([self._target_strengths[k] for k in self._target_strengths.keys()])

    def run_program(self, program: list):
        instruction: str
        for instruction in program:
            if instruction.startswith("noop"):
                self._clk += 1
                self.draw_pixel()
                self.update_strength()
            elif instruction.startswith("addx"):
                amount = parse_add(instruction)
                self._clk += 1
                self.draw_pixel()
                self.update_strength()
                self._clk += 1
                self.draw_pixel()
                self.update_strength()
                self._x += amount
                print(f"X: {self._x}")
                sprite_center = self._x % CRT_WIDTH
                self._sprite = range(sprite_center - 1, sprite_center + 2)
            else: # instruction not implemented
                continue

if __name__ == "__main__":
    with open(INPUT_FILENAME) as input_f:
        program = input_f.read().splitlines()

    target_clks = range(20, 221, 40)

    d = Device(target_clks, CRT_WIDTH, CRT_HEIGHT)
    d.print_screen()
    d.run_program(program)
    d.print_screen()
    print(f"The sum of the signal strengths is {d.get_strengths_sum()}")
    

    