from davar import model
import pytest


@pytest.fixture(scope="module")
def cached_node_Q42():
    """
    Contains a cached copy of model.Node(42)
    """
    return model.Node(42)


@pytest.fixture(scope="module")
def cached_node_Q5():
    """
    Contains a cached copy of model.Node(5)
    """
    return model.Node(5)


@pytest.fixture(scope="module")
def cached_rel_P31():
    """
    Contains a cached copy of model.Rel(5)
    """
    return model.Rel(31)


class TestNode:
    def test_describe(self, cached_node_Q42):
        assert cached_node_Q42.describe("en") == "Douglas Adams"

    def test_repr(self, cached_node_Q42):
        assert repr(cached_node_Q42) == "Node(42)"

    def test_str(self, cached_node_Q42):
        assert str(cached_node_Q42) == "Q42"


class TestRel:
    def test_describe(self, cached_rel_P31):
        assert cached_rel_P31.describe("en") == "instance of"

    def test_repr(self, cached_rel_P31):
        assert repr(cached_rel_P31) == "Rel(31)"

    def test_str(self, cached_rel_P31):
        assert str(cached_rel_P31) == "P31"


class TestStatement:
    def test_repr(self, cached_node_Q42):
        s = model.Statement(cached_node_Q42)
        assert repr(s) == "Statement(Node(42))"

    def test_str(self, cached_node_Q42):
        s = model.Statement(cached_node_Q42)
        assert str(s) == "(Q42)"

    def test_describe(self, cached_node_Q42):
        s = model.Statement(cached_node_Q42)
        assert s.describe("en") == "Douglas Adams."


class TestEdge:
    def test_repr(self, cached_node_Q42, cached_node_Q5):
        s = model.Edge(cached_node_Q42, cached_node_Q5)
        assert repr(s) == "Edge(Node(42), Node(5))"

    def test_str(self, cached_node_Q42, cached_node_Q5):
        s = model.Edge(cached_node_Q42, cached_node_Q5)
        assert str(s) == "(Q42 Q5)"

    def test_describe(self, cached_node_Q42, cached_node_Q5):
        s = model.Edge(cached_node_Q42, cached_node_Q5)
        assert s.describe("en") == "Douglas Adams -> human."


class TestLabeledEdge:
    def test_repr(self, cached_rel_P31, cached_node_Q42, cached_node_Q5):
        s = model.LabeledEdge(cached_rel_P31, cached_node_Q42, cached_node_Q5)
        assert repr(s) == "LabeledEdge(Rel(31), Node(42), Node(5))"

    def test_str(self, cached_rel_P31, cached_node_Q42, cached_node_Q5):
        s = model.LabeledEdge(cached_rel_P31, cached_node_Q42, cached_node_Q5)
        assert str(s) == "(P31 Q42 Q5)"

    def test_describe(self, cached_rel_P31, cached_node_Q42, cached_node_Q5):
        s = model.LabeledEdge(cached_rel_P31, cached_node_Q42, cached_node_Q5)
        assert s.describe("en") == "Douglas Adams -> human (instance of)."
