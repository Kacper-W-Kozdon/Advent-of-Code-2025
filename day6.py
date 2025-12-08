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
    def solve_puzzles(self, cephalopod: bool = False) -> int:

        solution: int = 0
        # print(f"{self.puzzles=}")
        for puzzle in self.puzzles:
            if cephalopod:
                puzzle = self.update(puzzle)
                # print(f"{puzzle=}")

            solution += int(eval(puzzle))

        return solution

    def update(self, puzzle: str) -> str:
        updated_puzzle: str = ""
        
        symbol: str = "*" if "*" in puzzle else "+"

        numbers: list[str] = puzzle.split(symbol)

        num_digits = len(max(numbers, key=len))

        for digit in range(num_digits):
            updated_puzzle += "".join([number[digit] for number in numbers]) + symbol

        return updated_puzzle[:-1]

    @classmethod
    def preprocess(cls, input_data: list[str]) -> list[str]:

        collapsed_puzzle_inputs: list[str] = []
        number_digits = len(input_data[0])
        symbols: list[str] = input_data[-1].split()
        symbol_index = 0
        last_space = 0

        for digit_index in range(number_digits):

            if not all([row[digit_index].isspace() for row in input_data[:-1]]):
                continue
            
            symbol = symbols[symbol_index]
            collapsed_puzzle_inputs.append("".join([row[last_space: digit_index] + symbol for row in input_data[:-1]])[:-1])

            last_space = digit_index + 1 
            symbol_index += 1
        
        symbol = symbols[symbol_index]
        collapsed_puzzle_inputs.append("".join([row[last_space:] + symbol for row in input_data[:-1]])[:-1])
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

    test_solution = test_puzzles.solve_puzzles(cephalopod=True)

    if test_solution != 3263827:
        raise ValueError(f"Expected solution: 3263827. Got {test_solution=}.")
    
    solution = puzzles.solve_puzzles(cephalopod=True)

    print(f"The second problem's {solution=}.")


if __name__ == "__main__":
    main()