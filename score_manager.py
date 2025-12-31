import csv
from datetime import datetime
import os

# Global variable for current quiz file
current_quiz_file = None
DATA_FOLDER = "data"
SCORE_FILENAME = os.path.join(DATA_FOLDER, "quiz_scores.csv")

def start_quiz(file):
    global current_quiz_file
    current_quiz_file = file
    print(f"Starting quiz: {current_quiz_file}")
    # Load your quiz and start asking questions here...

def ensure_file_exists(self):
    """Create the file with headers if it does not exist."""
    if not os.path.exists(self.filename):
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Test Saved"
            ])

def end_quiz(score, total):
    """Call this function when the quiz ends."""
    global current_quiz_file

    # Get timestamp for when the quiz ended
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to CSV file
    with open(SCORE_FILENAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, current_quiz_file, score, total])

    print(f"✅ Score saved to {SCORE_FILENAME}: {score}/{total}")
