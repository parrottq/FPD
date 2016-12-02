from .. import check



def test_is_link():
    assert check.is_link("https://example.org")
    assert check.is_link("http://example.org")
    assert not check.is_link("rsync://example.org")

    assert check.is_link("https://example.org/example")
    assert not check.is_link("example.org")
    assert not check.is_link("/example")

