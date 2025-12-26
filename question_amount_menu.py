import csv
import tkinter as tk
import os


class QuestionCountMenu:
    def __init__(self, root, data_folder, filename, selected_chapters, start_quiz_callback, show_main_menu_callback):
        self.root = root
        self.filename = filename
        self.data_folder = data_folder
        # selected_chapters will be an empty list [] if chapter selection was skipped
        self.selected_chapters = selected_chapters
        self.start_quiz = start_quiz_callback
        self.show_main_menu = show_main_menu_callback

        self.full_path = os.path.join(self.data_folder, self.filename)
        # Use the selected chapters to count questions
        self.total_questions = self.count_questions()

        self.build_ui()

    def count_questions(self):
        """
        Count how many questions exist in the CSV file.
        If self.selected_chapters is empty, count all rows (no chapter filtering).
        If self.selected_chapters is not empty, filter by chapter number.
        """
        count = 0

        # Determine if chapter filtering should be applied
        filter_by_chapter = bool(self.selected_chapters)

        try:
            with open(self.full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:

                    if not filter_by_chapter:
                        # Case 1: No chapters were selected/found (empty list was passed). Count all rows.
                        count += 1
                        continue  # Move to the next row

                    # Case 2: Chapters were selected. Filter based on chapter_number column.
                    if "chapter_number" in row:
                        chapter = row["chapter_number"].strip()
                        if chapter in self.selected_chapters:
                            count += 1

        except FileNotFoundError:
            print(f"Error: File not found at {self.full_path}")
            return 0
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return 0

        return count

    def build_ui(self):
        """Show the screen that asks how many questions the user wants."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text=f"Quiz: {self.filename}",
            font=("Arial", 20),
            bg="white"
        ).pack(pady=10)

        if self.selected_chapters:
            chapters_str = ", ".join(self.selected_chapters)
            display_text = f"Selected Chapters: {chapters_str}"
        else:
            display_text = "Selected Chapters: All (Chapter filtering skipped)"

        tk.Label(
            self.root,
            text=display_text,
            font=("Arial", 16),
            bg="white"
        ).pack(pady=5)

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

        # Check if the total available questions is 0 before starting the quiz
        if self.total_questions == 0:
            tk.messagebox.showerror("Error", "No questions available in the selected data.")
            return

        self.start_quiz(self.root, self.filename, amount, self.show_main_menu, self.selected_chapters)