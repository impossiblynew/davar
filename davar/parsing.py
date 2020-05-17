from arpeggio import OneOrMore, EOF, ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from davar import model

# define rules
# fmt: off
def _numerical_id(): return _(r'\d+')

def _q_id(): return "Q", _numerical_id

def _p_id(): return "P", _numerical_id

def _statement(): return "(", _p_id, _q_id, _q_id, ")"

def _davar(): return OneOrMore(_statement), EOF
# fmt: on

# visitor class
class _DavarVisitor(PTNodeVisitor):
    def visit__numerical_id(self, node, children):
        """
        Converts numerical_id value to int.
        """
        if self.debug:
            print(f"Converting {node.value}.")
        return int(node.value)

    def visit__q_id(self, node, children):
        """
        Instantiates a Node for each q_id.
        """
        if self.debug:
            print(f"Instantiating Node from {children}.")
        return model.Node(children[0])

    def visit__p_id(self, node, children):
        """
        Instantiates a Rel for each p_id.
        """
        if self.debug:
            print(f"Instantiating Rel from {children}.")
        return model.Rel(children[0])

    def visit__statement(self, node, children):
        """
        Instantiates a Statement for each statement.
        """
        if self.debug:
            print(f"Instantiating Statement from {children}.")
        return model.LabeledEdge(*children)

    def visit__davar(self, node, children):
        """
        Collects Statements into a List.
        """
        if self.debug:
            print(f"Collecting Statements {children} into List.")
        return list(children)


def _parse(davartext: str, debug: bool = False):
    parser = ParserPython(_davar, debug=debug)
    return parser.parse(davartext)


def _visit(davartree, debug: bool = False) -> list:
    return visit_parse_tree(davartree, _DavarVisitor(debug=debug))


def transcribe(davartext: str, debug: bool = False) -> list:
    """
    Parses a text string in davartext into a list of Statements.
    """
    parse_tree = _parse(davartext, debug=debug)
    result = _visit(parse_tree, debug=debug)
    return result
