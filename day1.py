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


def password_finder(input, mod: int = 99):
    dial = [num for num in range(0, mod - 1)]
    solution = 0

    starting_position = 50
    next_number = starting_position

    for instruction in input:
        instruction_numeric = int(instruction.replace("R", "+").replace("L", "-"))
        next_number = dial[next_number + instruction_numeric]
        if next_number == 0:
            solution += 1

    print(solution)


def main():
    input = 