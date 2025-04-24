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
        # was 119 / 1054, but has been updated to 124/1178
        crispr_essentiality = dd.get_crispr_essentiality("SOX10")
        self.assertLess(0, crispr_essentiality)
        self.assertLess(crispr_essentiality, 1.0)
        # was 32 / 710
        rnai_essentiality = dd.get_rnai_essentiality("SOX10")
        self.assertLess(0, rnai_essentiality)
        self.assertLess(rnai_essentiality, 1.0)
