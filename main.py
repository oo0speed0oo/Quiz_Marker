import os
import tkinter as tk
from quiz_logic import QuizLogic
from score_manager import start_quiz as start_quiz_tracking, end_quiz


DATA_FOLDER = "data"
current_quiz_file = None

def get_quiz_files():
    files = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".csv"):
            files.append(file)
    return files

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Select a Quiz", font=("Arial", 18), bg="white").pack(pady=20)

    quiz_files = get_quiz_files()

    for file in quiz_files:
        tk.Button(
            root,
            text=file.replace(".csv", "").replace("_", " ").title(),
            command=lambda f=file: start_quiz(f),
            width=30,
            height=2
        ).pack(pady=5)


# --- Initialize quiz ---
quiz = None  # Will be initialized when a quiz starts

# --- Functions for UI actions ---
def load_question():
    question = quiz.get_current_question()
    if not question:
        show_final_score()
        return

    question_label.config(text=question["question"])
    for letter in ["A", "B", "C", "D"]:
        text = question[f"choice_{letter.lower()}"]
        buttons[letter].config(text=f"{letter}) {text}", state="normal", bg="white")
    result_label.config(text="")
    next_button.config(state="disabled")

def handle_answer(letter):
    is_correct, correct_letter = quiz.check_answer(letter)
    correct_choice = quiz.get_current_question()[f"choice_{correct_letter.lower()}"]

    if is_correct:
        result_label.config(text="✅ Correct!", fg="green")
    else:
        result_label.config(text=f"❌ Wrong! Correct answer: {correct_letter}) {correct_choice}", fg="red")

    # Disable buttons after answering
    for btn in buttons.values():
        btn.config(state="disabled")

    next_button.config(state="normal")

def next_question():
    if quiz.next_question():
        load_question()
    else:
        show_final_score()

def start_quiz(filename):
    global quiz
    quiz = QuizLogic(os.path.join(DATA_FOLDER, filename))
    start_quiz_tracking(filename)  # 🆕 Tell score_manager which quiz started
    build_ui()
    load_question()


def restart_quiz():
    # Restart the same quiz using the saved filename
    global quiz
    quiz = QuizLogic(os.path.join(DATA_FOLDER, current_quiz_file))
    build_ui()
    load_question()

# --- Build UI ---
def build_ui():
    global question_label, result_label, next_button, buttons

    for widget in root.winfo_children():
        widget.destroy()

    # Show current quiz title
    tk.Label(
        root,
        text=f"Now Studying: {current_quiz_file.replace('.csv', '').replace('_', ' ').title()}",
        font=("Arial", 14),
        bg="white"
    ).pack(pady=10)

    question_label = tk.Label(root, text="", bg="white", font=("Arial", 16), wraplength=380)
    question_label.pack(pady=10)

    buttons = {}
    for letter in ["A", "B", "C", "D"]:
        btn = tk.Button(
            root,
            text="",
            command=lambda l=letter: handle_answer(l),
            bg="white",
            width=30,
            height=2
        )
        btn.pack(pady=5)
        buttons[letter] = btn

    result_label = tk.Label(root, text="", bg="white", font=("Arial", 12))
    result_label.pack(pady=10)

    next_button = tk.Button(root, text="Next", command=next_question, state="disabled")
    next_button.pack(pady=10)

    tk.Button(
        root,
        text="Back to Main Menu",
        command=show_main_menu,
        font=("Arial", 12),
        width=20,
        height=1
    ).pack(pady=10)

def show_final_score():
    from score_manager import end_quiz  # (optional safety import)
    for widget in root.winfo_children():
        widget.destroy()

    # 🆕 Save score automatically
    end_quiz(quiz.score, quiz.total_questions)

    tk.Label(
        root,
        text=f"Final Score: {quiz.score}/{quiz.total_questions}",
        font=("Arial", 20),
        bg="white"
    ).pack(pady=40)


# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quiz Marker")
    root.geometry("400x500")
    root.configure(bg="white")

    show_main_menu()

    root.mainloop()
