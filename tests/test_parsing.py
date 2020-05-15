from davar import parsing
from davar import model
import pytest


def test_transcribe_one_statement():
    assert parsing.transcribe("(P31 Q42 Q5)") == [
        model.Statement(model.Rel(31), model.Node(42), model.Node(5))
    ]


def test_transcribe_two_statements_with_space():
    assert parsing.transcribe("(P31 Q42 Q5) (P106 Q3236990 Q5482740)") == [
        model.Statement(model.Rel(31), model.Node(42), model.Node(5)),
        model.Statement(model.Rel(106), model.Node(3236990), model.Node(5482740)),
    ]
