import loaddata
from tqdm import tqdm
import json
from calculaterelevance import get_prediction, get_entropy

class bot:
    candidates: list[str]

    def __init__(self):
        self.candidates = loaddata.load_data()
        with open("precompute.json", "r") as f:
            score = json.load(f)
        with open("output.json", "w") as f:
            json.dump(score, f, indent=4)
    
    def get_guess(self):
        with open("output.json", "r") as f:
            score = json.load(f)
            return list(score.keys())[0]

    def narrow_down(self, guess: str, result: str):
        f = open("log_file.txt", "w")
        f.write(f"guess: {guess}, result: {result}\n")
        new_candidates = []
        for candidate in self.candidates:
            i = get_prediction(guess, candidate)
            if i == result:
                new_candidates.append(candidate)
        self.candidates = new_candidates
        print(len(self.candidates))
        score = {}
        for word in tqdm(self.candidates):
            score[word] = get_entropy(word, self.candidates)
        score = dict(sorted(score.items(), key=lambda item: item[1], reverse=True))
        json.dump(score, open("output.json", "w"), indent=4)