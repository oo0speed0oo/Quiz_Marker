import csv
import tkinter as tk
import os
from tkinter import messagebox


class QuestionCountMenu:
    def __init__(self, root, data_folder, filename, selected_units, selected_chapters, start_quiz_callback,
                 show_main_menu_callback):
        self.root = root
        self.data_folder = data_folder
        self.filename = filename
        self.selected_units = selected_units
        self.selected_chapters = selected_chapters
        self.start_quiz = start_quiz_callback
        self.show_main_menu = show_main_menu_callback
        self.full_path = os.path.join(self.data_folder, self.filename)

        # Calculate questions using the same safe .get() logic
        self.total_questions = self.count_questions()
        self.build_ui()

    def count_questions(self):
        count = 0
        try:
            with open(self.full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Match the safe loader logic
                    u = row.get("unit_number", "").strip()
                    c = row.get("chapter_number", "").strip()

                    unit_ok = not self.selected_units or u in self.selected_units
                    chap_ok = not self.selected_chapters or c in self.selected_chapters

                    if unit_ok and chap_ok:
                        count += 1
        except:
            return 0
        return count

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="white")

        tk.Label(self.root, text="Quiz Setup", font=("Arial", 20, "bold"), bg="white").pack(pady=20)
        tk.Label(self.root, text=f"Total Questions: {self.total_questions}", font=("Arial", 14), bg="white").pack(
            pady=10)

        # 1. Create the widget
        self.spinbox = tk.Spinbox(
            self.root,
            from_=1,
            to=max(1, self.total_questions),
            width=10,
            font=("Arial", 18),
            justify="center",
            highlightthickness=1,  # Forces a border to be drawn
            highlightbackground="black"
        )

        # 2. LOAD ORDER: Pack it BEFORE setting value
        self.spinbox.pack(pady=20)

        # 3. FORCE REFRESH: This fixes the "invisible until click" on Mac/Windows
        self.root.update()

        # 4. SET VALUE: Now that the widget is 'alive'
        self.spinbox.delete(0, "end")
        self.spinbox.insert(0, str(self.total_questions))

        tk.Button(
            self.root, text="START QUIZ", font=("Arial", 14, "bold"),
            bg="#4CAF50", width=20, height=2,
            command=self.start_selected_amount
        ).pack(pady=20)

        tk.Button(self.root, text="Back", command=lambda: self.show_main_menu(self.root)).pack()

    def start_selected_amount(self):
        val = self.spinbox.get().strip()
        try:
            # If the box is glitched/empty, use total_questions
            amount = int(val) if val else self.total_questions
            self.start_quiz(self.root, self.filename, amount, self.show_main_menu, self.selected_units,
                            self.selected_chapters)
        except:
            # Emergency fallback: just start with all questions
            self.start_quiz(self.root, self.filename, self.total_questions, self.show_main_menu, self.selected_units,
                            self.selected_chapters)