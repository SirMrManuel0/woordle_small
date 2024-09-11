
class LogManagerException(Exception):
    pass

class InvalidArgument(LogManagerException):
    def __init__(self, msg: str, argument_given, argument_expected) -> None:
        super().__init__(msg)
        self.argument_given = argument_given
        self.argument_expected = argument_expected

class CorruptedLog(LogManagerException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
