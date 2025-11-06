import os
import tkinter as tk

from question_amount_menu import QuestionCountMenu
from quiz_ui import start_quiz  # start_quiz(root, filename, limit, show_main_menu)

DATA_FOLDER = "data"


def get_quiz_files():
    """Return all .csv quiz files in the data folder."""
    files = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".csv"):
            files.append(file)
    return files


def show_main_menu(root):
    """Display the main menu screen."""
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(
        root,
        text="Select a Quiz",
        font=("Arial", 20),
        bg="white"
    ).pack(pady=20)

    quiz_files = get_quiz_files()

    for file in quiz_files:
        button_label = file.replace(".csv", "").replace("_", " ").title()

        tk.Button(
            root,
            text=button_label,
            width=30,
            height=2,
            command=lambda f=file: open_question_amount_menu(root, f)
        ).pack(pady=5)


def open_question_amount_menu(root, filename):
    """
    Open the screen where the user selects how many questions they want.
    """

    # Create the question amount UI
    QuestionCountMenu(
        root=root,
        data_folder=DATA_FOLDER,
        filename=filename,
        start_quiz_callback=start_quiz,           # quiz begins after selecting amount
        show_main_menu_callback=show_main_menu    # return function
    )
