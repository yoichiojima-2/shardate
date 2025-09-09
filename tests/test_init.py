"""Tests for shardate.__init__ module."""

import pytest
from unittest.mock import patch
import importlib.metadata


def test_version_with_package_not_found_error():
    """Test that __version__ falls back to 'unknown' when package metadata is not found."""
    with patch('importlib.metadata.version', side_effect=importlib.metadata.PackageNotFoundError):
        # Re-import the module to trigger the exception handling
        import importlib
        import shardate
        importlib.reload(shardate)
        
        assert shardate.__version__ == "unknown"


def test_version_with_valid_package():
    """Test that __version__ is set correctly when package metadata is found."""
    with patch('importlib.metadata.version', return_value="1.0.0"):
        # Re-import the module to get the mocked version
        import importlib
        import shardate
        importlib.reload(shardate)
        
        assert shardate.__version__ == "1.0.0"