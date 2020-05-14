import pytest
from zola2pdf import set_header_depth

TEST = """
# h1
## h2
"""

def test_header_deth_0():

    expected = """
# h1
## h2
"""
    result = set_header_depth(TEST, 0)
    print(result)

    assert result == expected


def test_header_deth_1():

    expected = """
## h1
### h2
"""
    result = set_header_depth(TEST, 1)
    print(result)

    assert result == expected


def test_header_deth_2():

    expected = """
### h1
#### h2
"""
    result = set_header_depth(TEST, 2)
    print(result)

    assert result == expected