import numpy as np

INPUT_FILENAME = "input"
PART = 2

if __name__ == "__main__":
    with open(INPUT_FILENAME) as inputfile:
        lines = inputfile.read().splitlines()
    separators_indices =  [-1] + [i for i, line in enumerate(lines) if line == "" ]

    elfs = []
    for i in range(len(separators_indices) - 1):
        elf_start = separators_indices[i] + 1
        elf_end = separators_indices[i + 1]
        elfs.append(np.array(lines[elf_start:elf_end]).astype(int))

    sums = np.array([np.sum(x) for x in elfs])
    
    if(PART == 1):
        print(f"The answer is: {np.max(sums)}")
    elif(PART == 2):
        print(f"The answer is: {np.sum(sorted(sums, reverse=True)[:3])}")
