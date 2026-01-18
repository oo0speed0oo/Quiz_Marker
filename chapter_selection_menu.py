import csv
import tkinter as tk
import os
from tkinter import messagebox


class ChapterSelectionMenu:
    def __init__(self, root, data_folder, filename, selected_units, open_next_menu_callback, show_main_menu_callback):
        self.root = root
        self.data_folder = data_folder
        self.filename = filename
        self.selected_units = selected_units
        self.open_next_menu = open_next_menu_callback
        self.show_main_menu = show_main_menu_callback
        self.full_path = os.path.join(self.data_folder, self.filename)
        self.chapter_vars = {}

        self.unique_chapters = self.get_unique_chapters()

        if not self.unique_chapters:
            messagebox.showerror("Error", "No chapters found for the selected criteria.")
            self.show_main_menu(self.root)
            return
        self.build_ui()

    def get_unique_chapters(self):
        chapters = set()
        try:
            with open(self.full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    unit = row.get("unit_number", "").strip()
                    chapter = row.get("chapter_number", "").strip()
                    # If units were skipped (empty list), allow all chapters
                    if not self.selected_units or unit in self.selected_units:
                        if chapter:
                            chapters.add(chapter)
        except Exception as e:
            print(f"Error reading chapters: {e}")
        return sorted(chapters)

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Select Chapters", font=("Arial", 18), bg="white").pack(pady=10)

        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=10)

        for i, chapter in enumerate(self.unique_chapters):
            var = tk.IntVar(value=1)
            self.chapter_vars[chapter] = var
            tk.Checkbutton(frame, text=f"Chapter {chapter}", variable=var, bg="white").grid(row=i // 2, column=i % 2,
                                                                                            sticky="w", padx=10)

        tk.Button(self.root, text="Continue", command=self.continue_forward, width=20).pack(pady=20)
        tk.Button(self.root, text="Back", command=lambda: self.show_main_menu(self.root)).pack()

    def continue_forward(self):
        selected = [c for c, v in self.chapter_vars.items() if v.get() == 1]
        if not selected:
            messagebox.showwarning("Warning", "Select at least one chapter.")
            return
        self.open_next_menu(self.root, self.filename, self.selected_units, selected)