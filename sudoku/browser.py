import csv
import urllib.request
import urllib.parse
import pprint
import time
from typing import Any
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import os
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()


SudokuConfig = list[list[int]]


def get_screen_dimensions():
    import tkinter as tk
    root = tk.Tk()
    dimensions = {'width': root.winfo_screenwidth(), 'height': root.winfo_screenheight()}
    root.quit()
    return dimensions


class Browser:
    difficulties = {1: "Easy", 2: "Medium", 3: 'Hard', 4: 'Evil'}
    _starting_url: str = "https://websudoku.com/"
    _half_screen_width = get_screen_dimensions()['width'] // 2
    _selenium_timeout_limit = 3

    def __init__(self):
        self.difficulty = None
        self.base_url = self._find_base_url()
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = webdriver.Chrome()
        self.driver.set_window_position(Browser._half_screen_width,0)
        self.driver.set_window_size(Browser._half_screen_width, Browser._half_screen_width)

    """
        CONVERT METHOD TO PROPERTY?
        https://www.programiz.com/python-programming/property 
    """

    def _find_base_url(self):
        url_data = urllib.request.urlopen(Browser._starting_url)
        html = BeautifulSoup(url_data, "html.parser")
        frameset = html.find("frameset")
        for frame in frameset:
            try:
                base_url = frame["src"]
                return base_url
            except TypeError:
                continue

    def set_difficulty(self, test: bool = True):
        if not test:

            print("Select Difficulty.\n",
                  "1: Easy\n",
                  "2: Medium\n",
                  "3: Hard\n",
                  "4: Evil")
            while True:
                try:
                    diff = input(" Enter number corresponding to desired difficulty: ")
                    if diff not in ("1", "2", "3", "4"):
                        raise ValueError
                    else:
                        break
                except ValueError:
                    print("Invalid difficulty selected. Enter a number between 1 and 4.")
                    continue

            self.difficulty = int(diff)
        else:
            self.difficulty = 4

    def get_difficulty(self) -> str:
        if self.difficulty is not None:
            return Browser.difficulties[self.difficulty]

    def _make_url(self) -> str:
        self.set_difficulty()
        suffix = {
            1: "",
            2: "level=2",
            3: "level=3",
            4: "level=4"
        }
        return self.base_url + suffix[self.difficulty]

    def open_url(self):

        self.driver.set_page_load_timeout(Browser._selenium_timeout_limit)
        try:
            self.driver.get(self._make_url())
        except TimeoutException:
            self.driver.execute_script("window.stop();")

    def _get_sudoku_html(self):
        try:
            self.open_url()
            print(.5)
            html = BeautifulSoup(self.driver.page_source, "html.parser")
            html = html.find("table", {"id": "puzzle_grid"})
            table = html.find('tbody')
            print(1)
            return table
        except RuntimeError as re:
            print("HTML Not Returned correctly", re.args())

    def make_board(self) -> SudokuConfig:
        print(2)
        board = []
        html = self._get_sudoku_html()
        print(3)
        for i, row in enumerate(html.find_all("tr")):
            intermediate_list = []
            for j, col in enumerate(row.find_all("td")):
                try:
                    value = int(col.contents[0].attrs['value'])
                    intermediate_list.append(value)
                    print(value, end=" | ")
                except:
                    value = None
                    intermediate_list.append(value)
                    print(" ", end=" | ")
            board.append(intermediate_list)
            print("\n")
        # print(board)
        return board


def main():
    browser = Browser()
    board = browser.make_board()


if __name__ == "__main__":
    main()