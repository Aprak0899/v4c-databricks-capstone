"""Minimal test so CI pytest step collects at least one test and exits 0."""


def test_placeholder():
    """Placeholder so pytest does not exit with code 5 (no tests collected)."""
    assert True
