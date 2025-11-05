import csv

def load_questions(filename):
    """
    Load quiz questions from a CSV file and return a list of dictionaries.
    Each dict has keys: question, choice_a, choice_b, choice_c, choice_d, answer
    """
    questions = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append(row)
    return questions
