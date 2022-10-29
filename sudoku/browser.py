import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from utility_functions import get_screen_dimensions, make_save_path

chromedriver_autoinstaller.install()

SudokuConfig = list[list[int]]


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

    def set_difficulty(self, diff, test: bool = False):
        if not test:
            self.difficulty = int(diff)
        else:
            self.difficulty = 7

    def get_difficulty(self) -> str:
        if self.difficulty is not None:
            return Browser.difficulties[self.difficulty]

    def _make_url(self) -> str:
        # self.set_difficulty(diff)
        return f"{self.base_url}?diff={self.difficulty}"

    def open_url(self):
        tries = 0
        while tries < 3:
            tries += 1
            timeout = Browser._selenium_timeout_limit * tries
            self.driver.set_page_load_timeout(timeout)
            try:
                self.driver.get(self._make_url())
                try:
                    self.driver.execute_script("document.body.style.zoom='60%'")
                    self.saved_site_screenshot = self.get_screenshot()
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
            print("HTML Not Returned correctly: ", re)

    def make_board(self, difficulty: int) -> SudokuConfig:
        self.set_difficulty(difficulty)
        board = []
        html = self._get_sudoku_html()
        for i, row in enumerate(html.find_all("tr")):
            intermediate_list = []
            for j, col in enumerate(row.find_all("td")):
                try:
                    value = int(col.contents[0])
                    intermediate_list.append(value)
                except:
                    value = None
                    intermediate_list.append(value)
            board.append(intermediate_list)
        return board

    def get_screenshot(self) -> bool:
        game_difficulty = Browser.difficulties[self.difficulty]
        try:
            file_name = make_save_path(save_path="files/site/", game_difficulty=game_difficulty)
            if file_name != '':
                self.driver.save_screenshot(file_name)
                return True
        except OSError as ose:
            print(ose, "Can't Save Screenshot of Sudoku Site")
            return False


def main():
    pass


if __name__ == "__main__":
    main()
