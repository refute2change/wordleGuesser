import loaddata
from tqdm import tqdm
import json
from collections import Counter
import math

words = loaddata.load_data()
idlist = None
with open("words.json", "r") as f:
    idlist = json.load(f)

freqs = {}
for word in words:
    freqs[word] = Counter(word)
results = {}
with open("newprecompute.json", "r") as f:
    results = json.load(f)

def get_word_appearance(word: str, candidate: str) -> str:
    result = ['m'] * len(word)
    freq = freqs[candidate].copy()
    unchecked = []
    # First pass: Check for exact matches
    for i, (w, c) in enumerate(zip(word, candidate)):
        if w == c:
            result[i] = 'c'
            freq[w] -= 1
        elif w not in candidate:
            result[i] = 'w'
        else:
            unchecked.append(i)
    if len(unchecked) == 0:
        return "".join(result)

    # Second pass: Check for misplaced matches
    for i in unchecked:
        w = word[i]
        if freq.get(w, 0) > 0:
            freq[w] -= 1
        else:
            result[i] = 'w'

    return "".join(result)

def encode_verdict(verdict: str) -> int:
    score = 0
    for i in range(len(verdict)):
        c = verdict[-(i + 1)]
        if c == 'c':
            score += 2 * (3 ** i)
        elif c == 'm':
            score += 3 ** i
    return score

def decode_verdict(score: int, length: int) -> str:
    verdict = ['w'] * length
    for i in range(length):
        j = score % 3
        if j == 0:
            verdict[-(i + 1)] = 'w'
        elif j == 1:
            verdict[-(i + 1)] = 'm'
        elif j == 2:
            verdict[-(i + 1)] = 'c'
        score = score // 3
    return "".join(verdict)

def precompute():
    for word in tqdm(words):
        results[idlist[word]] = [0] * len(words)
        for candidate in words:
            results[idlist[word]][idlist[candidate]] = encode_verdict(get_word_appearance(word, candidate))
    with open("newprecompute.json", "w") as f:
        json.dump(results, f)

def get_entropy(word: str, candidates: list[str]) -> float:
    i = Counter(results[str(idlist[word])][idlist[candidate]] for candidate in candidates)
    s = 0 + sum(i[j]/len(candidates) * math.log(len(candidates)/i[j], 2) for j in i)
    return s

def get_prediction(guess: str, answer: str) -> str:
    return decode_verdict(results[str(idlist[guess])][idlist[answer]], len(guess))
