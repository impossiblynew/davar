from davar import model
import pytest


def test_Node_describe():
    n = model.Node(42)
    assert n.describe("en") == "Douglas Adams"


def test_Node_repr():
    n = model.Node(42)
    assert repr(n) == "Node(42)"


def test_Node_str():
    n = model.Node(42)
    assert str(n) == "Q42"


def test_Rel_describe():
    r = model.Rel(31)
    assert r.describe("en") == "instance of"


def test_Rel_repr():
    r = model.Rel(31)
    assert repr(r) == "Rel(31)"


def test_Rel_str():
    r = model.Rel(31)
    assert str(r) == "P31"


def test_Statement_repr():
    n_sub = model.Node(42)
    s = model.Statement(n_sub)
    assert repr(s) == "Statement(Node(42))"


def test_Statement_str():
    n_sub = model.Node(42)
    s = model.Statement(n_sub)
    assert str(s) == "(Q42)"


def test_Statement_describe():
    n_sub = model.Node(42)
    s = model.Statement(n_sub)
    assert s.describe("en") == "Douglas Adams."


def test_Edge_repr():
    n_sub = model.Node(42)
    n_ob = model.Node(5)
    s = model.Edge(n_sub, n_ob)
    assert repr(s) == "Edge(Node(42), Node(5))"


def test_Edge_str():
    n_sub = model.Node(42)
    n_ob = model.Node(5)
    s = model.Edge(n_sub, n_ob)
    assert str(s) == "(Q42 Q5)"


def test_Edge_describe():
    n_sub = model.Node(42)
    n_ob = model.Node(5)
    s = model.Edge(n_sub, n_ob)
    assert s.describe("en") == "Douglas Adams -> human."


def test_LabeledEdge_repr():
    r = model.Rel(31)
    n_sub = model.Node(42)
    n_ob = model.Node(5)
    s = model.LabeledEdge(r, n_sub, n_ob)
    assert repr(s) == "LabeledEdge(Rel(31), Node(42), Node(5))"


def test_LabeledEdge_str():
    r = model.Rel(31)
    n_sub = model.Node(42)
    n_ob = model.Node(5)
    s = model.LabeledEdge(r, n_sub, n_ob)
    assert str(s) == "(P31 Q42 Q5)"


def test_LabeledEdge_describe():
    r = model.Rel(31)
    n_sub = model.Node(42)
    n_ob = model.Node(5)
    s = model.LabeledEdge(r, n_sub, n_ob)
    assert s.describe("en") == "Douglas Adams -> human (instance of)."
