import pathlib
from typing import Generator

def load_files(file_name):
    file_path = f"{pathlib.Path(__file__).parent}\\{file_name}"
    fContent = []
    with open(file_path) as f:
        for (lineIndex, line) in enumerate(f):  # loading the file into an np.array
            if bool(line):
                # print(line.strip("\n").split("|"))
                fContent.extend(line.strip("\n").split(","))  # splitting each entry into coordinates

    fContent = list(map(lambda x: str.split(x, "-"), fContent))

    return fContent


def raise_magnitude(number: str) -> str:
    num_digits = len(number)

    leading_digit = "1"

    ret = leading_digit + num_digits * "0"

    return ret


def generate_factors(bottom_limit: str, top_limit: str) -> Generator[int]:

    num_digits_bottom = len(bottom_limit)
    num_digits_top = len(top_limit)

    for divider in range(2, num_digits_top + 1):
        if not num_digits_bottom % divider or not num_digits_top % divider:
            yield divider


def generate_sequences_for_factor(test_number: str, bottom_limit: str, top_limit: str, factor: int, sequences: list[int]):
    while int(test_number) <= int(top_limit):
        
        if (num_digits := len(test_number)) % factor:
            test_number = raise_magnitude(test_number)
            num_digits += 1
        
        # print(f"{test_number=}")
        end_index = int(num_digits / factor) if num_digits / factor == int(num_digits / factor) else int(num_digits / factor) + 1
        first_frac_digits = test_number[:end_index]
        # print(f"{first_frac_digits=}")

        combined = int(factor * first_frac_digits)
        # print(f"{combined=}")

        if (int(bottom_limit) <= combined <= int(top_limit)) and combined not in sequences:
            sequences.append(combined)

        if len(str(int(first_frac_digits) + 1)) == len(first_frac_digits):
            test_number = factor * str(int(first_frac_digits) + 1)
        else:
            # print(f"{test_number, factor=}")
            test_number = raise_magnitude(test_number)
            # print(f"{test_number=}")
            num_digits += 1


def find_sequences(input: list[str], factor: int | None = None) -> list[int]:

    sequences: list[int] = []

    bottom_limit = input[0]
    top_limit = input[1]

    test_number = bottom_limit

    factors = [factor] if factor else generate_factors(bottom_limit, top_limit)

    for factor in factors:
        # print(f"{factor, len(test_number)=}")
        generate_sequences_for_factor(test_number, bottom_limit, top_limit, factor, sequences)

    return sequences


def find_sum_sequences(input: list[list[str]], factor: int | None = None) -> int:
    solution = 0
    all_sequences = set()

    for item in input:
        list_sequences: list[int] = find_sequences(item, factor)
        # print(f"{list_sequences=}")
        all_sequences.update(set(list_sequences))

    solution = sum(list(all_sequences))
    # print(f"{all_sequences=}")

    return solution


def main():
    test_input = load_files("test2.txt")
    data = load_files("data2.txt")
    
    test_solution = find_sum_sequences(test_input, factor=2)

    if test_solution != 1227775554:
        raise ValueError(f"Expected value: 1227775554. Got {test_solution=}.")

    solution = find_sum_sequences(data, factor=2)

    print(f"First {solution=}")

    test_solution = find_sum_sequences(test_input)

    if test_solution != 4174379265:
        raise ValueError(f"Expected value: 4174379265. Got {test_solution=}, {len("4174379265"), len(str(test_solution))=}.")
    
    solution = find_sum_sequences(data)

    print(f"Second {solution=}.")



if __name__ == "__main__":
    main()