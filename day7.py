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


def update_slice_scan(slice_scan: list[str], slice_line: str, next_slice_line: str, symbols: list[str]) -> None:
    splitter, beam, empty, start = tuple(symbols)

    line_len = len(slice_scan)

    for pixel_index in range(line_len):
            
        if (slice_scan[pixel_index] == beam) and (slice_line[pixel_index]) == beam:

            new_beam_left = max(0, pixel_index - 1)
            new_beam_right = min(pixel_index + 1, line_len)

            slice_scan[new_beam_left: new_beam_right + 1] = next_slice_line[new_beam_left: new_beam_right + 1]

        if (slice_scan[pixel_index] == beam) and (slice_line[pixel_index]) == splitter:
            slice_scan[pixel_index] = next_slice_line[pixel_index]
            pass

    raise NotImplementedError


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

    if not reverse:
        return solution
    
    returning_beam_indices: list[int] = []
    num_returning_beams: int = 0

    num_returning_beams = scan_line.count("|")

    solution_list: list[int] = [1 for _ in range(num_returning_beams)]
    

    last_beam_index: int = 0
    for _ in range(num_returning_beams):
        returning_beam_indices.append(scan_line[last_beam_index:].index("|"))
        last_beam_index += 1
    
    beam_slices: list[slice] = [slice(index, index + 1) for index in returning_beam_indices]

    input_data = input_data[::-1]

    for counter, pixel_index in enumerate(returning_beam_indices):
        scan_line_reverse: list[str] = ["|" if idx == pixel_index else "." for idx in range(len(input_data[0]))]
        
        break_condition = len(returning_beam_indices) - 1

        for index, line in enumerate(input_data):
            beam_slices[counter] = slice(max(0, beam_slices[counter].start - 1), min(beam_slices[counter].stop + 1, line_len))
            slice_scan = scan_line_reverse[beam_slices[counter]]
            slice_line = line[beam_slices[counter]]
            next_slice_line = input_data[index + 1][beam_slices[counter]]

            update_slice_scan(slice_scan, slice_line, next_slice_line, [splitter, beam, empty, start])
            scan_line_reverse[beam_slices[counter]] = slice_scan

            if start in input_data[index + 1]:
                break

        if counter == break_condition:
            break

        solution += scan_line_reverse[input_data[-1].index("S")].count("|")
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