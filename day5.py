import pathlib
from typing import Generator, Callable
import copy
import time
from functools import wraps


def timing(fun) -> Callable:
    @wraps(fun)
    def outer(*args, **kwargs):
        start = time.perf_counter()
        ret = fun(*args, **kwargs)
        end = time.perf_counter()
        duration = end - start
        if duration >= 0.05:
            print(f"---The execution of {fun.__name__=} {duration=}.---")
        return ret

    return outer


@timing
def load_files(file_name):
    file_path = f"{pathlib.Path(__file__).parent}\\{file_name}"
    fContent = []
    with open(file_path) as f:
        for (lineIndex, line) in enumerate(f):  # loading the file into an np.array
            if bool(line):
                # print(line.strip("\n").split("|"))
                fContent.append(line.strip("\n"))  # splitting each entry into coordinates

    return fContent


@timing
def check_ingredient(ranges: list[range], ingredient: str) -> bool:

    ingredient_id = int(ingredient)

    return any([ingredient_id in id_range for id_range in ranges])


def find_fresh_ranges(ranges) -> int:
    solution = 0
    fresh_ids: list[tuple[int, str]] = []
    new_ranges: list[range] = []
    start = 0
    stop = 0

    for id_range in ranges:
        fresh_ids.extend([(id_range.start, "start"), (id_range.stop, "stop")])

    fresh_ids.sort(key=lambda id_: id_[0])
    print(f"{fresh_ids=}")

    for index, id in enumerate(fresh_ids):

        if index == 0:
            start = id[0]
            update_start: bool = False
            update_stop: bool = True
            continue
        
        print(f"{id, update_start, update_stop=}")
        start, update_stop = (id[0], not update_start) if (id[1] == "start" and not update_stop) else (start, update_stop)
        stop, update_stop = (id[0], update_stop) if (id[1] == "stop") else (stop, update_start)
            
        print(f"{start, stop=}")

        if not update_stop:
            new_ranges.append(range(start, stop))

    ranges_set = set(new_ranges)
    print(f"{ranges_set=}")

    solution = sum([len(range) for range in new_ranges])
    return solution


def check_inventory(ranges: list[range], ingredients: list[str]) -> int:
    
    solution = 0

    for ingredient in ingredients:
        fresh = check_ingredient(ranges, ingredient)
        solution += int(fresh)

    return solution


class Inventory:
    def __init__(self, input_data: list[str]):
        self.ranges, self.ingredients = Inventory.prep(input_data)

    def check_inventory(self):
        return check_inventory(self.ranges, self.ingredients)
    
    def count_fresh_ids(self):
        return find_fresh_ranges(self.ranges)
    
    @classmethod
    def prep(cls, input_data) -> tuple[list[range], list[str]]:
        ranges: list[range] = []
        ingredients: list[str] = []

        split_index = input_data.index("")
        range_strings = input_data[:split_index]
        ingredients = input_data[split_index + 1:]
        ranges = list(map(lambda range_string: range(int(range_string[0]), int(range_string[1]) + 1), [range_string.split("-") for range_string in range_strings]))

        return ranges, ingredients


def main():
    test_data = load_files("test5.txt")
    input_data = load_files("data5.txt")

    test_inventory = Inventory(test_data)
    inventory = Inventory(input_data)

    test_solution = test_inventory.check_inventory()

    if test_solution != 3:
        raise ValueError(f"Expected solution: 3. Got {test_solution=}.")

    solution = inventory.check_inventory()

    print(f"The first {solution=}.")

    test_solution = test_inventory.count_fresh_ids()

    if test_solution != 14:
        raise ValueError(f"Expected solution: 14. Got {test_solution}.")
    
    solution = inventory.count_fresh_ids()

    print(f"The second {solution=}.")


if __name__ == "__main__":
    main()