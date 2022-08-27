import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import os
import datetime

chromedriver_autoinstaller.install()

SudokuConfig = list[list[int]]


def get_screen_dimensions():
    import tkinter as tk
    root = tk.Tk()
    dimensions = {'width': root.winfo_screenwidth(), 'height': root.winfo_screenheight()}
    root.quit()
    return dimensions


class Browser:
    difficulties = {1: "Super easy",
                    2: "Very easy",
                    3: "Easy",
                    4: "Medium",
                    5: "Hard",
                    6: "Harder",
                    7: "Very hard",
                    8: "Super hard",
                    9: "Impossible"}

    _starting_url: str = "https://menneske.no/sudoku/eng/random.html"
    _half_screen_width = get_screen_dimensions()['width'] // 2
    _selenium_timeout_limit = 10

    def __init__(self):
        self.difficulty = None
        self.base_url = Browser._starting_url
        self.driver = webdriver.Chrome()
        self.driver.set_window_position(Browser._half_screen_width, 0)
        self.driver.set_window_size(Browser._half_screen_width, Browser._half_screen_width)
        self.saved_site_screenshot = False

    """
        CONVERT METHOD TO PROPERTY?
        https://www.programiz.com/python-programming/property 
    """

    def set_difficulty(self, test: bool = True):
        if not test:

            print("Select Difficulty.\n"
                  "1: Super easy\n"
                  "2: Very easy\n"
                  "3: Easy\n"
                  "4: Medium\n"
                  "5: Hard\n"
                  "6: Harder\n"
                  "7: Very hard\n"
                  "8: Super hard\n"
                  "9: Impossible")
            while True:
                try:
                    diff = input(" Enter number corresponding to desired difficulty: ")
                    if diff not in ("1", "2", "3", "4"):
                        raise ValueError
                    else:
                        break
                except ValueError:
                    print("Invalid difficulty selected. Enter a number between 1 and 9.")
                    continue

            self.difficulty = int(diff)
        else:
            self.difficulty = 9

    def get_difficulty(self) -> str:
        if self.difficulty is not None:
            return Browser.difficulties[self.difficulty]

    def _make_url(self) -> str:
        self.set_difficulty()
        return f"{self.base_url}?diff={self.difficulty}"

    def open_url(self):
        tries = 0
        while tries < 3:
            tries += 1
            timeout = Browser._selenium_timeout_limit * tries
            self.driver.set_page_load_timeout(timeout)
            try:
                self.driver.get(self._make_url())
                # get screenshot here
                try:
                    self.saved_site_screenshot = self.save_screenshot()
                    print(self.saved_site_screenshot)
                except OSError as ose:
                    print(ose, "Can't Save Screenshot of Sudoku Site")
                break
            except TimeoutException:
                self.driver.execute_script("window.stop();")
                continue

    def _get_sudoku_html(self):
        try:
            self.open_url()
            html = BeautifulSoup(self.driver.page_source, "html.parser")
            table = html.find("table", {"id": "main"}).find("div", {"id": "bodycol"}).find("tbody")
            return table
        except RuntimeError as re:
            print("HTML Not Returned correctly", re.args())

    def save_screenshot(self) -> bool:
        date_time_string = datetime.datetime.now().strftime("%Y/%m/%d_%H:%M:%S")
        game_difficulty = Browser.difficulties[self.difficulty]
        try:
            if not os.path.exists("files/site/"):
                print(1)
                os.makedirs("files/site/", mode=0o777)
                file_name = f"/files/site/{date_time_string}_sudoku_game_difficulty_{game_difficulty}.png"
                self.driver.save_screenshot(file_name)
                print(1.5)

            else:
                print(2)
                file_name = f"/files/site/{date_time_string}_sudoku_game_difficulty_{game_difficulty}.png"
                self.driver.save_screenshot(file_name)
                print(2.5)
            return True
        except OSError as ose:
            print(ose, "Can't Save Screenshot of Sudoku Site")
            return False

    def make_board(self) -> SudokuConfig:
        board = []
        html = self._get_sudoku_html()
        for i, row in enumerate(html.find_all("tr")):
            intermediate_list = []
            for j, col in enumerate(row.find_all("td")):
                try:
                    value = int(col.contents[0])
                    intermediate_list.append(value)
                    # print(value, end=" | ")
                except:
                    value = None
                    intermediate_list.append(value)
                    # print(" ", end=" | ")
            board.append(intermediate_list)
            # print("\n")
        # print(board)
        return board


def main():
    browser = Browser()
    browser.open_url()


if __name__ == "__main__":
    main()
