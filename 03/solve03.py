
from string import ascii_uppercase, ascii_lowercase
INPUT_FILE = "input"
PART = 2

def get_item_priority(item: chr):
    if item in ascii_lowercase:
        return ord(item) - ord('a') + 1
    if item in ascii_uppercase:
        return ord(item) - ord('A') + 27

if __name__ == "__main__":
    with open(INPUT_FILE)  as input_f:
        rucksacks = input_f.read().splitlines()

    sum = 0

    if(PART == 1):
        for rucksack in rucksacks:
            comp_1 = set(rucksack[:(len(rucksack)//2)])
            comp_2 = set(rucksack[(len(rucksack)//2):])
            common = [x for x in comp_1.intersection(comp_2)][0]

            sum += get_item_priority(str(common))
    elif(PART == 2):
        for i in range(0, len(rucksacks), 3):
            rucksack_1 = set(rucksacks[i])
            rucksack_2 = set(rucksacks[i + 1])
            rucksack_3 = set(rucksacks[i + 2])
            badge = rucksack_1.intersection(rucksack_2)
            badge = [x for x in badge.intersection(rucksack_3)][0]
            sum += get_item_priority(str(badge))

    print(f"The total sum is: {sum}")