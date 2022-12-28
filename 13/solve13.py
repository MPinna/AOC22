from numpy import sign
from functools import cmp_to_key

INPUT_FILENAME ="input"
TEST1_FILENAME ="test1.txt"
TEST2_FILENAME ="test2.txt"

PART = 1

DEBUG = False

DIVIDER_PACKETS = [[[2]], [[6]]]

def debug_print(s: str):
    if(DEBUG):
        print(s)

def parse_pair(pair: str):
    left, right = pair.splitlines()
    return eval(left), eval(right)

def compare(left, right):
    type_left = type(left)
    type_right = type(right)

    if type_left == int and type_right == int:
        if left < right:
            return 1
        elif left == right:
            return 0
        else:
            return -1

    if type_left == list and type_right == list:
        len_left = len(left)
        len_right = len(right)

        if len_left > len_right:
            if len_right == 0:
                ret = -1
            ret = compare(left[:len_right], right)
            if ret == 0:
                ret = -1
            return ret
        elif len_left == len_right:
            ret = [compare(l,r) for l, r in zip(left, right)]
            if -1 in ret and 1 in ret:
                first_ordered_index = ret.index(1)
                first_unordered_index = ret.index(-1)
                return sign(first_unordered_index - first_ordered_index)
            else:
                return sign(sum(ret))
                
        else:
            if len_left == 0:
                return 1
            ret = compare(left, right[:len_left])
            if ret == 0:
                ret = 1
            return ret

    else:
        if type_left == int:
            return compare([left], right)
        else:
            return compare(left, [right])


if __name__ == "__main__":
    with open(INPUT_FILENAME) as input_f:
        pairs = input_f.read().split("\n\n")

    sum_of_indices = 0
    full_list = DIVIDER_PACKETS
    for index, pair in enumerate(pairs):
        left, right = parse_pair(pair)
        full_list.append(left)
        full_list.append(right)
        if compare(left, right) == 1:
            sum_of_indices += (index + 1)

    print(f"Sum of indices is {sum_of_indices}")
    full_list.sort(key=cmp_to_key(compare), reverse=True)
    
    decoder_key = (full_list.index([[2]]) + 1) * (full_list.index([[6]]) + 1)
    print(f"Decoder key is {decoder_key}")