import os
import tkinter as tk
from quiz_logic import QuizLogic
from score_manager import start_quiz as start_quiz_tracking, end_quiz

DATA_FOLDER = "data"

quiz = None
current_quiz_file = None
question_limit_global = None


def start_quiz(root, filename, question_limit, show_main_menu_callback):
    """Start the selected quiz."""
    global quiz, current_quiz_file, question_limit_global

    question_limit_global = question_limit
    current_quiz_file = os.path.join(DATA_FOLDER, filename)

    quiz = QuizLogic(current_quiz_file, limit=question_limit)

    # Start score tracking
    start_quiz_tracking(filename)

    build_ui(root, show_main_menu_callback)
    load_question(root, show_main_menu_callback)


def build_ui(root, show_main_menu_callback):
    """Build the quiz interface."""
    global question_label, result_label, next_button, buttons

    for widget in root.winfo_children():
        widget.destroy()

    question_label = tk.Label(root, text="", bg="white", font=("Arial", 16), wraplength=380)
    question_label.pack(pady=20)

    buttons = {}
    for letter in ["A", "B", "C", "D"]:
        btn = tk.Button(
            root,
            text="",
            command=lambda l=letter: handle_answer(root, l, show_main_menu_callback),
            bg="white",
            width=30,
            height=2
        )
        btn.pack(pady=5)
        buttons[letter] = btn

    result_label = tk.Label(root, text="", bg="white", font=("Arial", 12))
    result_label.pack(pady=10)

    next_button = tk.Button(
        root,
        text="Next",
        command=lambda: next_question(root, show_main_menu_callback),
        state="disabled"
    )
    next_button.pack(pady=10)

    tk.Button(
        root,
        text="Back to Main Menu",
        command=lambda: show_main_menu_callback(root),
        font=("Arial", 12),
        width=20,
        height=1
    ).pack(pady=10)


def load_question(root, show_main_menu_callback):
    question = quiz.get_current_question()
    if not question:
        show_final_score(root, show_main_menu_callback)
        return

    question_label.config(text=question["question"])

    for letter in ["A", "B", "C", "D"]:
        text = question[f"choice_{letter.lower()}"]
        buttons[letter].config(text=f"{letter}) {text}", state="normal", bg="white")

    result_label.config(text="")
    next_button.config(state="disabled")


def handle_answer(root, letter, show_main_menu_callback):
    is_correct, correct_letter = quiz.check_answer(letter)
    correct_choice = quiz.get_current_question()[f"choice_{correct_letter.lower()}"]

    if is_correct:
        result_label.config(text="✅ Correct!", fg="green")
    else:
        result_label.config(text=f"❌ Wrong! Correct answer: {correct_letter}) {correct_choice}",
                            fg="red")

    for btn in buttons.values():
        btn.config(state="disabled")

    next_button.config(state="normal")


def next_question(root, show_main_menu_callback):
    if quiz.next_question():
        load_question(root, show_main_menu_callback)
    else:
        show_final_score(root, show_main_menu_callback)


def show_final_score(root, show_main_menu_callback):
    """Show final score and save."""
    for widget in root.winfo_children():
        widget.destroy()

    score_text = f"Final Score: {quiz.score}/{quiz.total_questions}"
    tk.Label(root, text=score_text, font=("Arial", 20), bg="white").pack(pady=40)

    # Save score
    end_quiz(os.path.basename(current_quiz_file), quiz.score, quiz.total_questions)

    # Restart button WITH LIMIT INCLUDED
    tk.Button(
        root,
        text="Restart Quiz",
        command=lambda: start_quiz(
            root,
            os.path.basename(current_quiz_file),
            question_limit_global,
            show_main_menu_callback,
        ),
        font=("Arial", 14),
        width=20,
        height=2
    ).pack(pady=10)

    tk.Button(
        root,
        text="Back to Main Menu",
        command=lambda: show_main_menu_callback(root),
        font=("Arial", 14),
        width=20,
        height=2
    ).pack(pady=10)
