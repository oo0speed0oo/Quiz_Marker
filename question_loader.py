import csv

def load_questions(filename):
    questions = []

    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            questions.append({
                "question_number": row["question_number"].strip(),
                "unit_number": row["unit_number"].strip(),
                "chapter_number": row["chapter_number"].strip(),
                "question": row["question"].strip(),
                "choice_a": row["choice_a"].strip(),
                "choice_b": row["choice_b"].strip(),
                "choice_c": row["choice_c"].strip(),
                "choice_d": row["choice_d"].strip(),
                "answer": row["answer"].strip().upper()
            })

    return questions
