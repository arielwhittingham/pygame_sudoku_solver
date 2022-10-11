from collections import OrderedDict
from typing import Union
import copy
import numpy as np
from utility_functions import get_section

DictConfig = dict[tuple[int, int]:dict[str:int, str:int]]
CellConfig = dict[str:int, str:int]


class SudokuBoard:
    """
    This class represents the sudoku board data and logical operations that can be performed on the board and
    its squares, such as updating squares, resetting squares, returning possible values for a square, returning
    null squares and so on.
    """
    _complete_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    # Full set of possible Sudoku numbers for any rank, file, or
    # section (1 of 9 possible 3x3 sections of the board).

    def __init__(self, original_config: list[list[int]]):

        dict_config: DictConfig

        self.dict_config = self._get_dict_config(original_config)
        self.list_config = self._get_list_config()  # defined later based on dict_config unpacking

    def _get_dict_config(self, list_config) -> DictConfig:

        """
        Translates list[list[int]] configuration to a dictionary
        :param list_config:
        :return dict dict_config: key = tuple[row, col], value = dict[section:int, value:int]
        """

        dict_config: DictConfig = OrderedDict()
        cell_dict: dict[str:int, str:int]
        x: int
        y: int

        # create dictionary representation of the board
        for x in range(0, 9):
            for y in range(0, 9):
                cell_dict = {}
                row = 9 - x
                col = y + 1
                cell_dict["section"] = get_section(row, col)
                cell_dict["value"] = list_config[x][y]
                dict_config[row, col] = cell_dict
        return dict_config

    @property
    def config(self) -> DictConfig:
        return self.dict_config

    def _get_list_config(self) -> list[list[Union[int, None]]]:
        """
        Convert dict_config back to list
        """

        list_config = []

        for _ in range(9):
            intermediate = [None] * 9
            list_config.append(intermediate)
        # loop through dictionary keys and fill list of lists
        for key in self.config.keys():
            row_index = 9 - key[0]
            col_index = key[1] - 1
            value = self.config[key]["value"]
            list_config[row_index][col_index] = value
        return list_config

    def array_config(self) -> np.array:
        return np.array(self.list_config)

    def _return_taken_squares(self, axis: str, val: int) -> set[int]:
        """
        Return filled in square per axis
        :param axis: row, col, section
        :param val: 1-9 representing either rows 1-9, columns 1-9 or sections 1-9
        :return: set of numbers available for the val # axis.
        For example
        _return_taken_squares(row,1) will return all filled-in squares in row 1
        """

        taken: set[int] = set()
        config = self.config
        for key in config.keys():
            if axis == "row" and key[0] == val and config[key]["value"] is not None:
                taken.add(config[key]["value"])

            if axis == "col" and key[1] == val and config[key]["value"] is not None:
                taken.add(config[key]["value"])

            if axis == "section" and config[key]["section"] == val and config[key]["value"] is not None:
                taken.add(config[key]["value"])
        return taken

    def get_options(self, row: int, col: int) -> set[int]:
        """
        return all possible values from 1-9 for a particular cell
        :param row: row number
        :param col: column number
        :return: set of possible option
        """
        square: CellConfig
        square = self.config[row, col]
        starting_set = copy.copy(SudokuBoard._complete_set)
        row_values = self._return_taken_squares(axis="row", val=row)  # check row
        col_values = self._return_taken_squares(axis="col", val=col)  # check column
        section_values = self._return_taken_squares(axis="section", val=square["section"])  # check section
        return_set = starting_set.difference(row_values)
        return_set = return_set.difference(col_values)
        return_set = return_set.difference(section_values)
        return return_set

    def get_value(self, row, col) -> int:
        return self.config[row, col]["value"]

    def set_value(self, row, col, value) -> None:
        self.config[row, col]["value"] = value

    def remove_value(self, row, col) -> None:
        self.set_value(row, col, None)

    def _value_is_null(self, row, col) -> bool:
        return self.get_value(row, col) is None

    def update_value(self, row, col) -> Union[int, bool]:
        """
        Update empty cell if cell is empty
        and options for that are cell == 1
        """

        options = list(self.get_options(row, col))
        if len(options) != 1:
            return False
        elif len(options) == 1 and self._value_is_null(row, col):
            self.set_value(row, col, options[0])
            return options[0]
        else:
            return False

    def get_blank(self):

        keys = self.dict_config.keys()
        for ind in keys:
            row = ind[0]
            col = ind[1]
            if self._value_is_null(row, col):
                return ind
        return False


def main():
    pass


if __name__ == "__main__":
    main()
