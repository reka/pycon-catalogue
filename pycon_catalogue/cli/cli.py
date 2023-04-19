#! /usr/bin/env python3

import typer
from rich.console import Console

from pycon_catalogue import __version__
from pycon_catalogue.cli import talk_cli

app = typer.Typer(rich_markup_mode="markdown")
app.add_typer(talk_cli.app, name="talk", help="Talk CRUD")


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, help="Print the current version."),
) -> None:
    """PyCon Catalogue"""
    if version:
        Console().print(__version__)
        return
    if ctx.invoked_subcommand is None:
        Console().print(ctx.get_help())
