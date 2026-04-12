#!/usr/bin/env python3 -u
import shutil

import typer.core
from rich.traceback import install

install(show_locals=False)
typer.core.rich = None

app = typer.Typer(
    context_settings=dict(
        help_option_names=["-h", "--help"],
        max_content_width=shutil.get_terminal_size().columns,
    ),
    pretty_exceptions_enable=False,
    rich_markup_mode=None,
    add_completion=False,
    no_args_is_help=True,
    help="Categoric CLI",
    hidden=False,
)


@app.callback()
def main(ctx: typer.Context) -> None:
    pass


if __name__ == "__main__":
    app()
