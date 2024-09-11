import json

with open("../res/raw_words", "r") as f:
    words: list = f.readlines()
words: list = [word[:-1] for word in words if len(word) > 0]
final: list = []
for word in words:
    if len(word) == 5:
        final.append(word)
with open("../res/words.json", "w") as js:
    json.dump(final, js, indent=2)