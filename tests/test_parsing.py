from davar import parsing
from davar import model
import pytest


def test_transcribe_singletonStatement():
    assert parsing.transcribe("(Q5)") == [model.Statement(model.Node("Q5"))]


def test_transcribe_Edge():
    assert parsing.transcribe("(Q42 Q5)") == [model.Edge(model.Node("Q42"), model.Node("Q5"))]


def test_transcribe_LabeledEdge():
    assert parsing.transcribe("(P31 Q42 Q5)") == [
        model.LabeledEdge(model.Rel("P31"), model.Node("Q42"), model.Node("Q5"))
    ]


def test_transcribe_multiple_LabeledEdges():
    assert parsing.transcribe("(P31 Q42 Q5) (P106 Q3236990 Q5482740)") == [
        model.LabeledEdge(model.Rel("P31"), model.Node("Q42"), model.Node("Q5")),
        model.LabeledEdge(model.Rel("P106"), model.Node("Q3236990"), model.Node("Q5482740")),
    ]


def test_transcribe_multiple_Statements():
    assert parsing.transcribe("(Q5)(P31 Q42 Q5) (Q5 Q42) (P106 Q3236990 Q5482740)") == [
        model.Statement(model.Node("Q5")),
        model.LabeledEdge(model.Rel("P31"), model.Node("Q42"), model.Node("Q5")),
        model.Edge(model.Node("Q5"), model.Node("Q42")),
        model.LabeledEdge(model.Rel("P106"), model.Node("Q3236990"), model.Node("Q5482740")),
    ]


def test_transcribe_nested_Statements():
    assert parsing.transcribe("(Q5482740 (P31 Q42 Q5))", debug=True) == [
        model.Edge(
            model.Node("Q5482740"),
            model.LabeledEdge(model.Rel("P31"), model.Node("Q42"), model.Node("Q5")),
        )
    ]
