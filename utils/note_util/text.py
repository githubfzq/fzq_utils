import argparse
from pathlib import Path
import re
from typing import List


def remove_pattern_lines(input_file: Path, output_dir: Path, regexes: List[re.Pattern]):
    # read in the input file
    with input_file.open() as fp:
        lines = fp.readlines()
    # filter out lines that match the regexes
    lines = [line for line in lines if not any(regex.search(line) for regex in regexes)]
    # write the filtered lines to the output file
    output_path = output_dir / (input_file.name)
    with open(output_path, "w") as fp:
        fp.writelines(lines)

def batch_remove_pattern_lines(input_file: Path, output_dir: Path, regexes: List[re.Pattern]):
    for file in input_file.glob("*.txt"):
        remove_pattern_lines(file, output_dir, regexes)
