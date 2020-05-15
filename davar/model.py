from qwikidata.entity import WikidataItem, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api as get_dict

class Node(object):
    #A noun, item, entity, etc. Right now is simply a container for Wikidata entity IDs.
    def __init__(self, id: int):
        self.id = id
        self.data = get_dict(f"Q{id}")
    def __repr__(self):
        return f"Node({self.id})"
    def __str__(self):
        return f"Q{self.id}"
    def get_label(self, lang: str) -> str:
        """
        Finds the label of a WikiData item given a two letter language code.
        """
        return self.data["labels"][lang]["value"]

class Rel(object):
    #A relationship between nodes. Right now is simply a container for Wikidata property IDs.
    def __init__(self, id: int):
        self.id = id
        self.data = get_dict(f"P{id}")
    def __repr__(self):
        return f"Rel({self.id})"
    def __str__(self):
        return f"P{self.id}"
    def get_label(self, lang: str) -> str:
        """
        Finds the label of a WikiData item given a two letter language code.
        """
        return self.data["labels"][lang]["value"]

class Statement(object):
    #Defines a rel between two nodes, (i.e. a relationship between two entities) starting at node 1 and ending at node 2.
    def __init__(self, rel: Rel, node1: Node, node2: Node):
        self.rel = rel
        self.node1 = node1
        self.node2 = node2
    def __repr__(self):
        return f"Statement({repr(self.rel)}, {repr(self.node1)}, {repr(self.node2)})"
    def __str__(self):
        return f"({self.rel} {self.node1} {self.node2})"
    def describe(self, lang:str) -> str:
        """
        Translates / describes self in language as given in two character language code form in `lang`
        """
        rel_label = self.rel.get_label(lang)
        node1_label = self.node1.get_label(lang)
        node2_label = self.node2.get_label(lang)
        return f"{node1_label} -> {node2_label} ({rel_label})"




