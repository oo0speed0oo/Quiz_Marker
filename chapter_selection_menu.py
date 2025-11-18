# chapter_selection_menu.py
import csv
import tkinter as tk
import os


class ChapterSelectionMenu:
    def __init__(self, root, data_folder, filename, open_next_menu_callback, show_main_menu_callback):
        self.root = root
        self.data_folder = data_folder
        self.filename = filename
        # This will be 'open_question_amount_menu' from the main script
        self.open_next_menu = open_next_menu_callback
        self.show_main_menu = show_main_menu_callback

        self.full_path = os.path.join(self.data_folder, self.filename)
        # Dictionary to hold the state of the checkboxes: {'Chapter 1': tk.IntVar, 'Chapter 2': tk.IntVar, ...}
        self.chapter_vars = {}

        self.unique_chapters = self.get_unique_chapters()

        self.build_ui()

    def get_unique_chapters(self):
        """Read the CSV and return a sorted list of unique chapter numbers."""
        chapters = set()
        try:
            with open(self.full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                # The column name is assumed to be "chapter_number"
                for row in reader:
                    # Strip whitespace just in case and check if the key exists
                    if "chapter_number" in row:
                        chapter = row["chapter_number"].strip()
                        if chapter:  # Ensure it's not an empty string
                            chapters.add(chapter)
        except FileNotFoundError:
            print(f"Error: File not found at {self.full_path}")
            return []
        except KeyError:
            # Handle case where "chapter_number" column is missing
            print("Error: 'chapter_number' column not found in the CSV.")
            return []

        # Sort the chapters numerically/alphabetically for a clean display
        return sorted(list(chapters))

    def build_ui(self):
        """Show the screen that asks which chapters the user wants."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text=f"Quiz: {self.filename}",
            font=("Arial", 16),
            bg="white"
        ).pack(pady=10)

        tk.Label(
            self.root,
            text="Select Chapters",
            font=("Arial", 14),
            bg="white"
        ).pack(pady=10)

        # Create a frame to hold the checkboxes (better organization)
        checkbox_frame = tk.Frame(self.root, bg="white")
        checkbox_frame.pack(pady=10)

        # Create a checkbox for each unique chapter
        for chapter in self.unique_chapters:
            # Create a variable to track the state of the checkbox (1=checked, 0=unchecked)
            var = tk.IntVar(value=1)  # Default to all selected
            self.chapter_vars[chapter] = var

            # Create the Checkbutton
            tk.Checkbutton(
                checkbox_frame,
                text=f"Chapter {chapter}",
                variable=var,
                onvalue=1,
                offvalue=0,
                bg="white",
                anchor="w",  # Align text to the left
            ).pack(fill="x", padx=10, pady=2)  # Fill horizontally within the frame

        tk.Button(
            self.root,
            text="Continue to Question Count",
            font=("Arial", 14),
            width=30,
            command=self.continue_to_question_amount
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Back to Main Menu",
            font=("Arial", 12),
            width=20,
            command=lambda: self.show_main_menu(self.root)
        ).pack(pady=10)

    def continue_to_question_amount(self):
        """Collects the selected chapters and passes them to the next menu."""

        # Get the list of selected chapters
        selected_chapters = []
        for chapter, var in self.chapter_vars.items():
            if var.get() == 1:
                selected_chapters.append(chapter)

        if not selected_chapters:
            # Optional: Show an error if no chapters are selected
            tk.messagebox.showerror("Error", "Please select at least one chapter.")
            return

        # Pass the selected chapters to the function that opens the next menu
        # The next function now needs to accept a list of selected chapters
        self.open_next_menu(self.root, self.filename, selected_chapters)