"""Tests"""
from httpbin import __version__


def test_version():
    """Test version"""
    assert __version__ == '0.0.1.dev1'
