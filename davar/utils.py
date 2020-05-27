from davar.parsing import transcribe


class Davar:
    """Represents a set of statements in davar.
    """

    def __init__(self, statements: list):
        """Constructs a Davar object from a list of davar Statements.

        Parameters
        ----------
        statements : list
            A list of davar Statements
        """
        self.statements = statements

    @classmethod
    def from_davartext(cls, davartext: str):
        """Constructs a Davar object from a string of text written in davar.

        Parameters
        ----------
        davartext : str
            A string of text written in davar

        Returns
        -------
        Davar
            A Davar object
        """
        return cls(transcribe(davartext))

    def describe(self, lang: str) -> list:
        """Returns a list of strings describing its Statements in a human readable
        format in a given language.

        Parameters
        ----------
        lang : str
            BCP 47 language tag

        Returns
        -------
        list
            List of strings describing Statements in a human readable format
        """
        return [s.describe(lang) for s in self.statements]
