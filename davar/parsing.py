from arpeggio import OneOrMore, EOF, ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from davar import model

# define rules
# fmt: off
def numerical_id(): return _(r'\d+')

def q_id(): return "Q", numerical_id

def p_id(): return "P", numerical_id

def node(): return [q_id, statement]

def edge(): return "(", node, node, ")"

def labelededge(): return "(", p_id, node, node, ")"

def singletonstatement(): return "(", node, ")"

def statement(): return [edge, labelededge, singletonstatement]

def davar(): return OneOrMore(statement), EOF
# fmt: on

# visitor class
class DavarVisitor(PTNodeVisitor):
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
        return model.Node(children[0])

    def visit_p_id(self, node, children):
        """
        Instantiates a Rel for each p_id.
        """
        if self.debug:
            print(f"Instantiating Rel from {children}.")
        return model.Rel(children[0])

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


def parse(davartext: str, debug: bool = False):
    parser = ParserPython(davar, debug=debug)
    return parser.parse(davartext)


def visit(davartree, debug: bool = False) -> list:
    return visit_parse_tree(davartree, DavarVisitor(debug=debug))


def transcribe(davartext: str, debug: bool = False) -> list:
    """
    Parses a text string in davartext into a list of Statements.
    """
    parse_tree = parse(davartext, debug=debug)
    result = visit(parse_tree, debug=debug)
    return result
