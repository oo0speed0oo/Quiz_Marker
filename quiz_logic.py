import random
from question_loader import load_questions


class QuizLogic:
    def __init__(self, csv_file, selected_chapters=None, limit=None):
        all_questions = load_questions(csv_file)

        all_questions = [
            q for q in all_questions
            if q["unit_number"] in selected_units
            and q["chapter_number"] in selected_chapters
        ]

        random.shuffle(all_questions)

        if limit:
            all_questions = all_questions[:limit]

        self.all_questions = all_questions
        self.total_questions = len(all_questions)
        self.current_index = 0
        self.score = 0

    def _filter_questions_by_chapter(self, questions, chapters):
        """Return only questions whose chapter_number is in chapters."""
        filtered = []

        for q in questions:
            chapter = q.get("chapter_number", "").strip()
            if chapter in chapters:
                filtered.append(q)

        return filtered

    def get_current_question(self):
        """Return the current question dict or None."""
        if self.current_index < self.total_questions:
            return self.all_questions[self.current_index]
        return None

    def check_answer(self, user_choice):
        """Check if the user_choice matches the correct answer."""
        current = self.get_current_question()
        if not current:
            return False, None

        correct = current["answer"].strip().upper()
        is_correct = user_choice.upper() == correct

        if is_correct:
            self.score += 1

        return is_correct, correct

    def next_question(self):
        """Advance to the next question. Returns True if possible."""
        if self.current_index < self.total_questions - 1:
            self.current_index += 1
            return True
        return False

    def skip_question(self):
        """Skip the current question and remember it."""
        self.skipped.append(self.current_index)
        return self.next_question()

    def restart_quiz(self):
        """Restart the quiz with the same question set."""
        random.shuffle(self.all_questions)
        self.current_index = 0
        self.score = 0
        self.skipped.clear()
