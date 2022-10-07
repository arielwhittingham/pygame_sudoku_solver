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
    file_name: str = ''
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
        return file_name



