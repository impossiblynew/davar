from wikidata.client import Client


class Node:
    # A noun, item, entity, etc. Right now is simply a container for Wikidata entity IDs.
    def __init__(self, id: int):
        self.id = id
        self.data = Client().get(f"Q{id}")

    def __repr__(self):
        return f"Node({self.id})"

    def __str__(self):
        return f"Q{self.id}"

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def describe(self, lang: str, lvl: int = 0) -> str:
        """
        Finds the label of a WikiData item given a two letter language code.
        """
        return self.data.label[lang]


class Rel:
    # A relationship between nodes. Right now is simply a container for Wikidata property IDs.
    def __init__(self, id: int):
        self.id = id
        self.data = Client().get(f"P{id}")

    def __repr__(self):
        return f"Rel({self.id})"

    def __str__(self):
        return f"P{self.id}"

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def describe(self, lang: str, lvl: int = 0) -> str:
        """
        Finds the label of a WikiData item given a two letter language code.
        """
        return self.data.label[lang]  # returns same regardless of level


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
        Translates / describes self in language as given in two character language code form in `lang`
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
        Translates / describes self in language as given in two character language code form in `lang`
        """
        sub_label = self.sub.describe(lang, lvl + 1)
        ob_label = self.ob.describe(lang, lvl + 1)
        if lvl == 0:  # give fancy formatting if it is top level
            return f"{sub_label} → {ob_label}."
        else:  # give utilitarian formatting if it is not
            return f"[{sub_label} → {ob_label}]"


class LabeledEdge(Edge):
    """
    Defines a relationship between a subject Node and an object Node which is labeled with a Rel.
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
        Translates / describes self in language as given in two character language code form in `lang`
        """
        rel_label = self.rel.describe(lang, lvl + 1)
        sub_label = self.sub.describe(lang, lvl + 1)
        ob_label = self.ob.describe(lang, lvl + 1)

        if lvl == 0:  # give fancy formatting if it is top level
            return f"{sub_label} → {ob_label} ({rel_label})."
        else:  # give utilitarian formatting if it is not
            return f"[{sub_label} → {ob_label} ({rel_label})]"
