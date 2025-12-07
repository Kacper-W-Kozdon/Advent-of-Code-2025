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


class Math_Problems():

    def __init__(self, input_data: list[str]):

        self.puzzles = self.preprocess(input_data)

    @timing
    def solve_puzzles(self) -> int:

        solution: int = 0

        for puzzle in self.puzzles:
            solution += int(eval(puzzle))

        return solution

    @classmethod
    def preprocess(cls, input_data: list[str]) -> list[str]:

        collapsed_puzzle_inputs: list[str] = []
        symbols: list[str] = input_data[-1].split()

        for index, puzzle_inputs in enumerate(input_data[:-1]):
            
            if index == 0:
                collapsed_puzzle_inputs = [number for number in puzzle_inputs.split()]
                continue

            collapsed_puzzle_inputs = [f"{collapsed_puzzle_inputs[number_idx]} {symbols[number_idx]} {number}" for number_idx, number in enumerate(puzzle_inputs.split())]

        return collapsed_puzzle_inputs


def main():
    test_data = load_files("test6.txt")
    input_data = load_files("data6.txt")

    test_puzzles = Math_Problems(test_data)

    test_solution = test_puzzles.solve_puzzles()

    if test_solution != 4277556:
        raise ValueError(f"Expected solution: 4277556. Got {test_solution=}.")
    
    puzzles = Math_Problems(input_data)

    solution = puzzles.solve_puzzles()

    print(f"The first problem's {solution=}.")


if __name__ == "__main__":
    main()