import pathlib

def load_files(file_name):
    file_path = f"{pathlib.Path(__file__).parent}\\{file_name}"
    fContent = []
    with open(file_path) as f:
        for (lineIndex, line) in enumerate(f):  # loading the file into an np.array
            if bool(line):
                # print(line.strip("\n").split("|"))
                fContent.append(line.strip("\n"))  # splitting each entry into coordinates
    return fContent


def password_finder(input: list[str], mod: int = 99, protocol: int = 0):
    if not isinstance(input, list):
        raise TypeError(f"Expected list, got {type(input)=}.")
    if input == []:
        raise ValueError("Input list is empty.")
    if any([not isinstance(entry, str) for entry in input]):
        raise TypeError(f"Entries in the input list contain incorrect types. Expected str, got: {set([type(entry) for entry in input])=}")
    dial = [num for num in range(0, mod + 1)]
    solution = 0

    starting_position = 50
    next_number = starting_position

    for instruction in input:
        instruction_numeric = int(instruction.replace("R", "+").replace("L", "-"))
        if protocol:
            solution += abs((next_number + instruction_numeric) // (mod + 1))
        next_number = dial[(next_number + instruction_numeric) % (mod + 1)]

        if next_number == 0 and not protocol:
            solution += 1

    print(solution)
    return solution


def main():
    input_test = load_files("test1.txt")

    if (answer := password_finder(input_test)) != 3:
        raise ValueError(f"Expected the answer to be 3. Got {answer=}")
    
    input = load_files("data1.txt")
    answer = password_finder(input)

    print(f"Solution 1 {answer=}.")

    if (answer := password_finder(input_test, protocol=1)) != 6:
        raise ValueError(f"Expected the answer to be 6. Got {answer=}")
    
    answer = password_finder(input, protocol=1)

    print(f"Solution 2 {answer=}.")



if __name__ == "__main__":
    main()