import pathlib

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


def find_sequences(input: list[str]) -> list[int]:

    sequences: list[int] = []

    bottom_limit_digits = len(input[0])
    top_limit_digits = len(input[1])

    bottom_limit = input[0]
    top_limit = input[1]

    test_number = bottom_limit

    first_half_digits: str = ""

    while int(test_number) <= int(top_limit):
        if (num_digits := len(test_number)) % 2:
            test_number = raise_magnitude(test_number)
            num_digits += 1
        
        # print(f"{test_number=}")
        first_half_digits = test_number[:int(num_digits / 2)]
        # print(f"{first_half_digits=}")

        combined = int(2 * first_half_digits)

        if int(bottom_limit) <= combined <= int(top_limit):
            sequences.append(combined)

        test_number = 2 * str(int(first_half_digits) + 1)

    return sequences


def find_sum_sequences(input: list[list[str]]) -> int:
    solution = 0

    for item in input:
        list_sequences: list[int] = find_sequences(item)
        solution += sum(list_sequences)

    return solution


def main():
    test_input = load_files("test2.txt")
    
    solution = find_sum_sequences(test_input)

    print(solution)

if __name__ == "__main__":
    main()