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

        if not self.unique_chapters:
            print(f"No chapters found in {self.filename}. Skipping chapter selection menu.")
            for widget in self.root.winfo_children():
                widget.destroy()
            self.open_next_menu(self.root, self.filename, [])
            return

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

        # Create a frame to hold the checkboxes
        checkbox_frame = tk.Frame(self.root, bg="white")
        checkbox_frame.pack(pady=10, padx=20)  # Add some padding to the frame

        # --- Change starts here: Use .grid() for two columns ---

        # Calculate the number of items per column
        num_chapters = len(self.unique_chapters)
        # Determine the number of rows needed
        rows_per_column = (num_chapters + 1) // 2

        # Keep track of the current row and column
        row_counter = 0
        col_counter = 0

        # Create a checkbox for each unique chapter
        for i, chapter in enumerate(self.unique_chapters):
            # Create a variable to track the state of the checkbox (1=checked, 0=unchecked)
            var = tk.IntVar(value=1)  # Default to all selected
            self.chapter_vars[chapter] = var

            # Create the Checkbutton
            chk = tk.Checkbutton(
                checkbox_frame,
                text=f"Chapter {chapter}",
                variable=var,
                onvalue=1,
                offvalue=0,
                bg="white",
                anchor="w",  # Align text to the left
            )

            # Place the Checkbutton in the grid
            # i // rows_per_column determines the column (0 for first half, 1 for second half)
            # i % rows_per_column determines the row within that column
            chk.grid(
                row=i % rows_per_column,
                column=i // rows_per_column,
                sticky="w",  # Stick to the west (left) side of the cell
                padx=10,
                pady=2
            )

        # --- Change ends here ---

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