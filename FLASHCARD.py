import json

class Flashcard:
    def __init__(self, phase, answer):
        self.phase = phase
        self.answer = answer

    def __str__(self):
        return f"{self.phase}: {self.answer}"

    def to_dict(self):
        return {"phase": self.phase, "answer": self.answer}


def save_flashcard(flashcard, filename="flashcards.json"):
    try:
        with open(filename, "r") as file:
            flashcards = json.load(file)
    except FileNotFoundError:
        flashcards = []

    flashcards.append(flashcard.to_dict())

    with open(filename, "w") as file:
        json.dump(flashcards, file, indent=4)


while True:
    teacher = input("Are you a teacher? (y/n): ").lower()

    if teacher == "y":
        phase = input("Enter the phase: ")
        answer = input("Enter the answer: ")
        flashcard = Flashcard(phase, answer)
        save_flashcard(flashcard)
    elif teacher == "n":
        try:
            with open("flashcards.json", "r") as file:
                flashcards = json.load(file)
                for card in flashcards:
                    print(f"{card['phase']}: {card['answer']}")
        except FileNotFoundError:
            print("No flashcards found.")