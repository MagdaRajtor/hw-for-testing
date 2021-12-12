import argparse
import json
import os
from typing import List, Union
import pytest
from pytest_mock import mocker

current_dir = os.path.dirname(__file__)

def take_from_list(li: list, indices: Union[int, List[int]]):
    """
    This function returns list of elements for given indices.

    :param li: list of elements
    :param indices: single index or list of indices
    :return: list of elements selected using indices
    """
    if isinstance(indices, int):
        indices = [indices]
    if not isinstance(indices, list) or not all(isinstance(i, int) for i in indices):
        raise ValueError(f"Indices should be integer or list of integers, not {type(indices)}")
    for index in indices:
        if index >= len(li):
            raise IndexError(f"Index {index} is to big for list of length {len(li)}")

    return [li[i] for i in indices]


def calculate(in_file: str, out_file: str):
    with open(in_file, 'r') as f_p:
        data = json.load(f_p)

    result = take_from_list(data["list"], data["indices"])

    with open(out_file, 'w') as f_p:
        json.dump(result, f_p)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", default=os.path.join(current_dir, "input.json"), nargs="?")
    parser.add_argument("output_file", default=os.path.join(current_dir, "output.json"), nargs="?")
    args = parser.parse_args()

    calculate(args.input_file, args.output_file)


def test_take_from_list():
    assert take_from_list([0, 1], 0) == [0]
    assert take_from_list([11, 12, 13, 14, 15], [1, 3, 5-1]) == [12, 14, 15]
    with pytest.raises(ValueError):
        take_from_list([3, 4, 0, 1, 2], [0, 1, 0.5, 3, "four"])
    with pytest.raises(IndexError):
        take_from_list([3, 4, 0], [0, 1, 2, 6])

def test_calculate(mocker):
    #create a json file with the result by hand
    test_file = open("test.json", "w")
    test_file.write(json.dumps([1, 9, 8, 7]))
    test_file.close()

    #get a json file with the same result from the function -> :(
    mocker.patch(__name__ + '.take_from_list', return_value = [1, 9, 8, 7])
    calculate(args.input_file, args.output_file)
    out_file = open("output.json", "r")

    #they should be identical
    assert test_file == out_file