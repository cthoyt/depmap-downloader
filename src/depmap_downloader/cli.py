"""Command line interface for :mod:`depmap_downloader`."""

import logging

import click
from more_click import force_option, verbose_option

from .api import (
    ensure_achilles_gene_dependencies,
    ensure_crispr_gene_dependencies,
    ensure_rnai_gene_dependencies,
)

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


@click.command()
@verbose_option  # type:ignore
@force_option  # type:ignore
@click.option("--version", help="DepMap version, otherwise defaults to latest.")
def main(version: str | None, force: bool) -> None:
    """CLI for depmap_downloader."""
    path = ensure_crispr_gene_dependencies(version=version, force=force)
    click.echo(f"downloaded {path}")
    path = ensure_achilles_gene_dependencies(version=version, force=force)
    click.echo(f"downloaded {path}")
    path = ensure_rnai_gene_dependencies(force=force)
    click.echo(f"downloaded {path}")


if __name__ == "__main__":
    main()
