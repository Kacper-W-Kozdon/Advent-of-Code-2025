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


def project_beams(input_data: list[str]) -> int:
    splitter = "^"
    beam = "|"
    empty = "."
    start = "S"

    scan_line: list[str] = []

    solution = 0
    line_len = 0

    for index, line in enumerate(input_data):
        if index == 0:
            scan_line = list(line.replace(start, beam))
            line_len = len(scan_line)
            continue

        for pixel_index in range(line_len):
            
            if (scan_line[pixel_index] == beam) and (line[pixel_index]) == splitter:
                solution += 1

                new_beam_left = max(0, pixel_index - 1)
                new_beam_right = min(pixel_index + 1, line_len)

                scan_line[new_beam_left: new_beam_right + 1] = [beam, splitter, beam][new_beam_left - (pixel_index - 1): 3 - ((pixel_index + 1) - new_beam_right)]
    return solution


def main():
    test_data = load_files("test7.txt")
    input_data = load_files("data7.txt")

    test_solution = project_beams(test_data)
    
    if test_solution != 21:
        raise ValueError(f"Expected solution: 21. Got {test_solution=}")

    solution = project_beams(input_data)

    print(f"The first problem's {solution=}.")


if __name__ == "__main__":
    main()