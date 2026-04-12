"""CLI and console utilities."""

import shutil

import typer
import typer.core
from rich.traceback import install

install(show_locals=False)
typer.core.rich = None

# Logging
LOG_FORMAT_DEFAULT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS!UTC}</green> "
    "| <level>{level: <8}</level> "
    "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
    "- <level>{message}</level>"
)

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
    name: str | None = None,
    help_message: str | None = None,
    invoke_without_command: bool = False,
    hidden: bool = False,
    no_args_is_help: bool = True,
) -> typer.Typer:
    """Create a configured Typer instance.

    Args:
        name: App name.
        help_message: The help message for the Typer app.
        invoke_without_command: Whether to invoke without subcommand.
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
        help=help_message or (name or "CLI Application"),
        hidden=hidden,
        invoke_without_command=invoke_without_command,
        pretty_exceptions_show_locals=False,
    )


def get_terminal_width() -> int:
    """Get the current terminal width."""
    return shutil.get_terminal_size().columns


class CLITable:
    """Helper for formatting console tables."""

    @staticmethod
    def format_key_value(key: str, value: str, width: int | None = None) -> str:
        """Format a key-value pair for console output."""
        width = width or get_terminal_width()
        padding = width - len(key) - len(value) - 2
        padding = max(padding, 1)
        return f"{key}: {' ' * padding}{value}"
