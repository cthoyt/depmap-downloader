"""Main code."""

from functools import lru_cache
from pathlib import Path
from typing import Any, cast

import bs4
import pystow
import requests

__all__ = [
    "URL",
    "crispr_gene_dependencies_url",
    "ensure_achilles_gene_dependencies",
    "ensure_crispr_gene_dependencies",
    "ensure_rnai_gene_dependencies",
    "get_achilles_gene_dependencies_url",
    "get_crispr_essentiality",
    "get_downloads_table",
    "get_latest_rnai_url",
    "get_rnai_essentiality",
]

URL = "https://depmap.org/portal/download/api/downloads"
DEPMAP_MODULE = pystow.module("bio", "depmap")
ACHILLES_NAME = "Achilles_gene_dependency.csv"
CRISPR_NAME = "CRISPRGeneEffect.csv"
CRISPR_OLD_NAME = "CRISPR_gene_dependency.csv"
RNAI_DEMETER_NAME = "D2_combined_gene_dep_scores.csv"


@lru_cache(1)
def get_downloads_table() -> Any:
    """Get the full downloads table from the secret API."""
    return requests.get(URL, timeout=15).json()


@lru_cache(1)
def get_latest() -> str:
    """Get the latest release name."""
    latest = next(
        release for release in get_downloads_table()["releaseData"] if release["isLatest"]
    )
    return cast(str, latest["releaseName"])


def _help_download(name: str, version: str | None = None) -> str:
    if version is None:
        version = get_latest()
    for download in get_downloads_table()["table"]:
        if download["fileName"] == name and download["releaseName"] == version:
            return cast(str, download["downloadUrl"])
    raise ValueError


def crispr_gene_dependencies_url(version: str | None = None) -> str:
    """Get the CRISPR gene dependencies file URL."""
    return _help_download(CRISPR_NAME, version=version)


#: Columns: genes in the format "HUGO (Entrez)" - Rows: cell lines (Broad IDs)
def ensure_crispr_gene_dependencies(version: str | None = None, force: bool = False) -> Path:
    """Ensure the CRISPR gene dependencies file is downloaded."""
    if version is None:
        version = get_latest()
    return DEPMAP_MODULE.ensure(
        version,
        url=crispr_gene_dependencies_url(version=version),
        force=force,
        name=CRISPR_NAME,
    )


def get_achilles_gene_dependencies_url(version: str | None = None) -> str:
    """Get the Achilles gene dependencies file URL."""
    return _help_download(ACHILLES_NAME, version=version)


# Columns: genes in the format "HUGO (Entrez)" - Rows: cell lines (Broad IDs)
def ensure_achilles_gene_dependencies(version: str | None = None, force: bool = False) -> Path:
    """Ensure the Achilles gene dependencies file is downloaded."""
    if version is None:
        version = get_latest()
    return DEPMAP_MODULE.ensure(
        version,
        url=get_achilles_gene_dependencies_url(version=version),
        name=ACHILLES_NAME,
        force=force,
    )


def get_latest_rnai_url() -> tuple[str, str]:
    """Get the latest RNAi file URL."""
    table = get_downloads_table()["table"]
    for entry in table:
        # Note: there is only one RNAi Demeter file in the table, so we can just
        # return the first match and get the 'version' from the release name.
        if entry["fileName"] == RNAI_DEMETER_NAME:
            return entry["downloadUrl"], entry["releaseName"].replace(" ", "_").lower()
    raise ValueError(f"Could not find {RNAI_DEMETER_NAME} in downloads table")


def ensure_rnai_gene_dependencies(force: bool = False) -> Path:
    """Get the RNAi gene dependencies file URL."""
    rnai_url, version = get_latest_rnai_url()
    return DEPMAP_MODULE.ensure(
        version,
        url=rnai_url,
        name=RNAI_DEMETER_NAME,
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
    res = requests.get(url, timeout=15).json()
    soup = bs4.BeautifulSoup(res["html"], features="html.parser")
    element = soup.find("h4", class_=dataset)
    if element is None or element.text is None:
        raise ValueError
    fraction = element.text.split(":")[-1]
    num, denom = [float(part) for part in fraction.split("/")]
    return num / denom
