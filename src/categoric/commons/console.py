import shutil

import typer

typer_dir_kwargs = dict(
    exists=False,
    file_okay=False,
    dir_okay=True,
    writable=True,
    readable=True,
    resolve_path=True,
)
typer_file_kwargs = dict(
    exists=False,
    file_okay=True,
    dir_okay=False,
    writable=True,
    readable=True,
    resolve_path=True,
)


def get_typer(
    help_message: str, hidden: bool = False, no_args_is_help: bool = True
) -> typer.Typer:
    """Create a configured Typer instance.

    Args:
        help_message: The help message for the Typer app.
        hidden: Whether the Typer app is hidden.
        no_args_is_help: Whether to show help when no arguments are provided.

    Returns:
        A configured typer.Typer instance.
    """
    return typer.Typer(
        context_settings=dict(
            help_option_names=["-h", "--help"],
            max_content_width=shutil.get_terminal_size().columns,
        ),
        pretty_exceptions_enable=False,
        rich_markup_mode=None,
        add_completion=False,
        no_args_is_help=no_args_is_help,
        help=help_message,
        hidden=hidden,
    )
