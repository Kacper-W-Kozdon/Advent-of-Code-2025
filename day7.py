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


def project_beams(input_data: list[str], reverse: bool = False) -> int:
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
        line = "".join(scan_line)
        

        splitter_idx = 0
        # print(f"{line=}")
        if index == 0:
            continue

        for _ in range(line.count(splitter)):
            # print(f"{splitter_idx=}")
            splitter_idx = line[splitter_idx:].find(splitter)
            if (input_data[index - 1][splitter_idx] == splitter) and (input_data[index][splitter_idx] != splitter):
                
                line = line[:splitter_idx] + line[splitter_idx:].replace(splitter, empty, 1)
                splitter_idx += 1
                # pass
            else:
                # line = line[:splitter_idx] + line[splitter_idx:].replace(splitter, empty, 1)
                splitter_idx += 1
                # print(f"{line=}")

            pass
        # print(f"{line=}")

        input_data[index] = line
    # for line in input_data:
    #     print(line)
    if not reverse:
        return solution
    
    solution = 0

    reverse_scan_line: list[int] = [1 for _ in range(len(input_data[0]))]
    
    input_data = input_data[::-1]

    for line in input_data:
        # print(f"{reverse_scan_line=}")
        for pixel_index, pixel in enumerate(line):
            if pixel == start:
                pixel = beam
            left_pixel = max(0, pixel_index - 1)
            right_pixel = min(len(line), pixel_index + 1)

            if pixel == splitter:
                reverse_scan_line[pixel_index] = line[left_pixel].count(beam) * reverse_scan_line[left_pixel] + line[right_pixel].count(beam) * reverse_scan_line[right_pixel]

            else:
                reverse_scan_line[pixel_index] = pixel.count(beam) * reverse_scan_line[pixel_index]

    solution = sum(reverse_scan_line)
    return solution


def main():
    test_data = load_files("test7.txt")
    input_data = load_files("data7.txt")

    test_solution = project_beams(test_data)
    
    if test_solution != 21:
        raise ValueError(f"Expected solution: 21. Got {test_solution=}")

    solution = project_beams(input_data)

    print(f"The first problem's {solution=}.")

    test_solution = project_beams(test_data, reverse=True)
    
    if test_solution != 40:
        raise ValueError(f"Expected solution: 40. Got {test_solution=}")

    solution = project_beams(input_data, reverse=True)

    print(f"The second problem's {solution=}.")

if __name__ == "__main__":
    main()