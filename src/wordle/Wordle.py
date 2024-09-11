import os
import json
import string
import random

from src.wordle.WordleException import InvalidArgument, IllegalState

class Wordle:
    IS_AT_CORRECT_INDEX: int = 0
    IS_IN_WORD: int = 1
    NOT_IN_WORD: int = 2

    def __init__(self, path_wordlist: str) -> None:
        """
        This method initialises the Wordle-class and sets basic operations up.
        As input the path to the wordlist is needed. Make Sure that ALL words are of the length 5.
        throws: WordleException -> InvalidArgument
        :param path_wordlist:
        """

        # Argument Validation
        # Tests if the file exists
        if not os.path.isfile(path_wordlist):
            raise InvalidArgument("The given path is not a file!"
                                  , path_wordlist, "Path/to/your/json/wordlist")

        # Tests if the file is a JSON
        with open(path_wordlist, "r") as js:
            data: str = " ".join(js.readlines())
            try:
                data: list = json.loads(data)
            except ValueError as err:
                raise InvalidArgument("A JSON file was expected!",
                                      data, "['house', 'horse']")
        # Tests length of the words
        for word in data:
            if len(word) != 5:
                raise InvalidArgument("Every word has to be 5 letters long!",
                                    word, "house")

        # Tests if the letters are in the english alphabet
        for word in data:
            for letter in word:
                if letter.upper() not in string.ascii_uppercase:
                    raise InvalidArgument("All letters must be ascii characters!",
                                          letter, string.ascii_uppercase)

        # Prepare word list
        wordlist: list = []

        # Remove duplicates
        for word in data:
            if word not in wordlist:
                wordlist.append(word)

        # Set all words to uppercase
        for index, word in enumerate(wordlist):
            wordlist[index] = word.upper()

        # Set class variables
        self._words: list = wordlist
        self._words_path: str = path_wordlist
        self._current_wordle: str = ""
        self._tries: int = 6

    def _get_random_word(self) -> str:
        return random.choices(self._words)

    def _reset(self) -> None:
        self._current_wordle: str = ""
        self._tries: int = 6

    def try_word(self, word: str) -> dict[int, int]:
        # Tests Wordle-class State
        if len(self._current_wordle) != 5:
            raise IllegalState("Create a new Wordle first!")
        if self._tries <= 0:
            raise IllegalState("No tries left!")

        # Reduce tries
        self._tries -= 1

        answer: dict = {i: Wordle.NOT_IN_WORD for i in range(len(word))}

        # Check word
        for index, letter in enumerate(word):
            if word[index] == self._current_wordle[index]:
                answer[index] = Wordle.IS_AT_CORRECT_INDEX
            elif letter in self._current_wordle:
                answer[index] = Wordle.IS_IN_WORD

        return answer

    def new_wordle(self) -> None:
        self._reset()
        self._current_wordle: str = self._get_random_word()

    def __str__(self) -> str:  # Method that is called, if e.g. print(Wordle(path)) is used
        return f"Wordlist Path: {self._words_path}\nWords: {self._words}\nWord Count: {len(self._words)}"
