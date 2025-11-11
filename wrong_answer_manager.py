import csv
import os

DATA_FOLDER = "data"
WRONG_ANSWER_FILE = os.path.join(DATA_FOLDER, "wrong_answers.csv")

class WrongAnswerManager:

    def __init__(self, filename=WRONG_ANSWER_FILE):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create the file with headers if it does not exist."""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "question", "choice_a", "choice_b", "choice_c", "choice_d", "answer"
                ])

    def add_wrong_answer(self, question_dict):
        """Append wrong question to CSV file."""
        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                question_dict["question"],
                question_dict["choice_a"],
                question_dict["choice_b"],
                question_dict["choice_c"],
                question_dict["choice_d"],
                question_dict["answer"]
            ])
