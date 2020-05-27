from wikidata.client import Client
from re import compile
from nltk.corpus import wordnet as wn
import pycountry


class DavarWord:
    """Informal abstract class for Words, like Rel and Node.
    """

    def __init__(self, id: str):
        """Initializes a Word from an identifier. This should only be used on 
        super().__init__.

        Parameters
        ----------
        id : str
            Word identifier
        """
        self._validate_id(id)
        self.id = id

    def _validate_id(self, id: str):
        """Informal abstract method for validating id on init. This method should be
        implemented by any subclass that will be initialized. When implemented, it
        should do nothing if the id is valid and throw a ValueError if the id is invalid
        .

        Parameters
        ----------
        id : str
            Word identifier
        Raises
        ------
        NotImplementedError
            This will always be raised if this method is called, as it is an abstract
            method.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """Returns representation of self"""
        return f'{type(self).__name__}("{self.id}")'

    def __str__(self) -> str:
        """Returns pretty printed representation of self"""
        return str(self.id)

    def __eq__(self, other) -> bool:
        """Returns True if equal, false if not."""
        return self.id == other.id

    def describe(self, lang: str, lvl: int = 0) -> str:
        """Informal abstract method. Should be implemented by any subclasses. When
        implemented, returns a human-readable description of the Word in a given 
        language depending on level of hierachy.

        Parameters
        ----------
        lang : str
            BCP 47 language tag
        lvl : int, optional
            Hierachy level of description in output text, by default 0

        Returns
        -------
        str
            Description of self

        Raises
        ------
        NotImplementedError
            Will always be raised if this method as called, as it is an abstract method.
        """
        raise NotImplementedError


class Node(DavarWord):
    """Informal abstract class for Nodes in davar, which represent nouns, ideas, or 
    entities. Is empty because all code is shared with Rel, and exists so that
    subclasses of Node and of Rel can be distinguished easily.
    """

    def __init__(self, id):
        super().__init__(id)


class Rel(DavarWord):
    """Informal abstract class for Rel in davar, which represent properties, verbs, or any 
    other type of relationship between Nodes. Is empty because all code is shared with 
    Node, and exists so that subclasses of Node and of Rel can be distinguished easily.
    """

    def __init__(self, id):
        super().__init__(id)


class WikidataItem(Node):
    """Class for Wikidata Items, a type of Node, which is itself a type of DavarWord.
    """

    _compiled_id_regex = compile(r"Q\d+")

    def __init__(self, id: str):
        """Constructs and initializes a WikidataItem from a valid Wikidata Property
        identifier.

        Parameters
        ----------
        id : str
            A valid Wikidata Item identifier in the form Q# where # is a natural number.
        """
        super().__init__(id)
        self.data = Client().get(id)

    @classmethod
    def _validate_id(cls, id: str):
        """Called at `__init__` to validate identifiers, which should be in the form
        `Q#` where `#` is a natural number. Does nothing if the identifier is valid, but
        throws a ValueError if it is invalid.

        Parameters
        ----------
        id : str
            Hopefully, a valid Wikidata Item identifier.

        Raises
        ------
        ValueError
            Thrown if `id` is not, in fact, a valid Wikidata Item identifier.
        """
        if cls._compiled_id_regex.fullmatch(id) == None:
            raise ValueError(f"{id} is not a valid Wikidata Item ID")

    def describe(self, lang: str, lvl: int = 0) -> str:
        """Returns the Wikidata Item label in a given language. Ignores hierarchy, as
        Wikidata Items are displayed the same regardless of hierarchy.

        Parameters
        ----------
        lang : str
            BCP 47 language tag
        lvl : int, optional
            Hierachy level of description in output text, by default 0

        Returns
        -------
        str
            Wikidata Item label in given language
        """
        return self.data.label[lang]


class WikidataProperty(Rel):
    """Class for Wikidata Properties, a type of Rel, which is itself a type of DavarWord.
    """

    _compiled_id_regex = compile(r"P\d+")

    def __init__(self, id: str):
        """Constructs and initializes a WikidataProperty from a valid Wikidata
        Property identifier.

        Parameters
        ----------
        id : str
            A valid Wikidata Property identifier in the form `P#` where `#` is a
            natural number.
        """
        super().__init__(id)
        self.data = Client().get(id)

    @classmethod
    def _validate_id(cls, id):
        """Called at `__init__` to validate identifiers, which should be in the form
        `P#` where `#` is a natural number. Does nothing if the identifier is valid, but
        throws a ValueError if it is invalid.

        Parameters
        ----------
        id : str
            Hopefully, a valid Wikidata Property identifier.

        Raises
        ------
        ValueError
            Thrown if `id` is not, in fact, a valid Wikidata Property identifier.
        """
        if cls._compiled_id_regex.fullmatch(id) == None:
            raise ValueError(f"{id} is not a valid Wikidata Property ID")

    def describe(self, lang: str, lvl: int = 0) -> str:
        """Returns the Wikidata Property label in a given language. Ignores hierarchy,
        as Wikidata Properties are displayed the same regardless of hierarchy.

        Parameters
        ----------
        lang : str
            BCP 47 language tag
        lvl : int, optional
            Hierachy level of description in output text, by default 0

        Returns
        -------
        str
            Wikidata Property label in given language
        """
        return self.data.label[lang]


class OMWSynset(Node, Rel):
    """A Synonym Set in the Open Multilingual Wordnet, representing a set of synonyms
    that represent the same idea across languages.
    """

    _compiled_id_regex = compile(r"\d{8}-[v|r|n|a]")

    def __init__(self, id: str):
        """Constructs a OMWSynset from an "identifier," more formally Part Of Speech and
        offset, in the form `OFFSET-POS` where `OFFSET` is an eight digit code and POS
        is a letter representing part of speech, either 'v,' 'r,' 'n,' or 'a.'

        Parameters
        ----------
        id : str
            Synset offset and POS.
        """
        super().__init__(id)

    @classmethod
    def _validate_id(cls, id):
        if cls._compiled_id_regex.fullmatch(id) == None:
            raise ValueError(
                f"{id} is not a valid Open Multilingual WordNet Synset offset and POS"
            )

    @staticmethod
    def _bcp_47_to_iso_639_2(lang_tag: str) -> str:
        """Utility function for getting a ISO 639-2 three letter language code from a 
        BCP 47 language tag.

        Parameters
        ----------
        lang_tag : str
            BCP 47 language tag/code.

        Returns
        -------
        str
            Roughly equivalent ISO 639-2 three letter language code.
        """

        if "-" in lang_tag:
            lang_tag = lang_tag[: lang_tag.find("-")]
        if len(lang_tag) == 3:
            # three letter lang tags are already in alpha_3 format
            return lang_tag
        else:
            return pycountry.languages.get(alpha_2=lang_tag).alpha_3

    def describe(self, lang: str, lvl: int = 0) -> str:
        """Returns the first listed lemma name for Synset in a given language. Ignores
        hierarchy as Synsets do not change display depending on hierarchy.

        Parameters
        ----------
        lang : str
            BCP 47 language tag
        lvl : int, optional
            Hierachy level of description in output text, by default 0

        Returns
        -------
        str
            First lemma name for Synset in a given language.
        """
        return wn.synset_from_pos_and_offset(
            self.id[-1], int(self.id[:-2])
        ).lemma_names(self._bcp_47_to_iso_639_2(lang))[0]


class Statement:
    """Most basic form of Statement (often refered to as a Singleton Statement)
    involving only a subject.
    """

    def __init__(self, sub):
        """Constructs a Singleton Statement from a subject.

        Parameters
        ----------
        sub : Node or Statement
            The subject of this statement
        """
        self.sub = sub

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__  # FIXME: messy, bad

    def __repr__(self):
        return f"Statement({repr(self.sub)})"

    def __str__(self):
        return f"({self.sub})"

    def describe(self, lang: str, lvl: int = 0) -> str:
        """Describes self in human readable format in a given language by calling
        `.describe()` on children and structuring results in a human readable format.
        Will return slightly different formatting to minimize confusion if lvl is
        greater than 0.

        Parameters
        ----------
        lang : str
            BCP 47 language tag
        lvl : int, optional
            The level of hierarchy in the text description, by default 0

        Returns
        -------
        str
            Description of self in given language.
        """
        sub_label = self.sub.describe(lang, lvl + 1)
        if lvl == 0:  # give fancy formatting if it is top level
            return f"{sub_label}."
        else:  # give utilitarian formatting if it is not
            return f"[{sub_label}]"


class Edge(Statement):
    """Statement defining an unlabeled relationship between a subject and an object.
    """

    def __init__(self, sub, ob):
        """Constructs an edge from the subject to the object.

        Parameters
        ----------
        sub : Node or Statement
            Subject / origin of Edge
        ob : Node or Statement
            Object / endpoint of Edge
        """
        self.ob = ob
        super().__init__(sub)

    def __repr__(self):
        return f"Edge({repr(self.sub)}, {repr(self.ob)})"

    def __str__(self):
        return f"({self.sub} {self.ob})"

    def describe(self, lang: str, lvl: int = 0) -> str:
        """Describes self in human readable format in a given language by calling
        `.describe()` on children and structuring results in a human readable format.
        Will return slightly different formatting to minimize confusion if lvl is
        greater than 0.

        Parameters
        ----------
        lang : str
            BCP 47 language tag
        lvl : int, optional
            The level of hierarchy in the text description, by default 0

        Returns
        -------
        str
            Description of self in given language.
        """
        sub_label = self.sub.describe(lang, lvl + 1)
        ob_label = self.ob.describe(lang, lvl + 1)
        if lvl == 0:  # give fancy formatting if it is top level
            return f"{sub_label} → {ob_label}."
        else:  # give utilitarian formatting if it is not
            return f"[{sub_label} → {ob_label}]"


class LabeledEdge(Edge):
    """Statement defining a labeled relationship from a subject to an object.
    """

    def __init__(self, rel: Rel, sub, ob):
        """Constructs a LabeledEdge from subject to object, labeled by a rel.

        Parameters
        ----------
        rel : Rel
            Relationship between subject and object
        sub : Node or Statement
            Subject / origin of LabeledEdge
        ob : Node or Statement
            Object / endpoint of LabeledEdge
        """
        self.rel = rel
        super().__init__(sub, ob)

    def __repr__(self):
        return f"LabeledEdge({repr(self.rel)}, {repr(self.sub)}, {repr(self.ob)})"

    def __str__(self):
        return f"({self.rel} {self.sub} {self.ob})"

    def describe(self, lang: str, lvl: int = 0) -> str:
        """Describes self in human readable format in a given language by calling
        `.describe()` on children and structuring results in a human readable format.
        Will return slightly different formatting to minimize confusion if lvl is
        greater than 0.

        Parameters
        ----------
        lang : str
            BCP 47 language tag
        lvl : int, optional
            The level of hierarchy in the text description, by default 0

        Returns
        -------
        str
            Description of self in given language.
        """
        rel_label = self.rel.describe(lang, lvl + 1)
        sub_label = self.sub.describe(lang, lvl + 1)
        ob_label = self.ob.describe(lang, lvl + 1)

        if lvl == 0:  # give fancy formatting if it is top level
            return f"{sub_label} → {ob_label} ({rel_label})."
        else:  # give utilitarian formatting if it is not
            return f"[{sub_label} → {ob_label} ({rel_label})]"


def _bcp_47_to_iso_639_2(lang_code: str) -> str:
    """For backwards compatibility with 0.2.0, mirrors staticmethod of OMWSynset's
    `._bcp_42_to_iso_639_2()` method

    Parameters
    ----------
    lang_code : str
        Language tag/code in BCP 47

    Returns
    -------
    str
        Language tag/code in ISO 639-2
    """
    return OMWSynset._bcp_47_to_iso_639_2(lang_code)
