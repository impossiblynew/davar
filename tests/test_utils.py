import pytest
import davar.utils as d
import davar.model as m


@pytest.fixture(scope="module")
def flat_statement():
    return m.LabeledEdge(
        m.WikidataProperty("P31"),
        m.WikidataItem("Q3236990"),
        m.WikidataItem("Q5482740"),
    )


@pytest.fixture(scope="module")
def singleton_statement():
    return m.Statement(m.WikidataItem("Q2013"))


@pytest.fixture(scope="module")
def nested_statement():
    return m.Edge(
        m.WikidataItem("Q2"),
        m.LabeledEdge(
            m.WikidataProperty("P31"), m.WikidataItem("Q42"), m.WikidataItem("Q5")
        ),
    )


class TestDavar:
    def test_from_davartext(
        self, flat_statement, singleton_statement, nested_statement
    ):
        davar = d.Davar.from_davartext(
            "(P31 Q3236990 Q5482740) (Q2013)(Q2 (P31 Q42 Q5))"
        )
        assert davar.statements == [
            flat_statement,
            singleton_statement,
            nested_statement,
        ]

    def test_describe(self, flat_statement, singleton_statement, nested_statement):
        davar = d.Davar.from_davartext(
            "(P31 Q3236990 Q5482740) (Q2013)(Q2 (P31 Q42 Q5))"
        )
        assert davar.describe("en") == [
            flat_statement.describe("en"),
            singleton_statement.describe("en"),
            nested_statement.describe("en"),
        ]
