import csv
import tkinter as tk
import os

class UnitSelectionMenu:
    def __init__(self, root, data_folder, filename, open_next_menu_callback, show_main_menu_callback):
        self.root = root
        self.data_folder = data_folder
        self.filename = filename
        self.open_next_menu = open_next_menu_callback
        self.show_main_menu = show_main_menu_callback

        self.full_path = os.path.join(self.data_folder, self.filename)
        self.unit_vars = {}
        self.units = self.get_unique_units()
        self.build_ui()

    def get_unique_units(self):
        units = set()
        with open(self.full_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                units.add(row["unit_number"].strip())
        return sorted(units)

    def build_ui(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="Select Unit", font=("Arial", 18), bg="white").pack(pady=10)

        frame = tk.Frame(self.root, bg="white")
        frame.pack()

        for unit in self.units:
            var = tk.IntVar(value=1)
            self.unit_vars[unit] = var
            tk.Checkbutton(
                frame,
                text=f"Unit {unit}",
                variable=var,
                bg="white"
            ).pack(anchor="w")

        tk.Button(
            self.root,
            text="Continue to Chapter Selection",
            command=self.continue_forward,
            font=("Arial", 14),
            width=30
        ).pack(pady=20)

    def continue_forward(self):
        selected_units = [u for u, v in self.unit_vars.items() if v.get() == 1]
        self.open_next_menu(self.root, self.filename, selected_units)
