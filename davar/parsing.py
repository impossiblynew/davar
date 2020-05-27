import arpeggio
from arpeggio import OneOrMore, EOF, ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from davar import model

# define rules
# fmt: off
# The below "functions" are actually all arpeggio grammar rules and aren't meant to be
# used as normal functions.
def numerical_id(): return _(r'\d+')

def q_id(): return "Q", numerical_id

def p_id(): return "P", numerical_id

def synset(): return _(r'\d{8}\-[v|r|n|a]')

def node(): return [q_id, statement, synset]

def rel(): return [p_id, synset]

def edge(): return "(", node, node, ")"

def labelededge(): return "(", rel, node, node, ")"

def singletonstatement(): return "(", node, ")"

def statement(): return [edge, labelededge, singletonstatement]

def davar(): return OneOrMore(statement), EOF
# fmt: on

# visitor class
class DavarVisitor(PTNodeVisitor):
    """Visits each node of a graph of a davar text and turns it into a list of davar
    Statements.
    """

    def visit_numerical_id(self, node, children):
        """
        Converts numerical_id value to int.
        """
        if self.debug:
            print(f"Converting {node.value}.")
        return int(node.value)

    def visit_q_id(self, node, children):
        """
        Instantiates a Node for each q_id.
        """
        if self.debug:
            print(f"Instantiating Node from {children}.")
        return model.WikidataItem(f"Q{children[0]}")

    def visit_p_id(self, node, children):
        """
        Instantiates a WikidataProperty for each p_id.
        """
        if self.debug:
            print(f"Instantiating WikidataProperty from {children}.")
        return model.WikidataProperty(f"P{children[0]}")

    def visit_synset(self, node, children):
        """
        Instantiates a OMWSynset for each synset
        """
        if self.debug:
            print(f"Instantiating OMWSynset from {node.value}.")
        return model.OMWSynset(node.value)

    def visit_edge(self, node, children):
        """
        Instantiates a Edge for a statement with two q_ids.
        """
        if self.debug:
            print(f"Instantiating an Edge from {children}.")
        return model.Edge(*children)

    def visit_labelededge(self, node, children):
        """
        Instantiates a LabeledEdge for a statement of (p_id q_id q_id)
        """
        if self.debug:
            print(f"Instantiating a LabeledEdge from {children}.")
        return model.LabeledEdge(*children)

    def visit_singletonstatement(self, node, children):
        """
        Instantiates a singleton statement from a statement in the form (q_id)
        """
        if self.debug:
            print(f"Instantiating a Statement from {children}.")
        return model.Statement(*children)

    def visit_statement(self, node, children):
        """
        Passes on its (hopefully only) child to the next node. 
        """
        if self.debug:
            print(f"Passing first item of {children}.")
        return children[0]

    def visit_davar(self, node, children):
        """
        Collects Statements into a List.
        """
        if self.debug:
            print(f"Collecting Statements {children} into List.")
        return list(children)


def parse(davartext: str, debug: bool = False) -> arpeggio.NonTerminal:
    """Parses a text string in davar into a list of davar Statements

    Parameters
    ----------
    davartext : str
        A text string written in davar
    debug : bool, optional
        If true, prints debug statements as davartext is parsed and places .dot files
        representing said process into the project directory, by default False

    Returns
    -------
    arpeggio.NonTerminal
        Parse tree representing the entered text.
    """
    parser = ParserPython(davar, debug=debug)
    return parser.parse(davartext)


def visit(davartree, debug: bool = False) -> list:
    """Visits a davar parse tree and transforms it into a list of davar statements.

    Parameters
    ----------
    davartree : arpeggio.NonTerminal
        Davar parse tree
    debug : bool, optional
        If true, prints debug statements as davartree is transformed and places .dot
        files representing said process into the project directory, by default False

    Returns
    -------
    list
        List of davar Statements
    """
    return visit_parse_tree(davartree, DavarVisitor(debug=debug))


def transcribe(davartext: str, debug: bool = False) -> list:
    """Transcribes a string of text in davar into a list of davar Statements

    Parameters
    ----------
    davartext : str
        A string of text in
    debug : bool, optional
        If true, prints debug statements as davartext is transcribed and places .dot
        files representing process into project directory, by default False

    Returns
    -------
    list
        List of davar Statements
    """
    parse_tree = parse(davartext, debug=debug)
    result = visit(parse_tree, debug=debug)
    return result
