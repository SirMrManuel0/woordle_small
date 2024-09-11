class WordleException(Exception):
    pass

class InvalidArgument(WordleException):
    def __init__(self, msg: str, argument_given, argument_expected) -> None:
        super().__init__(msg)
        self.argument_given = argument_given
        self.argument_expected = argument_expected


class IllegalState(WordleException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)