import csv
import tkinter as tk
import os


class QuestionCountMenu:
    def __init__(self, root, data_folder, filename, selected_chapters, start_quiz_callback, show_main_menu_callback):
        self.root = root
        self.filename = filename
        self.data_folder = data_folder
        self.selected_chapters = selected_chapters  # NEW
        self.start_quiz = start_quiz_callback
        self.show_main_menu = show_main_menu_callback

        self.full_path = os.path.join(self.data_folder, self.filename)
        # Use the selected chapters to count questions
        self.total_questions = self.count_questions()

        self.build_ui()

    def count_questions(self):
        """Count how many questions exist in the CSV file for the selected chapters."""
        count = 0
        with open(self.full_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Filter questions based on the selected chapters
                if "chapter_number" in row and row["chapter_number"].strip() in self.selected_chapters:
                    count += 1
        return count

    def build_ui(self):
        """Show the screen that asks how many questions the user wants."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text=f"Quiz: {self.filename}",
            font=("Arial", 16),
            bg="white"
        ).pack(pady=10)

        chapters_str = ", ".join(self.selected_chapters)
        tk.Label(
            self.root,
            text=f"Selected Chapters: {chapters_str}",
            font=("Arial", 12),
            bg="white"
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=f"Total Questions Available: {self.total_questions}",
            font=("Arial", 14),
            bg="white"
        ).pack(pady=10)

        tk.Label(
            self.root,
            text="How many questions do you want?",
            font=("Arial", 14),
            bg="white"
        ).pack(pady=10)

        # Spinbox from 1 to total questions (adjust to avoid 0 if count is 0)
        max_q = max(1, self.total_questions)  # Ensure 'from_' is 1 even if total is 0
        self.spinbox = tk.Spinbox(
            self.root,
            from_=1,
            to=max_q,
            width=5,
            font=("Arial", 14)
        )
        self.spinbox.pack(pady=10)
        self.root.update()


        tk.Button(
            self.root,
            text="Start Quiz",
            font=("Arial", 14),
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
        """User picks how many questions to answer."""
        amount = int(self.spinbox.get())
        self.start_quiz(self.root, self.filename, amount, self.show_main_menu, self.selected_chapters)
