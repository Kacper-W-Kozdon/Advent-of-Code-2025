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


def get_joltage(input_: str, digits: int) -> int:
    ret = ""

    
    chosen_digits: list[str] = []

    input_digits = list(input_)
    chosen_digits = input_digits[-digits:]
    input_digits = input_digits[:-digits]

    for digit_index in range(digits):
        trial_max = max(input_digits)
        # print(f"{trial_max, chosen_digits=}")
        if trial_max < chosen_digits[digit_index]:
            break
        input_digits.append(chosen_digits.pop(digit_index))
        chosen_digits.insert(digit_index, trial_max)
        max_index = input_digits.index(trial_max)
        if (max_index == len(input_digits) - 1) or (input_digits == []):
            break
        input_digits = input_digits[max_index + 1:]

    ret = "".join(chosen_digits)

    # print(f"{ret, chosen_digits=}")

    return int(ret)


def get_total_joltage(input_: list[str], digits: int | None = None) -> int:

    if digits is None:
        digits = 2

    solution = 0

    for battery in input_:
        # print(f"{battery=}")
        solution += get_joltage(battery, digits)

    return solution


def main():
    test_data = load_files("test3.txt")
    input_data = load_files("data3.txt")

    test_solution = get_total_joltage(test_data)

    if test_solution != 357:
        raise ValueError(f"Expected value: 357. Got {test_solution=}.")
    
    solution = get_total_joltage(input_data)

    print(f"The first problem's {solution=}.")

    test_solution = get_total_joltage(test_data, digits=12)
    
    if test_solution != 3121910778619:
        raise ValueError(f"Expected value: 3121910778619. Got {test_solution=}.")
    
    solution = get_total_joltage(input_data, digits=12)

    print(f"The second problem's {solution=}.")

if __name__ == "__main__":
    main()