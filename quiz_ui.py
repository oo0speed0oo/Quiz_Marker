import os
import tkinter as tk
from quiz_logic import QuizLogic
from score_manager import start_quiz as start_quiz_tracking, end_quiz
from wrong_answer_manager import WrongAnswerManager

DATA_FOLDER = "data"

# Global state to allow for restarting and UI updates
quiz = None
current_quiz_file = None
question_limit_global = None
selected_units_global = None
selected_chapters_global = None
current_question_number = 0

wrong_manager = WrongAnswerManager()


def start_quiz(
        root,
        filename,
        question_limit,
        show_main_menu_callback,
        selected_units,  # Added parameter
        selected_chapters
):
    """Start the quiz with unit/chapter filtering and question limit."""
    global quiz, current_quiz_file, question_limit_global
    global selected_units_global, selected_chapters_global, current_question_number

    current_question_number = 0
    question_limit_global = question_limit
    selected_units_global = selected_units
    selected_chapters_global = selected_chapters
    current_quiz_file = os.path.join(DATA_FOLDER, filename)

    # Initialize Logic with both Unit and Chapter filters
    quiz = QuizLogic(
        current_quiz_file,
        selected_units=selected_units,
        selected_chapters=selected_chapters,
        limit=question_limit
    )

    start_quiz_tracking(filename)

    build_ui(root, show_main_menu_callback)
    load_question(root, show_main_menu_callback)


def build_ui(root, show_main_menu_callback):
    """Build the quiz interface buttons and labels."""
    global question_label, result_label, question_number_label
    global chapter_number_label, progress_label, next_button, buttons

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="white")

    # Question Display
    question_frame = tk.Frame(root, bg="white")
    question_frame.pack(pady=20)

    question_label = tk.Label(
        question_frame, text="", font=("Arial", 16),
        wraplength=600, justify="left", bg="white"
    )
    question_label.pack(pady=5)

    tk.Button(
        question_frame, text="Copy Question",
        command=lambda: (root.clipboard_clear(), root.clipboard_append(question_label.cget("text")))
    ).pack(pady=5)

    # Metadata (Question #, Chapter, Progress)
    question_number_label = tk.Label(question_frame, text="", font=("Arial", 12), bg="white")
    question_number_label.pack()

    chapter_number_label = tk.Label(question_frame, text="", font=("Arial", 12), bg="white")
    chapter_number_label.pack()

    progress_label = tk.Label(question_frame, text="", font=("Arial", 12), bg="white")
    progress_label.pack(pady=5)

    # Answer Buttons
    buttons = {}
    for letter in ["A", "B", "C", "D"]:
        btn = tk.Button(
            root, text="", font=("Arial", 14), width=45, height=2, bg="white",
            command=lambda l=letter: handle_answer(root, l, show_main_menu_callback)
        )
        btn.pack(pady=5)
        buttons[letter] = btn

    result_label = tk.Label(root, text="", font=("Arial", 14), bg="white")
    result_label.pack(pady=10)

    next_button = tk.Button(
        root, text="Next Question", font=("Arial", 14), state="disabled",
        command=lambda: next_question(root, show_main_menu_callback)
    )
    next_button.pack(pady=10)

    tk.Button(
        root, text="Back to Main Menu", font=("Arial", 12),
        command=lambda: show_main_menu_callback(root)
    ).pack(pady=10)


def load_question(root, show_main_menu_callback):
    """Update UI with data from the current question."""
    global current_question_number
    question = quiz.get_current_question()

    if not question:
        show_final_score(root, show_main_menu_callback)
        return

    current_question_number += 1
    question_label.config(text=question["question"])

    qn = question.get("question_number", "").strip()
    question_number_label.config(text=f"Question #: {qn}" if qn else "")

    ch = question.get("chapter_number", "").strip()
    chapter_number_label.config(text=f"Chapter: {ch}" if ch else "")

    progress_label.config(text=f"Progress: {current_question_number} / {quiz.total_questions}")

    for letter in ["A", "B", "C", "D"]:
        choice_text = question.get(f"choice_{letter.lower()}", "")
        buttons[letter].config(text=f"{letter}) {choice_text}", state="normal", bg="white")

    result_label.config(text="")
    next_button.config(state="disabled")


def handle_answer(root, letter, show_main_menu_callback):
    """Check answer and update visuals."""
    is_correct, correct_letter = quiz.check_answer(letter)
    question = quiz.get_current_question()
    correct_text = question[f"choice_{correct_letter.lower()}"]

    if is_correct:
        result_label.config(text=f"✅ Correct: {correct_text}", fg="green")
    else:
        result_label.config(text=f"❌ Wrong. Correct: {correct_letter}) {correct_text}", fg="red")
        wrong_manager.add_wrong_answer(question)

    for btn in buttons.values():
        btn.config(state="disabled")
    next_button.config(state="normal")


def next_question(root, show_main_menu_callback):
    if quiz.next_question():
        load_question(root, show_main_menu_callback)
    else:
        show_final_score(root, show_main_menu_callback)


def show_final_score(root, show_main_menu_callback):
    """Final screen with results and restart option."""
    for widget in root.winfo_children():
        widget.destroy()

    end_quiz(quiz.score, quiz.total_questions)

    tk.Label(root, text=f"Final Score: {quiz.score} / {quiz.total_questions}",
             font=("Arial", 26), bg="white").pack(pady=40)

    tk.Button(
        root, text="Restart Quiz", font=("Arial", 18), width=20,
        command=lambda: start_quiz(
            root, os.path.basename(current_quiz_file), question_limit_global,
            show_main_menu_callback, selected_units_global, selected_chapters_global
        )
    ).pack(pady=10)

    tk.Button(
        root, text="Back to Main Menu", font=("Arial", 18), width=20,
        command=lambda: show_main_menu_callback(root)
    ).pack(pady=10)