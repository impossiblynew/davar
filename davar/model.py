from wikidata.client import Client
from re import compile
from nltk.corpus import wordnet as wn
import pycountry


class DavarWord:
    """
    Informal abstract class for Nodes and Rels. Implements some methods but will throw a 
    NotImplementedError if .describe() is used.
    """

    def __init__(self, id: str):
        self._validate_id(id)
        self.id = id

    def _validate_id(self, id):  # Not sure if this should be a static or class method
        """
        Informal abstract method for validating id at init. Raises error if the id
        is not valid.
        """
        raise NotImplementedError

    def __repr__(self):
        return f'{type(self).__name__}("{self.id}")'

    def __str__(self):
        return self.id

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def describe(self, lang: str, lvl: int = 0) -> str:
        """
        Informal abstract method. This should describe itself in the given language,
        modulating output according to lvl.
        """
        raise NotImplementedError


class Node(DavarWord):
    """
    Empty class for Nodes.
    Nodes and Rels share a lot of code. This class exists so that subclasses of Node and
    subclasses of Rel can be distinguished.
    """

    def __init__(self, id):
        super().__init__(id)


class Rel(DavarWord):
    """
    Empty class for Nodes.
    Nodes and Rels share a lot of code. This class exists so that subclasses of Node and
    subclasses of Rel can be distinguished.
    """

    def __init__(self, id):
        super().__init__(id)


class WikidataItem(Node):
    """
    Class for WikidataItems, a kind of node. Initialize with a string giving the
    Wikidata Item Identifier. Calling describe will give the label in the requested
    language.
    """

    _compiled_id_regex = compile(r"Q\d+")

    def __init__(self, id: str):
        super().__init__(id)
        self.data = Client().get(id)

    @classmethod
    def _validate_id(cls, id: str):
        if cls._compiled_id_regex.fullmatch(id) == None:
            raise ValueError(f"{id} is not a valid Wikidata Item ID")

    def describe(self, lang: str, lvl: int = 0) -> str:
        """
        Finds the label of a WikiData item given a two letter language code.
        """
        return self.data.label[lang]


class WikidataProperty(Rel):
    """
    A relationship between nodes. Right now is simply a container for Wikidata property
    IDs.
    """

    _compiled_id_regex = compile(r"P\d+")

    def __init__(self, id: str):
        super().__init__(id)
        self.data = Client().get(id)

    @classmethod
    def _validate_id(cls, id):
        if cls._compiled_id_regex.fullmatch(id) == None:
            raise ValueError(f"{id} is not a valid Wikidata Property ID")

    def describe(self, lang: str, lvl: int = 0) -> str:
        """
        Finds the label of a WikiData item given a two letter language code.
        """
        return self.data.label[lang]  # returns same regardless of level


class OMWSynset(Node, Rel):
    """
    A synset from the open multilingual wordnet.
    """

    _compiled_id_regex = compile(r"\d{8}-[v|r|n|a]")

    def __init__(self, id: str):
        super().__init__(id)

    @classmethod
    def _validate_id(cls, id):
        if cls._compiled_id_regex.fullmatch(id) == None:
            raise ValueError(
                f"{id} is not a valid Open Multilingual WordNet synset offset"
            )

    @staticmethod
    def _bcp_47_to_iso_639_2(lang_tag: str) -> str:
        """Utility function for turning BCP 47 language tags into ISO 639-2 language
        tags.

        Arguments:
            lang_tag {str} -- Langauge tag/code in BCP 47

        Returns:
            str -- Rougly corresponding language code in ISO 639-2
        """

        if "-" in lang_tag:
            lang_tag = lang_tag[: lang_tag.find("-")]
        if len(lang_tag) == 3:
            # three letter lang tags are already in alpha_3 format
            return lang_tag
        else:
            return pycountry.languages.get(alpha_2=lang_tag).alpha_3

    def describe(
        self, lang: str, lvl: int = 0
    ) -> str:  # FIXME: It is impossible to use this together with Wikidata items because they use a different language scheme.
        """
        Gives the lemma (name) of a Open Multilingual Wordnet synset in a language given in a 3 letter code 
        """
        return wn.synset_from_pos_and_offset(
            self.id[-1], int(self.id[:-2])
        ).lemma_names(self._bcp_47_to_iso_639_2(lang))[0]


class Statement:
    """
    Most basic possible statement, which involves only a subject.
    """

    def __init__(self, sub):
        self.sub = sub

    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__  # FIXME: messy, bad

    def __repr__(self):
        return f"Statement({repr(self.sub)})"

    def __str__(self):
        return f"({self.sub})"

    def describe(self, lang: str, lvl: int = 0) -> str:
        """
        Translates / describes self in language as given in two character language code
        form in `lang`
        """
        sub_label = self.sub.describe(lang, lvl + 1)
        if lvl == 0:  # give fancy formatting if it is top level
            return f"{sub_label}."
        else:  # give utilitarian formatting if it is not
            return f"[{sub_label}]"


class Edge(Statement):
    """
    Defines a relation between a subject and an object.
    """

    def __init__(self, sub, ob):
        self.ob = ob
        super().__init__(sub)

    def __repr__(self):
        return f"Edge({repr(self.sub)}, {repr(self.ob)})"

    def __str__(self):
        return f"({self.sub} {self.ob})"

    def describe(self, lang: str, lvl: int = 0) -> str:
        """
        Translates / describes self in language as given in two character language code
        form in `lang`
        """
        sub_label = self.sub.describe(lang, lvl + 1)
        ob_label = self.ob.describe(lang, lvl + 1)
        if lvl == 0:  # give fancy formatting if it is top level
            return f"{sub_label} → {ob_label}."
        else:  # give utilitarian formatting if it is not
            return f"[{sub_label} → {ob_label}]"


class LabeledEdge(Edge):
    """
    Defines a relationship between a subject Node and an object Node which is labeled
    with a Rel.
    """

    def __init__(self, rel: Rel, sub, ob):
        self.rel = rel
        super().__init__(sub, ob)

    def __repr__(self):
        return f"LabeledEdge({repr(self.rel)}, {repr(self.sub)}, {repr(self.ob)})"

    def __str__(self):
        return f"({self.rel} {self.sub} {self.ob})"

    def describe(self, lang: str, lvl: int = 0) -> str:
        """
        Translates / describes self in language as given in two character language code
        form in `lang`
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
    ._bcp_42_to_iso_639_2() method

    Arguments:
        lang_code {str} -- Lang tag/code in BCP 47

    Returns:
        str -- Lang tag/code in ISO 639-2
    """
    return OMWSynset._bcp_47_to_iso_639_2(lang_code)
