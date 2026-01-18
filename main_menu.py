import os
import tkinter as tk
from unit_selection_menu import UnitSelectionMenu # Import the new menu
from chapter_selection_menu import ChapterSelectionMenu
from question_amount_menu import QuestionCountMenu
from quiz_ui import start_quiz

DATA_FOLDER = "data"

def get_quiz_files():
    """Return all .csv quiz files in the data folder."""
    files = []
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
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
            # STEP 1: Change this to open Unit Selection first
            command=lambda f=file: open_unit_selection_menu(root, f)
        ).pack(pady=5)

def open_unit_selection_menu(root, filename):
    """
    New Step: Open the screen where the user selects Units.
    """
    UnitSelectionMenu(
        root=root,
        data_folder=DATA_FOLDER,
        filename=filename,
        # After units are picked, it goes to Chapter selection
        open_next_menu_callback=open_chapter_selection_menu,
        show_main_menu_callback=show_main_menu
    )

def open_chapter_selection_menu(root, filename, selected_units):
    """
    STEP 2: Now receives 'selected_units' from UnitSelectionMenu
    """
    ChapterSelectionMenu(
        root=root,
        data_folder=DATA_FOLDER,
        filename=filename,
        selected_units=selected_units, # Now we have the missing argument!
        open_next_menu_callback=open_question_amount_menu,
        show_main_menu_callback=show_main_menu
    )

def open_question_amount_menu(root, filename, selected_units, selected_chapters):
    """
    STEP 3: Ensure this matches the call from ChapterSelectionMenu
    """
    QuestionCountMenu(
        root=root,
        data_folder=DATA_FOLDER,
        filename=filename,
        selected_units=selected_units,
        selected_chapters=selected_chapters,
        start_quiz_callback=start_quiz,
        show_main_menu_callback=show_main_menu
    )