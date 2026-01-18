import csv
import tkinter as tk
import os
from tkinter import messagebox


class QuestionCountMenu:
    def __init__(
        self,
        root,
        data_folder,
        filename,
        selected_units,
        selected_chapters,
        start_quiz_callback,
        show_main_menu_callback
    ):
        self.root = root
        self.data_folder = data_folder
        self.filename = filename
        self.selected_units = selected_units
        self.selected_chapters = selected_chapters
        self.start_quiz = start_quiz_callback
        self.show_main_menu = show_main_menu_callback

        self.full_path = os.path.join(self.data_folder, self.filename)

        self.total_questions = self.count_questions()

        self.build_ui()

    def count_questions(self):
        """
        Count questions filtered by selected units AND chapters.
        """
        count = 0

        try:
            with open(self.full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    unit = row.get("unit_number", "").strip()
                    chapter = row.get("chapter_number", "").strip()

                    if unit in self.selected_units and chapter in self.selected_chapters:
                        count += 1

        except FileNotFoundError:
            print(f"File not found: {self.full_path}")
            return 0
        except Exception as e:
            print(f"CSV read error: {e}")
            return 0

        return count

    def build_ui(self):
        """UI for selecting question count."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text=f"Quiz: {self.filename}",
            font=("Arial", 20),
            bg="white"
        ).pack(pady=10)

        units_text = ", ".join(self.selected_units)
        chapters_text = ", ".join(self.selected_chapters)

        tk.Label(
            self.root,
            text=f"Units: {units_text}",
            font=("Arial", 14),
            bg="white"
        ).pack(pady=2)

        tk.Label(
            self.root,
            text=f"Chapters: {chapters_text}",
            font=("Arial", 14),
            bg="white"
        ).pack(pady=2)

        tk.Label(
            self.root,
            text=f"Total Questions Available: {self.total_questions}",
            font=("Arial", 16),
            bg="white"
        ).pack(pady=10)

        tk.Label(
            self.root,
            text="How many questions do you want?",
            font=("Arial", 16),
            bg="white"
        ).pack(pady=10)

        max_q = max(1, self.total_questions)

        self.spinbox = tk.Spinbox(
            self.root,
            from_=1,
            to=max_q,
            width=6,
            font=("Arial", 14)
        )
        self.spinbox.pack(pady=10)

        tk.Button(
            self.root,
            text="Start Quiz",
            font=("Arial", 16),
            width=20,
            command=self.start_selected_amount
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Back to Main Menu",
            font=("Arial", 12),
            width=20,
            command=lambda: self.show_main_menu(self.root)
        ).pack(pady=10)

    def start_selected_amount(self):
        """Start quiz with selected question limit."""
        if self.total_questions == 0:
            messagebox.showerror(
                "Error",
                "No questions available for the selected unit and chapter."
            )
            return

        amount = int(self.spinbox.get())

        self.start_quiz(
            self.root,
            self.filename,
            amount,
            self.show_main_menu,
            self.selected_units,
            self.selected_chapters
        )
