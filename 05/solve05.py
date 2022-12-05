from string import ascii_lowercase, ascii_uppercase

INPUT_FILE = "input"
PART = 2

def parse_step(raw_step: str):
    step_numbers_string = ("".join([c for c in raw_step if c not in ascii_lowercase])).split("  ")
    return list(map(int, step_numbers_string))

def build_stacks(raw_stacks: list):
    num_of_stacks = int(raw_stacks[-1].split("  ")[-1])
    stacks = {}
    stack_line: str = raw_stacks[-1]
    for stack_number in range(1, num_of_stacks + 1):
        stack_index = stack_line.index(str(stack_number))
        stacks[stack_number] = []
        for stack_floor in range(len(raw_stacks) - 1, -1, -1):
            crate = raw_stacks[stack_floor][stack_index]
            if(crate in ascii_uppercase):
                stacks[stack_number].append(crate)

    return stacks

def execute_step(stacks: dict, step: tuple):
    amount, src, dest = step
    work = []
    for _ in range(amount):
        work += stacks[src].pop()
    
    if(PART == 1):
        stacks[dest] += work
    elif(PART == 2):
        stacks[dest] += work[::-1]


if __name__ == "__main__":
    with open(INPUT_FILE)  as input_f:
        raw_stacks, raw_steps = [part.split("\n") for part in input_f.read().split("\n\n")]

    stacks: dict = build_stacks(raw_stacks)

    raw_steps.pop() # remove empty line at the end of file

    for raw_step in raw_steps:
        step = parse_step(raw_step)
        execute_step(stacks, step)
    
    top_crates = "".join([stacks[stack_id][-1] for stack_id in list(stacks.keys())])

    print(f"The answer is: {top_crates}")