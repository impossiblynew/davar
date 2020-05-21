from davar import model
import pytest


@pytest.fixture(scope="module")
def cached_node_Q42():
    """
    Contains a cached copy of model.Node("Q42")
    """
    return model.Node("Q42")


@pytest.fixture(scope="module")
def cached_node_Q5():
    """
    Contains a cached copy of model.Node("Q5")
    """
    return model.Node("Q5")


@pytest.fixture(scope="module")
def cached_rel_P31():
    """
    Contains a cached copy of model.Rel("P5")
    """
    return model.Rel("P31")


@pytest.fixture(scope="module")
def example_statement(cached_rel_P31, cached_node_Q42, cached_node_Q5):
    # this is not used in tests that are of ability to construct a statement, only where that is the set up, like nesting tests.
    return model.LabeledEdge(cached_rel_P31, cached_node_Q42, cached_node_Q5)


class TestNode:
    def test_describe(self, cached_node_Q42):
        assert cached_node_Q42.describe("en") == "Douglas Adams"

    def test_repr(self, cached_node_Q42):
        assert repr(cached_node_Q42) == 'Node("Q42")'

    def test_str(self, cached_node_Q42):
        assert str(cached_node_Q42) == "Q42"


class TestRel:
    def test_describe(self, cached_rel_P31):
        assert cached_rel_P31.describe("en") == "instance of"

    def test_repr(self, cached_rel_P31):
        assert repr(cached_rel_P31) == 'Rel("P31")'

    def test_str(self, cached_rel_P31):
        assert str(cached_rel_P31) == "P31"


class TestStatement:
    def test_repr(self, cached_node_Q42):
        s = model.Statement(cached_node_Q42)
        assert repr(s) == 'Statement(Node("Q42"))'

    def test_str(self, cached_node_Q42):
        s = model.Statement(cached_node_Q42)
        assert str(s) == "(Q42)"

    def test_describe(self, cached_node_Q42):
        s = model.Statement(cached_node_Q42)
        assert s.describe("en") == "Douglas Adams."

    def test_describe_lvl(self, cached_node_Q42):
        s = model.Statement(cached_node_Q42)
        assert s.describe("en", lvl=1) == "[Douglas Adams]"


class TestStatementNested:
    def test_repr(self, example_statement):
        assert (
            repr(model.Statement(example_statement))
            == 'Statement(LabeledEdge(Rel("P31"), Node("Q42"), Node("Q5")))'
        )

    def test_str(self, example_statement):
        assert str(model.Statement(example_statement)) == "((P31 Q42 Q5))"

    def test_describe(self, example_statement):
        assert (
            model.Statement(example_statement).describe("en")
            == "[Douglas Adams → human (instance of)]."
        )


class TestEdge:
    def test_repr(self, cached_node_Q42, cached_node_Q5):
        s = model.Edge(cached_node_Q42, cached_node_Q5)
        assert repr(s) == 'Edge(Node("Q42"), Node("Q5"))'

    def test_str(self, cached_node_Q42, cached_node_Q5):
        s = model.Edge(cached_node_Q42, cached_node_Q5)
        assert str(s) == "(Q42 Q5)"

    def test_describe(self, cached_node_Q42, cached_node_Q5):
        s = model.Edge(cached_node_Q42, cached_node_Q5)
        assert s.describe("en") == "Douglas Adams → human."

    def test_describe_lvl(self, cached_node_Q42, cached_node_Q5):
        s = model.Edge(cached_node_Q42, cached_node_Q5)
        assert s.describe("en", lvl=1) == "[Douglas Adams → human]"


class TestEdgeNested:
    def test_repr(self, example_statement, cached_node_Q42):
        assert (
            repr(model.Edge(cached_node_Q42, example_statement))
            == 'Edge(Node("Q42"), LabeledEdge(Rel("P31"), Node("Q42"), Node("Q5")))'
        )

    def test_str(self, example_statement, cached_node_Q42):
        assert (
            str(model.Edge(cached_node_Q42, example_statement)) == "(Q42 (P31 Q42 Q5))"
        )

    def test_describe(self, example_statement, cached_node_Q42):
        assert (
            model.Edge(cached_node_Q42, example_statement).describe("en")
            == "Douglas Adams → [Douglas Adams → human (instance of)]."
        )


class TestLabeledEdge:
    def test_repr(self, cached_rel_P31, cached_node_Q42, cached_node_Q5):
        s = model.LabeledEdge(cached_rel_P31, cached_node_Q42, cached_node_Q5)
        assert repr(s) == 'LabeledEdge(Rel("P31"), Node("Q42"), Node("Q5"))'

    def test_str(self, cached_rel_P31, cached_node_Q42, cached_node_Q5):
        s = model.LabeledEdge(cached_rel_P31, cached_node_Q42, cached_node_Q5)
        assert str(s) == "(P31 Q42 Q5)"

    def test_describe(self, cached_rel_P31, cached_node_Q42, cached_node_Q5):
        s = model.LabeledEdge(cached_rel_P31, cached_node_Q42, cached_node_Q5)
        assert s.describe("en") == "Douglas Adams → human (instance of)."

    def test_describe_lvl(self, cached_rel_P31, cached_node_Q42, cached_node_Q5):
        s = model.LabeledEdge(cached_rel_P31, cached_node_Q42, cached_node_Q5)
        assert s.describe("en", lvl=1) == "[Douglas Adams → human (instance of)]"


class TestLabeledEdgeNested:
    def test_repr(self, example_statement, cached_rel_P31, cached_node_Q42):
        assert (
            repr(model.LabeledEdge(cached_rel_P31, cached_node_Q42, example_statement))
            == 'LabeledEdge(Rel("P31"), Node("Q42"), LabeledEdge(Rel("P31"), Node("Q42"), Node("Q5")))'
        )

    def test_str(self, example_statement, cached_rel_P31, cached_node_Q42):
        assert (
            str(model.LabeledEdge(cached_rel_P31, cached_node_Q42, example_statement))
            == "(P31 Q42 (P31 Q42 Q5))"
        )

    def test_describe(self, example_statement, cached_rel_P31, cached_node_Q42):
        assert (
            model.LabeledEdge(
                cached_rel_P31, cached_node_Q42, example_statement
            ).describe("en")
            == "Douglas Adams → [Douglas Adams → human (instance of)] (instance of)."
        )
