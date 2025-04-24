"""Test the API."""

import unittest

import depmap_downloader as dd


class TestAPI(unittest.TestCase):
    """Test the API."""

    def test_get_rnai_demeter(self):
        """Test getting the latest RNAi Demeter file."""
        url, version = dd.get_latest_rnai_url()
        self.assertEqual("https://ndownloader.figshare.com/files/13515395", url)
        self.assertEqual("demeter2_data_v6", version)

    def test_get_achilles(self) -> None:
        """Test getting the achilles URL."""
        url = dd.get_achilles_gene_dependencies_url(version="DepMap Public 21Q4")
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
