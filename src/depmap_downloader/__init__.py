"""Reproducibly/automatically download data from the DepMap."""

from .api import (
    crispr_gene_dependencies_url,
    ensure_achilles_gene_dependencies,
    ensure_crispr_gene_dependencies,
    ensure_rnai_gene_dependencies,
    get_achilles_gene_dependencies_url,
    get_crispr_essentiality,
    get_latest_rnai_url,
    get_rnai_essentiality,
)

__all__ = [
    "crispr_gene_dependencies_url",
    "ensure_achilles_gene_dependencies",
    "ensure_crispr_gene_dependencies",
    "ensure_rnai_gene_dependencies",
    "get_achilles_gene_dependencies_url",
    "get_crispr_essentiality",
    "get_latest_rnai_url",
    "get_rnai_essentiality",
]
