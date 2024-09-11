import os
import json
import time

from LogManagerException import InvalidArgument, CorruptedLog

class LogManager:
    def __init__(self, log_path: str):
        # Argument Validation
        # Tests if the path is valid
        if not os.path.isfile(log_path):
            raise InvalidArgument("The given path is invalid! Please provide the correct path to the JSON!",
                                  log_path, "path/to/the/log/JSON.json")

        # Tests if the file is a json
        try:
            with open(log_path, "r") as js:
                data: str = " ".join(js.readlines())
                data: dict = json.loads(data)
                del data
        except ValueError:
            raise InvalidArgument("The given path does not lead to a JSON!",
                                  log_path, "path/to/the/log/JSON.json")

        # Validates the log file
        with open(log_path, "r") as js:
            log: dict = json.load(js)
        try:
            entry_count: int = int(log["count"])
            log['count'] = int(log['count'])
        except KeyError:
            raise CorruptedLog("Are you sure this is a valid log file?")
        except ValueError:
            raise CorruptedLog("log count must be an integer!")

        if entry_count != len(list(log.keys())):
            raise CorruptedLog("The given log file is invalid! Please, make sure it is a correct file!")

        # Set the self variables
        self._log_path: str = log_path
        self._log_count: int = entry_count

    def get(self, amount: int = 1) -> tuple:
        """
        Returns the last n amount of logs. Default value is 1.
        :param amount:
        :return:
        """
        if amount <= 0:
            raise InvalidArgument("The amount needs to be 1 or more!", amount, 1)
        if amount > self._log_count:
            raise InvalidArgument("The given amount is bigger than the amount of logs."
                                  + " If this is on purpose, please use get_promise!", amount, 1)

        with open(self._log_path, "r") as js:
            logs: dict = json.load(js)
        result_logs: list = []
        for i in range(amount):
            result_logs.append(logs['logs'][len(logs['logs']) - 1 - i])
        return tuple(result_logs)

    def get_promise(self, amount: int = 3) -> tuple:
        """
        This method works like get, but it allows you to enter an amount higher than the amount of logs.
        :param amount:
        :return:
        """
        if amount <= 0:
            raise InvalidArgument("The amount needs to be 1 or more!", amount, 1)

        with open(self._log_path, "r") as js:
            logs: dict = json.load(js)
        if amount <= self._log_count:
            return self.get(amount)

        amount: int = self._log_count
        return self.get(amount)

    def write(self, word: str) -> None:
        with open(self._log_path, "r") as js:
            logs: dict = json.load(js)
        logs['count'] += 1
        logs['logs'].append(word)
        self._log_count += 1
        with open(self._log_path, "w") as js:
            json.dump(logs, js)
