import random
from question_loader import load_questions

class QuizLogic:
    def __init__(self, csv_file, selected_units=None, selected_chapters=None, limit=None):
        """
        Initializes the quiz logic with filtered questions.
        If selected_units or selected_chapters are None or empty,
        it treats it as 'Select All'.
        """
        # Load all questions from the CSV file
        all_questions = load_questions(csv_file)

        # 1. Prepare Filter Lists
        # We ensure they are lists so we can use 'in' logic
        units = selected_units if selected_units else []
        chapters = selected_chapters if selected_chapters else []

        # 2. Apply Filtering
        filtered_questions = []
        for q in all_questions:
            # Check Unit Match: Match if unit list is empty OR if unit is in list
            unit_val = q.get("unit_number", "").strip()
            unit_match = not units or unit_val in units

            # Check Chapter Match: Match if chapter list is empty OR if chapter is in list
            chap_val = q.get("chapter_number", "").strip()
            chap_match = not chapters or chap_val in chapters

            if unit_match and chap_match:
                filtered_questions.append(q)

        # 3. Shuffle for variety
        random.shuffle(filtered_questions)

        # 4. Apply Question Limit
        if limit and limit < len(filtered_questions):
            filtered_questions = filtered_questions[:limit]

        # 5. State Management
        self.all_questions = filtered_questions
        self.total_questions = len(filtered_questions)
        self.current_index = 0
        self.score = 0

    def get_current_question(self):
        """Returns the current question dictionary or None if finished."""
        if 0 <= self.current_index < self.total_questions:
            return self.all_questions[self.current_index]
        return None

    def check_answer(self, user_choice):
        """
        Validates the user's answer.
        Returns (is_correct: bool, correct_answer_letter: str)
        """
        current = self.get_current_question()
        if not current:
            return False, None

        correct_letter = current["answer"].strip().upper()
        is_correct = user_choice.strip().upper() == correct_letter

        if is_correct:
            self.score += 1

        return is_correct, correct_letter

    def next_question(self):
        """Advances the index. Returns True if there is another question."""
        if self.current_index < self.total_questions - 1:
            self.current_index += 1
            return True
        return False

    def restart_quiz(self):
        """Resets the quiz state and reshuffles the current set."""
        random.shuffle(self.all_questions)
        self.current_index = 0
        self.score = 0