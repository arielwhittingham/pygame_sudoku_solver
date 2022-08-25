import sys
import os

sys.path.append(os.path.abspath('.'))
import time
import pygame
import game
import browser
from pygame import font, color
from typing import Any, Union

pygame.init()
font.init()


class SudokuGui:
    GREEN = color.Color(52, 150, 50)
    RED = color.Color(252, 100, 50)
    BLACK = color.Color(0, 0, 0)
    YELLOW = (255, 255, 50)
    WHITE = color.Color(255, 255, 255)
    CLEAR = color.Color(255, 255, 255, 0)
    try_counter = 0

    color_mapper = {
        'w': WHITE,
        'g': GREEN,
        'r': RED,
        'b': BLACK,
        'y': YELLOW
    }

    def __init__(self, square=306):
        self.size = square
        self.window_height = self.size
        self.window_width = self.size
        self.block_size = self.size // 9
        self.font_size = self.size // 10
        self.screen = pygame.display.set_mode((self.window_height, self.window_width))
        self.game_board = None
        self.array_config = None
        self.dict_config = None
        self.difficulty = None
        self.main_run()

    def draw_grid(self):
        for x in range(9):
            for y in range(9):
                rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, SudokuGui.BLACK, rect, 1)

    def set_highlight(self, row: int, col: int, sq_color, width: int):
        rect = pygame.Rect((col - 1) * self.block_size, (9 - row) * self.block_size, self.block_size, self.block_size)
        pygame.draw.rect(self.screen, sq_color, rect, width)
        pygame.display.update()

    def index_to_screen_position(self, row: int, col: int):
        column_offset = self.size // 30
        row_offset = 0
        return_row = ((9 - row) * self.block_size) + row_offset
        return_column = ((col - 1) * self.block_size) + column_offset
        return return_column, return_row

    def get_color(self, row, col, border_offset=0) -> tuple[int]:
        c_col, c_row = self.index_to_screen_position(row, col)
        return self.screen.get_at((c_col + border_offset, c_row + border_offset))

    def color_sections(self):
        section_size = self.block_size * 3
        for row in range(3):
            for col in range(3):
                row_pos = section_size * row
                col_pos = section_size * col
                if (row + col) % 2:
                    self.screen.fill(SudokuGui.GREEN,
                                     rect=(row_pos, col_pos, self.window_width / 3, self.window_height / 3))
                else:
                    self.screen.fill(SudokuGui.RED,
                                     rect=(row_pos, col_pos, self.window_width / 3, self.window_height / 3))
            # self.layer_background = pygame.surface.Surface((800, 600))
            # self.layer_background.fill(COLORS[0])

    def insert_value(self, row: int, col: int, value: Union[int, None], color_input: str = None, custom_color: Any = False) -> None:

        """
        :param custom_color: add color during execution from self.get_color() method
        :param color_input: string that maps to a sudoku_color
        :param row: 1-9 sudoku board row
        :param col: 1-9 sudoku board column
        :param value: 1-9 sudoku value
        :return: None
        """
        pg_color: Any
        if custom_color is False:
            if color_input is None:
                color_input = 'w'
                pg_color = SudokuGui.color_mapper[color_input]
            else:
                pg_color = SudokuGui.color_mapper[color_input]
        else:
            pg_color = pygame.color.Color(custom_color)
        value = str(value)
        val_font = pygame.font.SysFont('Arial', self.font_size)
        val = val_font.render(value, True, pg_color)
        screen_position = self.index_to_screen_position(row, col)
        self.screen.blit(val, screen_position)

    def fetch_game(self):
        sudoku_site = browser.Browser()
        self.game_board = game.SudokuBoard(sudoku_site.make_board())
        self.difficulty = sudoku_site.get_difficulty()
        self.refresh_board()

    @property
    def board(self):
        return self.array_config

    def refresh_board(self):
        self.array_config = self.game_board.array_config()
        self.dict_config = self.game_board.dict_config

    def set_gui_data(self):
        for ind in self.dict_config:
            if self.dict_config[ind]['value'] is not None:
                self.insert_value(ind[0], ind[1], self.dict_config[ind]['value'], 'y')

    def backtrack(self):
        try:
            # pygame.display.update()
            self.refresh_board()
            next_blank = self.game_board.get_blank()
            if not next_blank:
                pygame.display.update()
                print("tries: ", SudokuGui.try_counter)
                print("Backtracking done - Solved!!")
                time.sleep(100)
                sys.exit()

            row = next_blank[0]
            col = next_blank[1]
            options = self.game_board.get_options(row, col)
            for i, option in enumerate(options):
                SudokuGui.try_counter += 1
                self.game_board.set_value(row, col, option)
                original_color = pygame.Color(self.get_color(row, col, border_offset=1))
                self.insert_value(row, col, option, color_input='w')
                if SudokuGui.try_counter % 100 == 0:
                    pygame.display.update()
                if self.backtrack():
                    pygame.display.update()
                    print("Backtracking done - Solved!!")
                    time.sleep(10)
                    sys.exit()

                self.insert_value(row, col, option, custom_color=color.Color(original_color))
                self.game_board.remove_value(row, col)
                self.refresh_board()
                # pygame.display.update()
        except RuntimeError as re:
            print("Backtrack Runtime Error", re)

    def solve(self) -> bool:
        try:
            keep_solving = True
            while keep_solving:
                counter = 0
                for ind in self.dict_config:
                    if self.dict_config[ind]['value'] is None:
                        self.set_highlight(ind[0], ind[1], SudokuGui.YELLOW, 1)
                        value = self.game_board.update_value(ind[0], ind[1])
                        if value is False:
                            counter += 1
                            self.set_highlight(ind[0], ind[1], SudokuGui.BLACK, 1)
                        else:
                            counter += 1
                            self.refresh_board()
                            self.insert_value(ind[0], ind[1], value, color_input='w')
                            self.set_highlight(ind[0], ind[1], SudokuGui.BLACK, 1)
                            break
                    else:
                        counter += 1
                if counter >= 81:
                    keep_solving = False
                    return True
        except RuntimeError as re:
            print("Solver Runtime Error", re)

    def setup_puzzle(self):
        self.color_sections()
        self.draw_grid()
        self.fetch_game()
        self.set_gui_data()

    def solve_puzzle(self):
        if self.solve():
            self.backtrack()

    def main_run(self):
        setup_once = True
        solve_once = True
        running = True
        pygame.display.set_caption("Click Anywhere To Start!")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if solve_once:
                        solve_once = False
                        if setup_once:
                            setup_once = False
                            self.setup_puzzle()
                            pygame.display.set_caption(f"Sudoku Solver - Difficulty: {self.difficulty}")
                            pygame.event.pump()
                        try:
                            self.solve_puzzle()
                            sys.exit()
                        except RuntimeError:
                            break
                if event.type == pygame.MOUSEBUTTONDOWN or pygame.MOUSEBUTTONUP:
                    pass

            pygame.display.update()


def main():
    SudokuGui()


if __name__ == '__main__':
    main()
