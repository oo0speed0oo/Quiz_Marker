import random
from question_loader import load_questions

class QuizLogic:
    def __init__(self, csv_file):
        self.all_questions = load_questions(csv_file)
        random.shuffle(self.all_questions)
        self.total_questions = len(self.all_questions)
        self.current_index = 0
        self.score = 0
        self.skipped = []

    def get_current_question(self):
        """Return the current question dict."""
        if self.current_index < self.total_questions:
            return self.all_questions[self.current_index]
        return None

    def check_answer(self, user_choice):
        """Check if the user_choice matches the correct answer."""
        current = self.get_current_question()
        if not current:
            return False, None

        correct = current["answer"].strip().upper()
        is_correct = (user_choice == correct)
        if is_correct:
            self.score += 1
        return is_correct, correct

    def next_question(self):
        """Move to the next question, if available."""
        if self.current_index < self.total_questions - 1:
            self.current_index += 1
            return True
        return False

    def skip_question(self):
        """Skip the current question and save its index for later review."""
        self.skipped.append(self.current_index)
        return self.next_question()

    def restart_quiz(self):
        """Restart the quiz."""
        random.shuffle(self.all_questions)
        self.current_index = 0
        self.score = 0
        self.skipped = []
