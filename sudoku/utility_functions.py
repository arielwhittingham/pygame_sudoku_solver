import tkinter as tk
import datetime
import os

# get screen dimensions using tkinter
def get_screen_dimensions():
    root = tk.Tk()
    dimensions = {'width': root.winfo_screenwidth(), 'height': root.winfo_screenheight()}
    root.quit()
    return dimensions


# create path to save screenshots, for later use
def make_screenshot_save_path(save_path, game_difficulty) -> str:
    date_time_string = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path, mode=0o777)
            os.getcwd()
            file_name = f"{save_path}/{date_time_string}_sudoku_game_difficulty_{game_difficulty}.png"
        else:
            file_name = f"{save_path}/{date_time_string}_sudoku_game_difficulty_{game_difficulty}.png"
        return file_name
    except OSError as ose:
        print(ose, "Can't create file path")
        return ''


# return section number on sudoku board
def get_section(row: int, col: int) -> int:
    """
    :param row: row
    :param col: column
    :return: return 3x3 section on the board

    section numbers:
       |7|8|9|
       |4|5|6|
       |1|2|3|
    """

    if row <= 3:
        if col <= 3:
            return 1
        elif 3 < col <= 6:
            return 2
        else:
            return 3

    elif 3 < row <= 6:
        if col <= 3:
            return 4
        elif 3 < col <= 6:
            return 5
        else:
            return 6
    else:
        if col <= 3:
            return 7
        elif 3 < col <= 6:
            return 8
        else:
            return 9

