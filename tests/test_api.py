"""Test the API."""

import unittest

import depmap_downloader as dd
from depmap_downloader import get_achilles_gene_dependencies_url


class TestAPI(unittest.TestCase):
    """Test the API."""

    def test_get_achilles(self) -> None:
        """Test getting the achilles URL."""
        url = get_achilles_gene_dependencies_url(version="DepMap Public 21Q4")
        self.assertEqual("https://ndownloader.figshare.com/files/31315828", url)

    def test_essentiality(self) -> None:
        """Test getting CRISPR and RNAi essentiality."""
        self.assertEqual(119 / 1054, dd.get_crispr_essentiality("SOX10"))
        self.assertEqual(32 / 710, dd.get_rnai_essentiality("SOX10"))
