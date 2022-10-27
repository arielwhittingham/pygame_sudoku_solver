import tkinter as tk
import datetime
import os
from fpdf import FPDF as PDF
import pathlib


# get screen dimensions using tkinter
def get_screen_dimensions():
    root = tk.Tk()
    dimensions = {'width': root.winfo_screenwidth(), 'height': root.winfo_screenheight()}
    root.quit()
    return dimensions


# create path to save screenshots, for later use
def make_save_path(save_path, game_difficulty, extension=".png") -> str:
    date_time_string = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path, mode=0o777)
            os.getcwd()
            file_name = f"{os.getcwd()}/{save_path}/{date_time_string}_sudoku_game_difficulty_{game_difficulty}.{extension}"
        else:
            file_name = f"{os.getcwd()}/{save_path}/{date_time_string}_sudoku_game_difficulty_{game_difficulty}.{extension}"
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


def get_newest_screenshots(sub_folder: str) -> pathlib.Path:
    """
    Return latest file in each screenshot directory
    """
    cwd = pathlib.Path(os.getcwd())
    file_names = os.listdir(pathlib.Path.joinpath(cwd, sub_folder))
    file_names.sort(reverse=True)
    return pathlib.Path.joinpath(cwd, sub_folder, file_names[0])


def create_pdf(unsolved_screenshot: str, solved_screenshot: str, game_difficulty):
    try:
        with open(f"{unsolved_screenshot}") as f:
            f.close()
        with open(f"{solved_screenshot}") as f:
            f.close()

    except OSError:
        print("Failed to open screenshot files in /files directory")

    try:
        pdf_object = PDF(orientation='L')  # pdf object
        pdf_object.add_page()
        pdf_object.image(str(unsolved_screenshot), x=0, y=0, w=100, h=100)
        pdf_object.image(str(solved_screenshot), x=pdf_object.w - 100, y=0, w=100, h=100)
        pdf_object.output(make_save_path('files/pdf', game_difficulty, extension=".pdf"), 'F')
    except OSError:
        print("Failed to create PDF output")
