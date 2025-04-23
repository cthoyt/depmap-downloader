# -*- coding: utf-8 -*-

"""Main code."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

import bs4
import pystow
import requests

__all__ = [
    "URL",
    "get_downloads_table",
    "crispr_gene_dependencies_url",
    "ensure_crispr_gene_dependencies",
    "get_achilles_gene_dependencies_url",
    "ensure_achilles_gene_dependencies",
    "get_latest_rnai_url",
    "ensure_rnai_gene_dependencies",
    "get_rnai_essentiality",
    "get_crispr_essentiality",
]

URL = "https://depmap.org/portal/download/api/downloads"
DEPMAP_MODULE = pystow.module("bio", "depmap")
ACHILLES_NAME = "Achilles_gene_dependency.csv"
CRISPR_NAME = "CRISPRGeneEffect.csv"
CRISPR_OLD_NAME = "CRISPR_gene_dependency.csv"
RNAI_NAME = "D2_combined_gene_dep_scores.csv"


@lru_cache(1)
def get_downloads_table():
    """Get the full downloads table from the secret API."""
    return requests.get(URL).json()


@lru_cache(1)
def get_latest() -> str:
    """Get the latest release name."""
    latest = next(
        release for release in get_downloads_table()["releaseData"] if release["isLatest"]
    )
    return latest["releaseName"]


def _help_download(name: str, version: Optional[str] = None) -> str:
    if version is None:
        version = get_latest()
    for download in get_downloads_table()["table"]:
        if download["fileName"] == name and download["releaseName"] == version:
            return download["downloadUrl"]
    raise ValueError


def crispr_gene_dependencies_url(version: Optional[str] = None) -> str:
    """Get the CRISPR gene dependencies file URL."""
    return _help_download(CRISPR_NAME, version=version)


#: Columns: genes in the format "HUGO (Entrez)" - Rows: cell lines (Broad IDs)
def ensure_crispr_gene_dependencies(version: Optional[str] = None, force: bool = False) -> Path:
    """Ensure the CRISPR gene dependencies file is downloaded."""
    if version is None:
        version = get_latest()
    return DEPMAP_MODULE.ensure(
        version,
        url=crispr_gene_dependencies_url(version=version),
        force=force,
        name=CRISPR_NAME,
    )


def get_achilles_gene_dependencies_url(version: Optional[str] = None) -> str:
    """Get the Achilles gene dependencies file URL."""
    return _help_download(ACHILLES_NAME, version=version)


# Columns: genes in the format "HUGO (Entrez)" - Rows: cell lines (Broad IDs)
def ensure_achilles_gene_dependencies(version: Optional[str] = None, force: bool = False) -> Path:
    """Ensure the Achilles gene dependencies file is downloaded."""
    if version is None:
        version = get_latest()
    return DEPMAP_MODULE.ensure(
        version,
        url=get_achilles_gene_dependencies_url(version=version),
        name=ACHILLES_NAME,
        force=force,
    )


def get_latest_rnai_url():
    """Get the latest RNAi file URL."""
    table = get_downloads_table()["table"]
    for entry in table:
        # Note: there is only one RNAi file in the table, so we can just return it
        if entry["fileName"] == RNAI_NAME:
            return entry["downloadUrl"], entry["releaseName"].replace(" ", "_").lower()
    raise ValueError(f"Could not find {RNAI_NAME} in downloads table")


def ensure_rnai_gene_dependencies(force: bool = False) -> Path:
    """Get the RNAi gene dependencies file URL."""
    rnai_url, version = get_latest_rnai_url()
    return DEPMAP_MODULE.ensure(
        version,
        url=rnai_url,
        name=RNAI_NAME,
        force=force,
    )



def get_crispr_essentiality(symbol: str) -> float:
    """Get essentiality of the gene in the CRISPR experiments."""
    return _get_essentiality(symbol, "crispr")


def get_rnai_essentiality(symbol: str) -> float:
    """Get essentiality of the gene in the RNAi experiments."""
    return _get_essentiality(symbol, "rnai")


def _get_essentiality(symbol: str, dataset: str) -> float:
    url = f"https://depmap.org/portal/tile/gene/essentiality/{symbol}"
    res = requests.get(url).json()
    soup = bs4.BeautifulSoup(res["html"], features="html.parser")
    element = soup.find("h4", **{"class": dataset})
    fraction = element.text.split(":")[-1]
    num, denom = [float(part) for part in fraction.split("/")]
    return num / denom
