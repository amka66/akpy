"""
Test file
"""

from akpy.entry import go


def test_go():
    """Test go command"""
    assert go() is None
