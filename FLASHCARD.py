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
                print("Loaded existing flashcards:", flashcards)  # Debug statement
            else:
                flashcards = []
                print("No existing flashcards found, creating new list.")  # Debug statement
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

clear_flashcards()

while True:
    teacher = input("Are you a teacher? (y/n): ").lower()

    if teacher == "y":
        action = input("What would you like to do? (add/clear/view flashcards): ").lower()
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
                    flashcards = json.load(file)
                    if not flashcards:
                        print("No flashcards found.")
                    else:
                        for card in flashcards:
                            print(f"{card['id']}: {card['topic']}: {card['phase']} - {card['answer']}")
            except FileNotFoundError:
                print("No flashcards found.")
    elif teacher == "n":
        streak = 0
        amountofcorrectAnswers = 0
        try:
            with open("flashcards.json", "r") as file:
                flashcards = json.load(file)
                if not flashcards:
                    print("No flashcards found.")
                else:
                    while True:
                        for card in flashcards:
                            print(f"{card['id']}: {card['topic']}: {card['phase']}")
                        flashcard_id = int(input("Enter the flashcard number you want to see (or 0 to exit): "))
                        if flashcard_id == 0:
                            break
                        for card in flashcards:
                            if card['id'] == flashcard_id:
                                print(f"Flashcard {flashcard_id} | {card['topic']}")
                                print(f"Phase: {card['phase']}")
                                while True:
                                    answerAttempt = input("Enter your answer: ")
                                    if answerAttempt == card['answer']:
                                        print("Correct!")
                                        streak += 1
                                        amountofcorrectAnswers += 1
                                        if streak > 0:
                                            print(f"Your streak is {streak}!")
                                        break
                                    else:
                                        print("Incorrect. Try again.")
                                        print(f"You lost your streak of {streak}!")
                                        streak = 0
                                break
                        else:
                            print(f"Flashcard {flashcard_id} not found.")
        except FileNotFoundError:
            print("No flashcards found.")