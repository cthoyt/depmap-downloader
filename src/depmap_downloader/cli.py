# -*- coding: utf-8 -*-

"""Command line interface for :mod:`depmap_downloader`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m depmap_downloader`` python will execute``__main__.py`` as a script.
  That means there won't be any ``depmap_downloader.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``depmap_downloader.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
"""

import logging
from typing import Optional

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
@verbose_option
@force_option
@click.option("--version", help="DepMap version, otherwise defaults to latest.")
def main(version: Optional[str], force: bool):
    """CLI for depmap_downloader."""
    path = ensure_crispr_gene_dependencies(version=version, force=force)
    click.echo(f"downloaded {path}")
    path = ensure_achilles_gene_dependencies(version=version, force=force)
    click.echo(f"downloaded {path}")
    path = ensure_rnai_gene_dependencies(force=force)
    click.echo(f"downloaded {path}")


if __name__ == "__main__":
    main()
