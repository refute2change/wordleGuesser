import loaddata
from tqdm import tqdm
import json

words = loaddata.load_data()

def get_word_appearance(word: str, candidate: str) -> tuple[int]:
    result = [0] * len(word)
    letter_count = {}
    unchecked = {}
    for i in range(len(word)):
        if word[i] == candidate[i]:
            result[i] = 1
            if word[i] not in letter_count:
                letter_count[word[i]] = 1
            else:
                letter_count[word[i]] += 1
        elif word[i] in candidate:
            if word[i] not in unchecked:
                unchecked[word[i]] = 1
            else:
                unchecked[word[i]] += 1
        else:
            result[i] = -1
    for i in range(len(word)):
        if result[i] == 0:
            if unchecked[word[i]] == 0:
                result[i] = -1
                continue
            criteria = (letter_count[word[i]] if word[i] in letter_count else 0)
            if criteria < candidate.count(word[i]):
                unchecked[word[i]] -= 1
                if word[i] in letter_count:
                    letter_count[word[i]] += 1
                else:
                    letter_count[word[i]] = 1
            else:
                result[i] = -1
    return tuple(result)

def get_word_appearance_count(word: str, candidates: list[str]) -> int:
    available = {}
    for i in candidates:
        result = get_word_appearance(word, i)
        if result not in available:
            available[result] = 1
        else:
            available[result] += 1
    return available

json_obj = {}
output_file = open("output.json", "w")

for k in tqdm(range(len(words))):
    i = words[k]
    json_obj[i] = get_word_appearance_count(i, words)

print(json_obj)
output_file.close()