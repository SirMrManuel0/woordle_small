import json

with open("../res/raw_words", "r") as f:
    words: list = f.readlines()
words: list = [word[:-1] for word in words if len(word) > 0]
with open("../res/words.json", "w") as js:
    json.dump(words, js, indent=2)