import json

class Flashcard:
    def __init__(self, topic, phase, answer, id=None):
        self.id = id
        self.topic = topic
        self.phase = phase
        self.answer = answer

    def __str__(self):
        return f"{self.id}: {self.topic}: {self.phase}: {self.answer}"

    def to_dict(self):
        return {"id": self.id, "topic": self.topic, "phase": self.phase, "answer": self.answer}


def save_flashcard(flashcard, filename="flashcards.json"):
    try:
        with open(filename, "r") as file:
            content = file.read().strip()
            if content:
                flashcards = json.loads(content)
            else:
                flashcards = []
    except FileNotFoundError:
        flashcards = []
        print("No existing flashcards found, creating new list.")  # Debug statement

    flashcard.id = len(flashcards) + 1
    flashcards.append(flashcard.to_dict())
    print("Flashcard to be saved:", flashcards)  # Debug statement

    with open(filename, "w") as file:
        json.dump(flashcards, file, indent=4)
        print("Flashcards saved to file.")  # Debug statement


def clear_flashcards(filename="flashcards.json"):
    with open(filename, "w") as file:
        json.dump([], file, indent=4)
    print("Flashcards cleared from file.")


def student_mode():
    streak = 0
    amountofcorrectAnswers = 0
    score = 0
    try:
        with open("flashcards.json", "r") as file:
            content = file.read().strip()
            if content:
                flashcards = json.loads(content)
            else:
                flashcards = []
    except FileNotFoundError:
        flashcards = []
        print("No flashcards found.")
        return

    if not flashcards:
        print("No flashcards found.")
        return

    while True:
        for card in flashcards:
            print(f"{card['id']}: {card['topic']}: {card['phase']}")
        try:
            flashcard_id = int(input("Enter the flashcard number you want to see (or 0 to exit): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if flashcard_id == 0:
            break

        found = False
        for card in flashcards:
            if card['id'] == flashcard_id:
                found = True
                print(f"Flashcard {flashcard_id} | {card['topic']}")
                print(f"Phase: {card['phase']}")
                while True:
                    answerAttempt = input("Enter your answer: ")
                    if answerAttempt == card['answer']:
                        print("Correct!")
                        streak += 1
                        amountofcorrectAnswers += 1
                        score = ((streak * 0.5) + amountofcorrectAnswers) + score
                        print(f"You have a score of {score}")
                        if streak > 0:
                            print(f"Your streak is {streak}!")
                        break
                    else:
                        print("Incorrect. Try again.")
                        print(f"You lost your streak of {streak}!")
                        print(f"You have a score of {score}")
                        streak = 0
                break

        if not found:
            print(f"Flashcard {flashcard_id} not found.")


def teacher_mode():
    while True:
        action = input("What would you like to do? (add/clear/view flashcards/exit): ").lower()
        if action == "add":
            topic = input("Enter the topic: ")
            phase = input("Enter the phase: ")
            answer = input("Enter the answer: ")
            flashcard = Flashcard(topic, phase, answer)
            save_flashcard(flashcard)
        elif action == "clear":
            confirmation = input("Are you sure you want to clear all flashcards? (y/n): ").lower()
            if confirmation == "y":
                clear_flashcards()
            else:
                print("Flashcards not cleared.")
        elif action == "view":
            try:
                with open("flashcards.json", "r") as file:
                    content = file.read().strip()
                    if content:
                        flashcards = json.loads(content)
                    else:
                        flashcards = []
                if not flashcards:
                    print("No flashcards found.")
                else:
                    for card in flashcards:
                        print(f"{card['id']}: {card['topic']}: {card['phase']}, Answer: {card['answer']}")
            except FileNotFoundError:
                print("No flashcards found.")
        elif action == "exit":
            break
        else:
            print("Invalid action. Please choose add, clear, view, or exit.")


# Main Program
clear_flashcards()

while True:
    user_type = input("Are you a teacher or a student? (teacher/student/exit): ").lower()

    if user_type == "teacher":
        teacher_mode()
    elif user_type == "student":
        student_mode()
    elif user_type == "exit":
        print("Goodbye!")
        break
    else:
        print("Invalid input. Please enter teacher, student, or exit.")