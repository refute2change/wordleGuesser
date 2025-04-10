import loaddata
import json

words = loaddata.load_data()
idlist = {words[i]: i for i in range(len(words))}

with open("words.json", "w") as f:
    json.dump(idlist, f, indent=4)