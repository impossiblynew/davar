from davar.parsing import transcribe
from davar.model import Statement


class Davar:
    """
    A class for holding davar statements, acting as the analog for some amount of
    davartext.
    """

    def __init__(self, statements: list):
        self.statements = statements

    @classmethod
    def from_davartext(cls, davartext: str):
        return cls(transcribe(davartext))

    def describe(self, lang: str) -> list:
        return [s.describe(lang) for s in self.statements]
