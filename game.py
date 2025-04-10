import random
from collections import Counter
from bot import bot
from calculaterelevance import get_prediction

class game:
    answer: str
    guesses: list[str] = []
    results: list[str] = []

    def __init__(self, length: int = 5, index: int = -1):
        if length < 3:
            raise ValueError("Length must be at least 3")
        else:
            file = open("answers/" + str(length) + "letters.txt", "r")
            words = file.read().splitlines()
            n = random.randint(0, len(words) - 1)
            self.answer = words[n]

    def show_answer(self):
        return self.answer
    
    def guess(self, guess: str):
        if len(self.guesses) == 6:
            return
        if len(guess) != len(self.answer):
            print("Invalid guess length")
            return
        result = get_prediction(guess, self.answer)
        self.guesses.append(guess)
        self.results.append(result)
        return result

g = game(5)
b = bot()
print(g.answer)
for i in range(6):
    guess = b.get_guess()
    result = g.guess(guess)
    print(g.answer in b.candidates)
    b.narrow_down(guess, result)
    print(f"Guess: {guess}, Result: {result}")
    if result == 'c' * len(guess):
        print("You win!")
        break
    input()

