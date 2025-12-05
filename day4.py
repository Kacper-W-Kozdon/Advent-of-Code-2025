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


def process_row(rows: list[list[str]], max_rolls: int) -> tuple[int, list[str]]:
    # print(f"{rows=}")

    ret: int = 0
    num_columns: int = len(rows[0])
    column_indices: list[int] = []

    collapsed: str = ""

    collapsed_list: list[str] = ["" for _ in range(num_columns)]

    for row_index, row in enumerate(rows):
        collapsed_list = [collapsed_list[column] + row[column] for column in range(num_columns)]

    collapsed = collapsed_list[0] + collapsed_list[1]

    if (collapsed[1:].count("@") < max_rolls) and (collapsed[0] == "@"):
        ret += 1
        column_indices.append(0)

    collapsed = collapsed_list[-1] + collapsed_list[-2]

    if (collapsed[1:].count("@") < max_rolls) and (collapsed[0] == "@"):
        ret += 1
        column_indices.append(num_columns - 1)
    
    for column in range(1, num_columns - 1):
        collapsed = collapsed_list[column] + collapsed_list[column - 1] + collapsed_list[column + 1]
        middle_roll_index = int(len(collapsed_list[column]) / 2) + 1
        if (collapsed[1:].count("@") < max_rolls) and (collapsed[0] == "@"):
            ret += 1
            column_indices.append(column)

    new_row = ["." if index in column_indices else rows[0][index] for index in range(num_columns)]

    return ret, new_row


def forklift_single_run(input_data: list[str], updated_input: list[str], max_rolls: int) -> int:
    solution = 0
    adjacent_rows: list[list[str]] = []
    for row_index, row in enumerate(input_data):
        if row_index == 0:
            adjacent_rows = [list(row), list(input_data[row_index + 1])]
        elif row_index == len(input_data) - 1:
            adjacent_rows = [list(row), list(input_data[row_index - 1])]
        else:
            adjacent_rows = [list(row), list(input_data[row_index - 1]), list(input_data[row_index + 1])]

        count, new_row = process_row(adjacent_rows, max_rolls)

        solution += count
        updated_input.append("".join(new_row))

    return solution


def direct_forklift(input_data: list[str], max_rolls: int | None = None, repeat: bool = False) -> int:
    if max_rolls is None:
        max_rolls = 4

    solution = 0

    updated_input: list[str] = []
    
    solution += forklift_single_run(input_data, updated_input, max_rolls)
    
    if not repeat:
        return solution
    
    while (updated_input != input_data) and (solution != (len(input_data) * len(input_data[0]))):
        input_data = copy.copy(updated_input)
        updated_input.clear()
        solution += forklift_single_run(input_data, updated_input, max_rolls)

    return solution


def main():
    test_data = load_files("test4.txt")
    input_data = load_files("data4.txt")
    
    test_solution = direct_forklift(test_data)

    if test_solution != 13:
        raise ValueError(f"Expected solution: 13. Got {test_solution=}.")
    
    solution = direct_forklift(input_data)

    print(f"The first problem's {solution=}.")

    test_solution = direct_forklift(test_data, repeat=True)

    if test_solution != 43:
        raise ValueError(f"Expected solution: 43. Got {test_solution=}.")
    
    solution = direct_forklift(input_data, repeat=True)

    print(f"The second problem's {solution=}.")


if __name__ == "__main__":
    main()