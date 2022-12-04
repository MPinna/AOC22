
INPUT_FILE = "input"
PART = 2

def is_fully_contained(assignment: str):
        sections = [list(map(int, x.split("-"))) for x in assignment.split(",")]
        return (sections[0][0] - sections[1][0]) * (sections[0][1] - sections[1][1]) <= 0

def has_overlap(assignment: str):
        sections = [list(map(int, x.split("-"))) for x in assignment.split(",")]
        return (sections[0][0] - sections[1][1]) * (sections[0][1] - sections[1][0]) <= 0


if __name__ == "__main__":
    with open(INPUT_FILE)  as input_f:
        assignments = input_f.read().splitlines()

    total = 0
    for assignment in assignments:
        if(PART == 1):
            if is_fully_contained(assignment):
                total += 1
        elif(PART == 2):
            if has_overlap(assignment):
                total += 1
        
    print(f"Total is: {total}")
