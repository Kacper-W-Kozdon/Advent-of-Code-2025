import pathlib
from typing import Generator
import copy


def load_files(file_name):
    file_path = f"{pathlib.Path(__file__).parent}\\{file_name}"
    fContent = []
    with open(file_path) as f:
        for (lineIndex, line) in enumerate(f):  # loading the file into an np.array
            if bool(line):
                # print(line.strip("\n").split("|"))
                fContent.append(line.strip("\n"))  # splitting each entry into coordinates

    return fContent


def process_row(rows: list[list[str]], max_rolls: int) -> int:
    # print(f"{rows=}")

    ret: int = 0
    num_columns: int = len(rows[0])

    collapsed: str = ""

    collapsed_list: list[str] = ["" for _ in range(num_columns)]

    for row_index, row in enumerate(rows):
        collapsed_list = [collapsed_list[column] + row[column] for column in range(num_columns)]

    collapsed = collapsed_list[0] + collapsed_list[1]

    if (collapsed[1:].count("@") < max_rolls) and (collapsed[0] == "@"):
        ret += 1

    collapsed = collapsed_list[-1] + collapsed_list[-2]

    if (collapsed[1:].count("@") < max_rolls) and (collapsed[0] == "@"):
        ret += 1
    
    for column in range(1, num_columns - 1):
        collapsed = collapsed_list[column] + collapsed_list[column - 1] + collapsed_list[column + 1]
        middle_roll_index = int(len(collapsed_list[column]) / 2) + 1
        if (collapsed[1:].count("@") < max_rolls) and (collapsed[0] == "@"):
            ret += 1

    return ret


def direct_forklift(input_data: list[str], max_rolls: int | None = None) -> int:
    if max_rolls is None:
        max_rolls = 4

    solution = 0

    adjacent_rows: list[list[str]] = []
    
    for row_index, row in enumerate(input_data):
        if row_index == 0:
            adjacent_rows = [list(row), list(input_data[row_index + 1])]
        elif row_index == len(input_data) - 1:
            adjacent_rows = [list(row), list(input_data[row_index - 1])]
        else:
            adjacent_rows = [list(row), list(input_data[row_index - 1]), list(input_data[row_index + 1])]

        solution += process_row(adjacent_rows, max_rolls)

    return solution


def main():
    test_data = load_files("test4.txt")
    input_data = load_files("data4.txt")
    
    test_solution = direct_forklift(test_data)

    if test_solution != 13:
        raise ValueError(f"Expected solution: 13. Got {test_solution=}.")
    
    solution = direct_forklift(input_data)

    print(f"The first problem's {solution=}.")


if __name__ == "__main__":
    main()