import os
import tkinter as tk
from quiz_logic import QuizLogic
from score_manager import start_quiz as start_quiz_tracking, end_quiz
from wrong_answer_manager import WrongAnswerManager

DATA_FOLDER = "data"

quiz = None
current_quiz_file = None
question_limit_global = None
wrong_manager = WrongAnswerManager()
# Variable for the chapter filter, needed for restart
selected_chapters_global = None


def start_quiz(root, filename, limit, show_main_menu_callback, selected_chapters):
    """Start the selected quiz."""
    global quiz, current_quiz_file, question_limit_global, selected_chapters_global, current_question_number

    current_question_number = 0

    # FIX 1: The parameter is named 'limit', not 'question_limit'
    question_limit_global = limit
    # NEW: Store the chapters for restart
    selected_chapters_global = selected_chapters

    current_quiz_file = os.path.join(DATA_FOLDER, filename)

    # FIX 2: Pass selected_chapters and use 'limit' as the argument name
    quiz = QuizLogic(
        current_quiz_file,
        selected_chapters=selected_chapters,  # Pass the chapter filter
        limit=limit  # Use the 'limit' parameter
    )

    start_quiz_tracking(filename)

    # FIX 3: Pass the callback correctly to build_ui and load_question
    build_ui(root, show_main_menu_callback)
    load_question(root, show_main_menu_callback)


def build_ui(root, show_main_menu_callback):
    """Build the quiz interface."""
    global question_label, result_label, question_number_label, current_question_label, \
        chapter_number_label, next_button, buttons

    for widget in root.winfo_children():
        widget.destroy()

    # ----- QUESTION + COPY BUTTON -----
    question_frame = tk.Frame(root, bg="white")
    question_frame.pack(pady=20)

    question_label = tk.Label(
        question_frame,
        text="",
        bg="white",
        font=("Arial", 16),
        wraplength=380,
        justify="left"
    )
    question_label.pack(padx=5)

    def copy_question():
        root.clipboard_clear()
        root.clipboard_append(question_label.cget("text"))

    tk.Button(
        question_frame,
        text="Copy Question",
        command=copy_question
    ).pack(padx=5)

    # ----- QUESTION NUMBER LABEL -----
    question_number_label = tk.Label(
        question_frame,
        text="Q #: ",  # prefix text
        bg="white",
        font=("Arial", 16),
        wraplength=380,
        justify="center"
    )
    question_number_label.pack(padx=5)

    # ----- CHAPTER NUMBER LABEL -----
    chapter_number_label = tk.Label(
        question_frame,
        text="Ch #: ",  # prefix text
        bg="white",
        font=("Arial", 16),
        wraplength=380,
        justify="center"
    )
    chapter_number_label.pack(padx=5)

    # ----- CURRENT QUESTION NUMBER LABEL -----
    current_question_label = tk.Label(
        question_frame,
        text=" ",  # prefix text
        bg="white",
        font=("Arial", 16),
        wraplength=380,
        justify="center"
    )
    current_question_label.pack(padx=5)

    # ----- ANSWER BUTTONS -----
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
    global current_question_number
    question = quiz.get_current_question()
    if not question:
        show_final_score(root, show_main_menu_callback)
        return

    # Increment question counter
    current_question_number += 1

    # Update QUESTION label
    question_label.config(text=question["question"])

    # Update QUESTION NUMBER label only if it exists
    if "question_number" in question and question["question_number"]:
        question_number_label.config(text=f"Q #: {question['question_number']}")
        question_number_label.pack()  # ensure it is visible
    else:
        question_number_label.pack_forget()  # hide if missing

    # Update QUESTION CHAPTER label only if it exists
    if "chapter_number" in question and question["chapter_number"]:
        chapter_number_label.config(text=f"Ch #: {question['chapter_number']}")
        chapter_number_label.pack()  # ensure it is visible
    else:
        chapter_number_label.pack_forget()  # hide if missing

    # ----- CURRENT PROGRESS (e.g., 2 / 40) -----
    current_question_label.config(
        text=f"Progress: {current_question_number} / {quiz.total_questions}"
    )
    current_question_label.pack()

    # Update answer buttons
    for letter in ["A", "B", "C", "D"]:
        text = question[f"choice_{letter.lower()}"]
        buttons[letter].config(text=f"{letter}) {text}", state="normal", bg="white")

    result_label.config(text="")
    next_button.config(state="disabled")


def handle_answer(root, letter, show_main_menu_callback):
    is_correct, correct_letter = quiz.check_answer(letter)
    question = quiz.get_current_question()
    correct_choice = question[f"choice_{correct_letter.lower()}"]

    if is_correct:
        result_label.config(text=f"✅ {correct_choice} is correct!", fg="green")
    else:
        result_label.config(
            text=f"❌ {letter} Wrong! Correct: {correct_letter}) {correct_choice}",
            fg="red"
        )

        # SAVE WRONG ANSWER
        wrong_manager.add_wrong_answer(question)

    # disable buttons
    for btn in buttons.values():
        btn.config(state="disabled")

    next_button.config(state="normal")


def next_question(root, show_main_menu_callback):
    if quiz.next_question():
        load_question(root, show_main_menu_callback)
    else:
        show_final_score(root, show_main_menu_callback)


def show_final_score(root, show_main_menu_callback):
    global current_quiz_file, question_limit_global, selected_chapters_global

    for widget in root.winfo_children():
        widget.destroy()

    score_text = f"Final Score: {quiz.score}/{quiz.total_questions}"
    tk.Label(root, text=score_text, font=("Arial", 25), bg="white").pack(pady=40)

    # end_quiz(os.path.basename(current_quiz_file), quiz.score, quiz.total_questions)
    end_quiz(quiz.score, quiz.total_questions)

    # Restart with the SAME question limit AND chapter filter
    tk.Button(
        root,
        text="Restart Quiz",
        command=lambda: start_quiz(
            root,
            os.path.basename(current_quiz_file),
            question_limit_global,
            show_main_menu_callback,
            selected_chapters_global  # NEW: Pass the stored chapter list
        ),
        font=("Arial", 20),
        width=20,
        height=2
    ).pack(pady=10)

    tk.Button(
        root,
        text="Back to Main Menu",
        command=lambda: show_main_menu_callback(root),
        font=("Arial", 20),
        width=20,
        height=2
    ).pack(pady=10)