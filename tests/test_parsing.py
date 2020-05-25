from davar import parsing
from davar import model as m
import pytest


def test_transcribe_singletonStatement():
    assert parsing.transcribe("(Q5)") == [m.Statement(m.WikidataItem("Q5"))]


def test_transcribe_Edge():
    assert parsing.transcribe("(Q42 Q5)") == [
        m.Edge(m.WikidataItem("Q42"), m.WikidataItem("Q5"))
    ]


def test_transcribe_LabeledEdge():
    assert parsing.transcribe("(P31 Q42 Q5)") == [
        m.LabeledEdge(
            m.WikidataProperty("P31"), m.WikidataItem("Q42"), m.WikidataItem("Q5"),
        )
    ]


def test_transcribe_multiple_LabeledEdges():
    assert parsing.transcribe("(P31 Q42 Q5) (P106 Q3236990 Q5482740)") == [
        m.LabeledEdge(
            m.WikidataProperty("P31"), m.WikidataItem("Q42"), m.WikidataItem("Q5"),
        ),
        m.LabeledEdge(
            m.WikidataProperty("P106"),
            m.WikidataItem("Q3236990"),
            m.WikidataItem("Q5482740"),
        ),
    ]


def test_transcribe_multiple_Statements():
    assert parsing.transcribe("(Q5)(P31 Q42 Q5) (Q5 Q42) (P106 Q3236990 Q5482740)") == [
        m.Statement(m.WikidataItem("Q5")),
        m.LabeledEdge(
            m.WikidataProperty("P31"), m.WikidataItem("Q42"), m.WikidataItem("Q5"),
        ),
        m.Edge(m.WikidataItem("Q5"), m.WikidataItem("Q42")),
        m.LabeledEdge(
            m.WikidataProperty("P106"),
            m.WikidataItem("Q3236990"),
            m.WikidataItem("Q5482740"),
        ),
    ]


def test_transcribe_nested_Statements():
    assert parsing.transcribe("(Q5482740 (P31 Q42 Q5))", debug=True) == [
        m.Edge(
            m.WikidataItem("Q5482740"),
            m.LabeledEdge(
                m.WikidataProperty("P31"), m.WikidataItem("Q42"), m.WikidataItem("Q5"),
            ),
        )
    ]


@pytest.mark.xfail
def test_transcribe_OWNSynsets():
    assert parsing.transcribe("(01835496-v 02084071-n 00110659-r)", debug=True) == [
        m.LabeledEdge(
            m.OMWSynset("01835496-v"),
            m.OMWSynset("02084071-n"),
            m.OMWSynset("00110659-r"),
        )
    ]
