"""Tests for shardate.__init__ module."""
import importlib.metadata
import unittest.mock

import shardate


def test_version_with_package_not_found_error():
    """Test version handling when PackageNotFoundError is raised."""
    with unittest.mock.patch(
        'importlib.metadata.version',
        side_effect=importlib.metadata.PackageNotFoundError()
    ):
        # Reload the module to trigger the exception handling
        import importlib
        importlib.reload(shardate)
        assert shardate.__version__ == "unknown"


def test_version_with_valid_package():
    """Test version retrieval when package is found."""
    with unittest.mock.patch(
        'importlib.metadata.version',
        return_value="1.2.3"
    ):
        # Reload the module to trigger version retrieval
        import importlib
        importlib.reload(shardate)
        assert shardate.__version__ == "1.2.3"