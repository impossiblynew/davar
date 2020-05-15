from davar import model
import pytest


def test_Node_label_getting():
    n = model.Node(42)
    assert n.get_label("en") == "Douglas Adams"


def test_Node_repr():
    n = model.Node(42)
    assert repr(n) == "Node(42)"


def test_Node_str():
    n = model.Node(42)
    assert str(n) == "Q42"


def test_Rel_label_getting():
    r = model.Rel(31)
    assert r.get_label("en") == "instance of"


def test_Rel_repr():
    r = model.Rel(31)
    assert repr(r) == "Rel(31)"


def test_Rel_str():
    r = model.Rel(31)
    assert str(r) == "P31"


def test_Statement_repr():
    r = model.Rel(31)
    n = model.Node(42)
    s = model.Statement(r, n, n)
    assert repr(s) == "Statement(Rel(31), Node(42), Node(42))"


def test_Statement_str():
    r = model.Rel(31)
    n = model.Node(42)
    s = model.Statement(r, n, n)
    assert str(s) == "(P31 Q42 Q42)"


def test_Statement_describe():
    r = model.Rel(31)
    n = model.Node(42)
    s = model.Statement(r, n, n)
    assert s.describe("en") == "Douglas Adams -> Douglas Adams (instance of)"
