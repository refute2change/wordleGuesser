import loaddata
from tqdm import tqdm
import json
from collections import Counter
import time

words = loaddata.load_data()

freqs = {}
for word in words:
    freqs[word] = Counter(word)

def get_word_appearance(word: str, candidate: str) -> str:
    result = ['m'] * len(word)
    freq = freqs[candidate]
    unchecked = []
    # First pass: Check for exact matches
    for i, (w, c) in enumerate(zip(word, candidate)):
        if w == c:
            result[i] = 'c'
            freq[w] -= 1
        elif freq.get(w, 0) == 0:
            result[i] = 'w'
        else:
            unchecked.append(i)
    if len(unchecked) == 0:
        return "".join(result)

    # Second pass: Check for misplaced matches
    for i in unchecked:
        w = word[i]
        result[i] = 'w' if freq.get(w, 0) <= 0 else 'm'
        freq[w] -= 1

    return "".join(result)

def get_word_appearance_count(word: str, candidates: list[str]) -> dict[str, int]:
    appearance_count = {}
    for candidate in candidates:
        result = get_word_appearance(word, candidate)
        appearance_count[result] = appearance_count.get(result, 0) + 1
    return appearance_count

t = time.process_time()
print(get_word_appearance_count("apple", words))
print(time.process_time() - t)

# json_obj = {}
# output_file = open("output.json", "w")

# for k in tqdm(range(len(words))):
#     i = words[k]
#     json_obj[i] = get_word_appearance_count(i, words)

# output_file.close()