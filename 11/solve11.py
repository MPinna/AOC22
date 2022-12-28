INPUT_FILENAME ="input"
TEST1_FILENAME ="test1.txt"
TEST2_FILENAME ="test2.txt"

PART = 1
ROUNDS = 20
RELIEF_FACTOR = 1

DEBUG = False

def debug_print(s: str):
    if(DEBUG):
        print(s)

def parse_monkey_logic(monkey_logic: str):
    lines = monkey_logic.splitlines()
    items = list(map(int, lines[1].split(":")[1].split(",")))
    operation = lines[2].split("=")[1].strip()
    test_divisor = int(lines[3].split(" ")[-1])
    destination_true = int(lines[4].split(" ")[-1])
    destination_false = int(lines[5].split(" ")[-1])

    return items, operation, test_divisor, destination_true, destination_false


class KeepAway():


    monkeys = []

    def __init__(self):
        self.monkeys = []
        self.modulo = 1

    def add_monkeys(self, monkey_logics: list):
        for monkey_logic in monkey_logics:
            monkey = {}
            items, operation, test_divisor, destination_true, destination_false = parse_monkey_logic(monkey_logic)
            monkey["items"] = items
            monkey["operation"] = operation
            monkey["test_divisor"] = test_divisor
            monkey["destination_true"] = destination_true
            monkey["destination_false"] = destination_false
            monkey["items_counted"] = 0

            self.monkeys.append(monkey)

        assert all([m["destination_true"] < len(self.monkeys) and m["destination_false"] < len(self.monkeys) for m in self.monkeys])
        print(f"All monkeys added correctly")

        for monkey in self.monkeys:
            self.modulo *= monkey["test_divisor"]



    def execute_round(self, round):
        for index, monkey in enumerate(self.monkeys):
            items: list = monkey["items"]
            formal_operation: str= monkey["operation"]
            test_divisor = monkey["test_divisor"]
            destination_true = monkey["destination_true"]
            destination_false = monkey["destination_false"]

            for item in items:
                actual_operation = formal_operation.replace("old", str(item))
                new = eval(actual_operation) % self.modulo
                new = new // RELIEF_FACTOR
                if new % test_divisor == 0:
                    self.monkeys[destination_true]["items"].append(new)
                else:
                    self.monkeys[destination_false]["items"].append(new)
                self.monkeys[index]["items"] = []
                self.monkeys[index]["items_counted"] += 1

    def print_item_counted(self):
        for index, monkey in enumerate(self.monkeys):
            print(f"Monkey {index} inspected items {monkey['items_counted']} times.")

    def get_monkey_business(self):
        counts = [m["items_counted"] for m in self.monkeys]
        counts.sort(reverse=True)
        return counts[0]*counts[1]
        


if __name__ == "__main__":
    with open(INPUT_FILENAME) as input_f:
        monkey_logics = input_f.read().split("\n\n")

    ka = KeepAway()
    ka.add_monkeys(monkey_logics)
    print()
    for i in range(10000):
        ka.execute_round(i)
    
    monkey_business_level = ka.get_monkey_business()
    print(f"The level of monkey business is {monkey_business_level}")

    