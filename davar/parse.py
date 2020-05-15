from arpeggio import OneOrMore, EOF, ParserPython, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
import model

# define rules
# fmt: off
def numerical_id(): return _(r'\d+')

def q_id(): return "Q", numerical_id

def p_id(): return "P", numerical_id

def statement(): return "(", p_id, q_id, q_id, ")"

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

    def visit_statement(self, node, children):
        """
        Instantiates a Statement for each statement.
        """
        if self.debug:
            print(f"Instantiating Statement from {children}.")
        return model.Statement(*children)

    def visit_davartext(self, node, children):
        """
        Collects Statements into a List.
        """
        if self.debug:
            print(f"Collecting Statements {children} into List.")
        return list(children)


def parse(davartext: str, debug: bool = False) -> list:
    """
    Parses a text string in davartext into a list of Statements.
    """
    parser = ParserPython(davar, debug=debug)
    parse_tree = parser.parse(davartext)
    result = visit_parse_tree(parse_tree, DavarVisitor(debug=debug))
    return result
