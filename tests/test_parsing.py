from davar import parsing
from davar import model
import pytest


def test_transcribe_singletonStatement():
    assert parsing.transcribe("(Q5)") == [model.Statement(model.WikidataItem("Q5"))]


def test_transcribe_Edge():
    assert parsing.transcribe("(Q42 Q5)") == [
        model.Edge(model.WikidataItem("Q42"), model.WikidataItem("Q5"))
    ]


def test_transcribe_LabeledEdge():
    assert parsing.transcribe("(P31 Q42 Q5)") == [
        model.LabeledEdge(
            model.WikidataProperty("P31"),
            model.WikidataItem("Q42"),
            model.WikidataItem("Q5"),
        )
    ]


def test_transcribe_multiple_LabeledEdges():
    assert parsing.transcribe("(P31 Q42 Q5) (P106 Q3236990 Q5482740)") == [
        model.LabeledEdge(
            model.WikidataProperty("P31"),
            model.WikidataItem("Q42"),
            model.WikidataItem("Q5"),
        ),
        model.LabeledEdge(
            model.WikidataProperty("P106"),
            model.WikidataItem("Q3236990"),
            model.WikidataItem("Q5482740"),
        ),
    ]


def test_transcribe_multiple_Statements():
    assert parsing.transcribe("(Q5)(P31 Q42 Q5) (Q5 Q42) (P106 Q3236990 Q5482740)") == [
        model.Statement(model.WikidataItem("Q5")),
        model.LabeledEdge(
            model.WikidataProperty("P31"),
            model.WikidataItem("Q42"),
            model.WikidataItem("Q5"),
        ),
        model.Edge(model.WikidataItem("Q5"), model.WikidataItem("Q42")),
        model.LabeledEdge(
            model.WikidataProperty("P106"),
            model.WikidataItem("Q3236990"),
            model.WikidataItem("Q5482740"),
        ),
    ]


def test_transcribe_nested_Statements():
    assert parsing.transcribe("(Q5482740 (P31 Q42 Q5))", debug=True) == [
        model.Edge(
            model.WikidataItem("Q5482740"),
            model.LabeledEdge(
                model.WikidataProperty("P31"),
                model.WikidataItem("Q42"),
                model.WikidataItem("Q5"),
            ),
        )
    ]
