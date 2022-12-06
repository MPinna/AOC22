INPUT_FILE = "input"
PART = 2

START_OF_PKT_LEN = 4
START_OF_MSG_LEN = 14

def find_marker(datastream: str, marker_len: int):
    datastream_len = len(datastream)
    window = set()
    for i in range(datastream_len - marker_len + 1):
        window.clear()
        window = set(datastream[i:i + marker_len])
        if(len(window) ==  marker_len):
            return i + marker_len

if __name__ == "__main__":
    with open(INPUT_FILE)  as input_f:
        datastream = input_f.read().strip()

    chars_processed = find_marker(datastream, START_OF_PKT_LEN if PART == 1 else START_OF_MSG_LEN)

    print(f"The answer is: {chars_processed}")