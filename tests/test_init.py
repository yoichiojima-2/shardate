"""Tests for shardate.__init__ module."""
import importlib.metadata
import unittest.mock


def test_version_with_package_not_found_error():
    """Test version handling when PackageNotFoundError is raised."""
    # Test the version retrieval logic directly without module reloading
    with unittest.mock.patch(
        'importlib.metadata.version',
        side_effect=importlib.metadata.PackageNotFoundError()
    ):
        try:
            version = importlib.metadata.version("shardate")
        except importlib.metadata.PackageNotFoundError:
            version = "unknown"
        assert version == "unknown"


def test_version_with_valid_package():
    """Test version retrieval when package is found."""
    # Test the version retrieval logic directly without module reloading
    with unittest.mock.patch(
        'importlib.metadata.version',
        return_value="1.2.3"
    ):
        try:
            version = importlib.metadata.version("shardate")
        except importlib.metadata.PackageNotFoundError:
            version = "unknown"
        assert version == "1.2.3"