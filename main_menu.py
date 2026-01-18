import os
import csv
import tkinter as tk
from unit_selection_menu import UnitSelectionMenu
from chapter_selection_menu import ChapterSelectionMenu
from question_amount_menu import QuestionCountMenu
from quiz_ui import start_quiz

DATA_FOLDER = "data"

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.data_folder = DATA_FOLDER
        self.build_ui()

    def get_quiz_files(self):
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        return [f for f in os.listdir(self.data_folder) if f.endswith(".csv")]

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="white")

        tk.Label(self.root, text="Select a Quiz", font=("Arial", 22, "bold"), bg="white").pack(pady=30)

        for file in self.get_quiz_files():
            button_label = file.replace(".csv", "").replace("_", " ").title()
            tk.Button(
                self.root, text=button_label, width=35, height=2,
                command=lambda f=file: self.handle_quiz_selection(f)
            ).pack(pady=8)

    def handle_quiz_selection(self, filename):
        full_path = os.path.join(self.data_folder, filename)
        unique_units = set()
        unique_chapters = set()

        try:
            with open(full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    u = row.get("unit_number", "").strip()
                    c = row.get("chapter_number", "").strip()
                    if u: unique_units.add(u)
                    if c: unique_chapters.add(c)
        except Exception as e:
            print(f"Error reading file: {e}")

        sorted_units = sorted(list(unique_units))
        sorted_chapters = sorted(list(unique_chapters))

        # SKIP LOGIC: If 0 or 1 units exist, skip both selectors
        if len(sorted_units) <= 1:
            self.open_question_amount_menu(self.root, filename, sorted_units, sorted_chapters)
        else:
            UnitSelectionMenu(
                root=self.root,
                data_folder=self.data_folder,
                filename=filename,
                open_next_menu_callback=self.open_chapter_selection,
                show_main_menu_callback=lambda r: MainMenu(r)
            )

    def open_chapter_selection(self, root, filename, selected_units):
        ChapterSelectionMenu(
            root=root,
            data_folder=self.data_folder,
            filename=filename,
            selected_units=selected_units,
            open_next_menu_callback=self.open_question_amount_menu,
            show_main_menu_callback=lambda r: MainMenu(r)
        )

    def open_question_amount_menu(self, root, filename, selected_units, selected_chapters):
        QuestionCountMenu(
            root=root,
            data_folder=self.data_folder,
            filename=filename,
            selected_units=selected_units,
            selected_chapters=selected_chapters,
            start_quiz_callback=start_quiz,
            show_main_menu_callback=lambda r: MainMenu(r)
        )