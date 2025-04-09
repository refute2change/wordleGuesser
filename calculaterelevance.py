import loaddata
from tqdm import tqdm
import json

words = loaddata.load_data()

def get_word_appearance(word: str, candidate: str) -> tuple[int]:
    result = [0] * len(word)
    letter_count = {}
    unchecked = {}

    # First pass: Check for exact matches
    for i, (w, c) in enumerate(zip(word, candidate)):
        if w == c:
            result[i] = 1
            letter_count[w] = letter_count.get(w, 0) + 1
        elif w in candidate:
            unchecked[w] = unchecked.get(w, 0) + 1
        else:
            result[i] = -1

    # Second pass: Check for misplaced matches
    for i, w in enumerate(word):
        if result[i] == 0:
            if unchecked.get(w, 0) > 0:
                criteria = letter_count.get(w, 0)
                if criteria < candidate.count(w):
                    unchecked[w] -= 1
                    letter_count[w] = letter_count.get(w, 0) + 1
                else:
                    result[i] = -1
            else:
                result[i] = -1

    return tuple(result)

def get_word_appearance_count(word: str, candidates: list[str]) -> dict[tuple[int], int]:
    appearance_count = {}
    for candidate in candidates:
        result = get_word_appearance(word, candidate)
        appearance_count[result] = appearance_count.get(result, 0) + 1
    return appearance_count

json_obj = {}
output_file = open("output.json", "w")

for k in tqdm(range(len(words))):
    i = words[k]
    json_obj[i] = get_word_appearance_count(i, words)

json.dump(json_obj, output_file, indent=4)
output_file.close()