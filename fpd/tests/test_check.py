from .. import check



def test_is_link():
    assert check.is_link("https://example.org")
    assert check.is_link("http://example.org")
    assert not check.is_link("rsync://example.org")

    assert check.is_link("https://example.org/example")
    assert not check.is_link("example.org")
    assert not check.is_link("/example")


def test_package_urls():
    package = check.Package("http://example.org/archlinux/core/os/x86_64/linux-0-x86_64.pkg.tar.xz")
    assert package.rel_url == "core/os/x86_64/linux-0-x86_64.pkg.tar.xz"
    assert package.base_url == "http://example.org/archlinux/core/os/x86_64/linux-0-x86_64.pkg.tar.xz"
    assert package.size == -1

    package.update_base_url("http://example.com/arch/")
    assert package.rel_url == "core/os/x86_64/linux-0-x86_64.pkg.tar.xz"
    assert package.base_url == "http://example.com/arch/core/os/x86_64/linux-0-x86_64.pkg.tar.xz"
    assert package.size == -1

