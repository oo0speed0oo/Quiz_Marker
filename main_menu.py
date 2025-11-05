import os
import tkinter as tk
from quiz_ui import start_quiz

DATA_FOLDER = "data"

def show_main_menu(root):
    """Display the main menu."""
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Quiz Main Menu", font=("Arial", 20), bg="white").pack(pady=20)

    # List all quiz files in the data folder
    quiz_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
    for file in quiz_files:
        tk.Button(
            root,
            text=file,
            command=lambda f=file: start_quiz(root, f, show_main_menu),  # ✅ FIXED
            font=("Arial", 14),
            width=25,
            height=2
        ).pack(pady=5)

    tk.Button(
        root,
        text="Exit",
        command=root.quit,
        font=("Arial", 12),
        width=20,
        height=1
    ).pack(pady=10)
