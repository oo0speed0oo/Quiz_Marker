import random
from question_loader import load_questions

class QuizLogic:
    def __init__(self, csv_file, selected_chapters=None, limit=None):
        # 1. Load all questions from CSV
        all_questions = load_questions(csv_file)

        # 2. NEW: Filter questions based on selected chapters
        if selected_chapters:
            self.all_questions = self.filter_questions(all_questions, selected_chapters)
        else:
            self.all_questions = all_questions

        # 3. Shuffle (on the filtered list)
        random.shuffle(self.all_questions)

        # 4. Apply limit (on the filtered and shuffled list)
        if limit is not None:
            self.all_questions = self.all_questions[:limit]

        # Stats
        self.total_questions = len(self.all_questions)
        self.current_index = 0
        self.score = 0
        self.skipped = []

    def filter_questions(self, questions, chapters):
        """Filters the list of questions to include only those in the selected chapters."""
        filtered = []
        # 'chapters' is a list of strings, e.g., ['1', '2']
        for q in questions:
            # We assume 'chapter_number' is the key in the question dictionary
            if q.get("chapter_number", "").strip() in chapters:
                filtered.append(q)
        return filtered

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
