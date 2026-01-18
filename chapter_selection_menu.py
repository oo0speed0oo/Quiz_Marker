import csv
import tkinter as tk
import os
from tkinter import messagebox


class ChapterSelectionMenu:
    def __init__(
        self,
        root,
        data_folder,
        filename,
        selected_units,
        open_next_menu_callback,
        show_main_menu_callback
    ):
        self.root = root
        self.data_folder = data_folder
        self.filename = filename
        self.selected_units = selected_units
        self.open_next_menu = open_next_menu_callback
        self.show_main_menu = show_main_menu_callback

        self.full_path = os.path.join(self.data_folder, self.filename)

        # Holds checkbox state: { "1": IntVar, "2": IntVar, ... }
        self.chapter_vars = {}

        self.unique_chapters = self.get_unique_chapters()

        if not self.unique_chapters:
            messagebox.showerror(
                "Error",
                "No chapters found for the selected units."
            )
            self.show_main_menu(self.root)
            return

        self.build_ui()

    def get_unique_chapters(self):
        """Return sorted unique chapters limited to selected units."""
        chapters = set()

        try:
            with open(self.full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    unit = row.get("unit_number", "").strip()
                    chapter = row.get("chapter_number", "").strip()

                    if unit in self.selected_units and chapter:
                        chapters.add(chapter)

        except FileNotFoundError:
            print(f"File not found: {self.full_path}")
            return []

        return sorted(chapters)

    def build_ui(self):
        """Build chapter selection screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text=f"Quiz: {self.filename}",
            font=("Arial", 18),
            bg="white"
        ).pack(pady=10)

        tk.Label(
            self.root,
            text="Select Chapters",
            font=("Arial", 16),
            bg="white"
        ).pack(pady=10)

        checkbox_frame = tk.Frame(self.root, bg="white")
        checkbox_frame.pack(padx=20, pady=10)

        num_chapters = len(self.unique_chapters)
        rows_per_column = (num_chapters + 1) // 2

        for i, chapter in enumerate(self.unique_chapters):
            var = tk.IntVar(value=1)
            self.chapter_vars[chapter] = var

            chk = tk.Checkbutton(
                checkbox_frame,
                text=f"Chapter {chapter}",
                variable=var,
                bg="white",
                anchor="w"
            )

            chk.grid(
                row=i % rows_per_column,
                column=i // rows_per_column,
                sticky="w",
                padx=10,
                pady=3
            )

        tk.Button(
            self.root,
            text="Continue to Question Count",
            font=("Arial", 14),
            width=30,
            command=self.continue_forward
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Back to Main Menu",
            font=("Arial", 12),
            width=20,
            command=lambda: self.show_main_menu(self.root)
        ).pack(pady=10)

    def continue_forward(self):
        """Collect selected chapters and move forward."""
        selected_chapters = [
            chapter
            for chapter, var in self.chapter_vars.items()
            if var.get() == 1
        ]

        if not selected_chapters:
            messagebox.showerror(
                "Error",
                "Please select at least one chapter."
            )
            return

        self.open_next_menu(
            self.root,
            self.filename,
            self.selected_units,
            selected_chapters
        )
