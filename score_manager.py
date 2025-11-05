import csv
from datetime import datetime

# Global variable for current quiz file
current_quiz_file = None

def start_quiz(file):
    global current_quiz_file
    current_quiz_file = file
    print(f"Starting quiz: {current_quiz_file}")
    # Load your quiz and start asking questions here...

def end_quiz(score, total):
    """Call this function when the quiz ends."""
    global current_quiz_file

    # Create a filename for the score log
    score_filename = "quiz_scores.csv"

    # Get timestamp for when the quiz ended
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to CSV file
    with open(score_filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, current_quiz_file, score, total])

    print(f"✅ Score saved to {score_filename}: {score}/{total}")
