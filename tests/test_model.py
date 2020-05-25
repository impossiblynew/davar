from davar import model as m
import pytest


@pytest.fixture(scope="module")
def cached_WikidataItem_Q42():
    """
    Contains a cached copy of m.WikidataItem("Q42")
    """
    return m.WikidataItem("Q42")


@pytest.fixture(scope="module")
def cached_WikidataItem_Q5():
    """
    Contains a cached copy of m.WikidataItem("Q5")
    """
    return m.WikidataItem("Q5")


@pytest.fixture(scope="module")
def cached_WikidataProperty_P31():
    """
    Contains a cached copy of m.WikidataProperty("P5")
    """
    return m.WikidataProperty("P31")


@pytest.fixture(scope="module")
def example_statement(
    cached_WikidataProperty_P31, cached_WikidataItem_Q42, cached_WikidataItem_Q5
):
    # this is not used in tests that are of ability to construct a statement, only where that is the set up, like nesting tests.
    return m.LabeledEdge(
        cached_WikidataProperty_P31, cached_WikidataItem_Q42, cached_WikidataItem_Q5
    )


@pytest.mark.xfail  # FIXME: not sure how to make this work when validation is in effect
def test_abstract_node_describe():
    n = m.Node("42")
    with pytest.raises(NotImplementedError):
        n.describe("en")


def test_abstract_DavarWord_validate():
    with pytest.raises(NotImplementedError):
        m.DavarWord("Q42")


class TestWikidataItem:
    def test_describe(self, cached_WikidataItem_Q42):
        assert cached_WikidataItem_Q42.describe("en") == "Douglas Adams"

    def test_repr(self, cached_WikidataItem_Q42):
        assert repr(cached_WikidataItem_Q42) == 'WikidataItem("Q42")'

    def test_str(self, cached_WikidataItem_Q42):
        assert str(cached_WikidataItem_Q42) == "Q42"

    def test_validate(self):
        with pytest.raises(ValueError):
            m.WikidataItem("Q42Z")


class TestWikidataProperty:
    def test_describe(self, cached_WikidataProperty_P31):
        assert cached_WikidataProperty_P31.describe("en") == "instance of"

    def test_repr(self, cached_WikidataProperty_P31):
        assert repr(cached_WikidataProperty_P31) == 'WikidataProperty("P31")'

    def test_str(self, cached_WikidataProperty_P31):
        assert str(cached_WikidataProperty_P31) == "P31"


class TestOWNSynset:
    def test_describe(self):
        assert m.OMWSynset("02084071-n").describe("en") == "dog"

    def test_repr(self):
        assert repr(m.OMWSynset("02084071-n")) == 'OMWSynset("02084071-n")'

    def test_str(self):
        assert str(m.OMWSynset("02084071-n")) == "02084071-n"

    def test_validate(self):
        with pytest.raises(ValueError):
            m.OMWSynset("Q42")


class TestStatement:
    def test_repr(self, cached_WikidataItem_Q42):
        s = m.Statement(cached_WikidataItem_Q42)
        assert repr(s) == 'Statement(WikidataItem("Q42"))'

    def test_str(self, cached_WikidataItem_Q42):
        s = m.Statement(cached_WikidataItem_Q42)
        assert str(s) == "(Q42)"

    def test_describe(self, cached_WikidataItem_Q42):
        s = m.Statement(cached_WikidataItem_Q42)
        assert s.describe("en") == "Douglas Adams."

    def test_describe_lvl(self, cached_WikidataItem_Q42):
        s = m.Statement(cached_WikidataItem_Q42)
        assert s.describe("en", lvl=1) == "[Douglas Adams]"


class TestStatementNested:
    def test_repr(self, example_statement):
        assert (
            repr(m.Statement(example_statement))
            == 'Statement(LabeledEdge(WikidataProperty("P31"), WikidataItem("Q42"), WikidataItem("Q5")))'
        )

    def test_str(self, example_statement):
        assert str(m.Statement(example_statement)) == "((P31 Q42 Q5))"

    def test_describe(self, example_statement):
        assert (
            m.Statement(example_statement).describe("en")
            == "[Douglas Adams → human (instance of)]."
        )


class TestEdge:
    def test_repr(self, cached_WikidataItem_Q42, cached_WikidataItem_Q5):
        s = m.Edge(cached_WikidataItem_Q42, cached_WikidataItem_Q5)
        assert repr(s) == 'Edge(WikidataItem("Q42"), WikidataItem("Q5"))'

    def test_str(self, cached_WikidataItem_Q42, cached_WikidataItem_Q5):
        s = m.Edge(cached_WikidataItem_Q42, cached_WikidataItem_Q5)
        assert str(s) == "(Q42 Q5)"

    def test_describe(self, cached_WikidataItem_Q42, cached_WikidataItem_Q5):
        s = m.Edge(cached_WikidataItem_Q42, cached_WikidataItem_Q5)
        assert s.describe("en") == "Douglas Adams → human."

    def test_describe_lvl(self, cached_WikidataItem_Q42, cached_WikidataItem_Q5):
        s = m.Edge(cached_WikidataItem_Q42, cached_WikidataItem_Q5)
        assert s.describe("en", lvl=1) == "[Douglas Adams → human]"


class TestEdgeNested:
    def test_repr(self, example_statement, cached_WikidataItem_Q42):
        assert (
            repr(m.Edge(cached_WikidataItem_Q42, example_statement))
            == 'Edge(WikidataItem("Q42"), LabeledEdge(WikidataProperty("P31"), WikidataItem("Q42"), WikidataItem("Q5")))'
        )

    def test_str(self, example_statement, cached_WikidataItem_Q42):
        assert (
            str(m.Edge(cached_WikidataItem_Q42, example_statement))
            == "(Q42 (P31 Q42 Q5))"
        )

    def test_describe(self, example_statement, cached_WikidataItem_Q42):
        assert (
            m.Edge(cached_WikidataItem_Q42, example_statement).describe("en")
            == "Douglas Adams → [Douglas Adams → human (instance of)]."
        )


class TestLabeledEdge:
    def test_repr(
        self,
        cached_WikidataProperty_P31,
        cached_WikidataItem_Q42,
        cached_WikidataItem_Q5,
    ):
        s = m.LabeledEdge(
            cached_WikidataProperty_P31, cached_WikidataItem_Q42, cached_WikidataItem_Q5
        )
        assert (
            repr(s)
            == 'LabeledEdge(WikidataProperty("P31"), WikidataItem("Q42"), WikidataItem("Q5"))'
        )

    def test_str(
        self,
        cached_WikidataProperty_P31,
        cached_WikidataItem_Q42,
        cached_WikidataItem_Q5,
    ):
        s = m.LabeledEdge(
            cached_WikidataProperty_P31, cached_WikidataItem_Q42, cached_WikidataItem_Q5
        )
        assert str(s) == "(P31 Q42 Q5)"

    def test_describe(
        self,
        cached_WikidataProperty_P31,
        cached_WikidataItem_Q42,
        cached_WikidataItem_Q5,
    ):
        s = m.LabeledEdge(
            cached_WikidataProperty_P31, cached_WikidataItem_Q42, cached_WikidataItem_Q5
        )
        assert s.describe("en") == "Douglas Adams → human (instance of)."

    def test_describe_lvl(
        self,
        cached_WikidataProperty_P31,
        cached_WikidataItem_Q42,
        cached_WikidataItem_Q5,
    ):
        s = m.LabeledEdge(
            cached_WikidataProperty_P31, cached_WikidataItem_Q42, cached_WikidataItem_Q5
        )
        assert s.describe("en", lvl=1) == "[Douglas Adams → human (instance of)]"


class TestLabeledEdgeNested:
    def test_repr(
        self, example_statement, cached_WikidataProperty_P31, cached_WikidataItem_Q42
    ):
        assert (
            repr(
                m.LabeledEdge(
                    cached_WikidataProperty_P31,
                    cached_WikidataItem_Q42,
                    example_statement,
                )
            )
            == 'LabeledEdge(WikidataProperty("P31"), WikidataItem("Q42"), LabeledEdge(WikidataProperty("P31"), WikidataItem("Q42"), WikidataItem("Q5")))'
        )

    def test_str(
        self, example_statement, cached_WikidataProperty_P31, cached_WikidataItem_Q42
    ):
        assert (
            str(
                m.LabeledEdge(
                    cached_WikidataProperty_P31,
                    cached_WikidataItem_Q42,
                    example_statement,
                )
            )
            == "(P31 Q42 (P31 Q42 Q5))"
        )

    def test_describe(
        self, example_statement, cached_WikidataProperty_P31, cached_WikidataItem_Q42
    ):
        assert (
            m.LabeledEdge(
                cached_WikidataProperty_P31, cached_WikidataItem_Q42, example_statement
            ).describe("en")
            == "Douglas Adams → [Douglas Adams → human (instance of)] (instance of)."
        )


def test__bcp_42_to_iso_639_2():
    assert m._bcp_42_to_iso_639_2("en") == "eng"
