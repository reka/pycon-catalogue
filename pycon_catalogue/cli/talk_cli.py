#! /usr/bin/env python3

import sys

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table

from pycon_catalogue.cli.common_options import INTERACTIVE_OPTION, FormatOptions
from pycon_catalogue.cli.utils import exit_with_error, get_from_options
from pycon_catalogue.crud import talk_crud
from pycon_catalogue.errors import TalkNotFound
from pycon_catalogue.models import Talk

app = typer.Typer(rich_markup_mode="markdown")

short_name_option: str = typer.Option(
    None,
    help="The short_name of the talk.",
)

speaker_name_option: str = typer.Option(
    None,
    help="The speaker_name of the talk.",
)

title_option: str = typer.Option(
    None,
    help="The title of the talk.",
)

youtube_video_id_option: str = typer.Option(
    None,
    help="The youtube_video_id of the talk.",
)


@app.command()
def create(
    ctx: typer.Context,
    short_name: str = short_name_option,
    speaker_name: str = speaker_name_option,
    title: str = title_option,
    youtube_video_id: str = youtube_video_id_option,
    interactive_flag: bool = INTERACTIVE_OPTION,
    plain: bool = FormatOptions.PLAIN,
    show_json: bool = FormatOptions.JSON,
):
    """Create a new talk"""
    interactive = sys.stdin.isatty() and interactive_flag

    stdout_console = Console()
    stderr_console = Console(stderr=True)

    provided_further_fields = _get_field_values(ctx, interactive, stderr_console)
    try:
        result = talk_crud().create(provided_further_fields)
    except ValidationError as e:
        if not interactive or not Talk.all_simple_field_errors(e):
            raise exit_with_error(f"Can't create a talk. {e}") from e

        for error_data in e.errors():
            field_name = error_data["loc"][0]
            msg = error_data["msg"]
            stderr_console.print(f"Validation error. {field_name} {msg}")
            provided_further_fields[field_name] = Prompt.ask(field_name)
        try:
            result = talk_crud().create(provided_further_fields)
        except ValidationError as e_next:
            raise exit_with_error(f"Talk still invalid. {e_next}") from e_next
    stderr_console.print("New talk created. 🪅")
    _print_talk(result, show_json, plain)


@app.command()
def ls(
    plain: bool = FormatOptions.PLAIN,
    show_json: bool = FormatOptions.JSON,
):
    """List all talks"""
    result = talk_crud().read_items()

    stdout_console = Console()
    stderr_console = Console(stderr=True)

    if show_json:
        stdout_console.print_json(data=result)
        return

    if plain:
        # Define the maximum width of each column
        max_width = [5, 42]

        # Print a header & a separator row
        # if the output isn't redirected.
        if sys.stdout.isatty():
            # Print the header row
            header = ["ID", "short_name"]
            stderr_console.print(
                "|".join([f"{h:<{max_width[i]}}" for i, h in enumerate(header)])
            )
            # Print the separator row
            stderr_console.print(
                "|".join(["-" * max_width[i] for i in range(len(max_width))])
            )
        for item in result:
            id_str = f"{item['id']:<{max_width[0]}}"
            short_name_str = f"{item['short_name']:<{max_width[0]}}"
            stdout_console.print(f"{id_str}|{short_name_str}")
        return

    table = Table(show_header=True)
    table.add_column("ID")
    table.add_column("short_name")

    for item in result:
        table.add_row(str(item["id"]), item["short_name"])
    stdout_console.print(table)


@app.command()
def view(
    talk_id: int,
    plain: bool = FormatOptions.PLAIN,
    show_json: bool = FormatOptions.JSON,
):
    """Get a talk by ID."""
    try:
        talk = talk_crud().read(talk_id)
    except TalkNotFound as e:
        raise exit_with_error(str(e)) from e

    _print_talk(talk, show_json, plain)


@app.command(name="delete")
def delete_talk(talk_id: int):
    """Delete a talk by ID."""
    try:
        talk_crud().delete(talk_id)
    except TalkNotFound as e:
        raise exit_with_error(str(e)) from e

    console_stderr = Console(stderr=True)
    console_stderr.print("Talk has been deleted.")


@app.command()
def edit(
    ctx: typer.Context,
    talk_id: int,
    short_name: str = short_name_option,
    speaker_name: str = speaker_name_option,
    title: str = title_option,
    youtube_video_id: str = youtube_video_id_option,
    plain: bool = FormatOptions.PLAIN,
    show_json: bool = FormatOptions.JSON,
    interactive_flag: bool = INTERACTIVE_OPTION,
):
    interactive = sys.stdin.isatty() and interactive_flag

    try:
        current_talk = talk_crud().read(talk_id).dict()
    except TalkNotFound as e:
        raise exit_with_error(str(e)) from e

    talk_field_names = Talk.non_id_further_fields()
    provided_further_fields = get_from_options(ctx, talk_field_names)

    # Ask for input values in interactive mode.
    if not provided_further_fields and interactive:
        for field_name in talk_field_names:
            updated_value = Prompt.ask(field_name, default=current_talk[field_name])
            if updated_value != current_talk[field_name]:
                provided_further_fields[field_name] = updated_value

    if not provided_further_fields:
        raise exit_with_error("Nothing to update.")

    talk = talk_crud().update(talk_id, provided_further_fields)

    console_stderr = Console(stderr=True)
    console_stderr.print("Talk has been updated.")

    _print_talk(talk, show_json, plain)


def _print_talk(talk: Talk, show_json: bool, plain: bool):
    stdout_console = Console()

    if show_json:
        stdout_console.print_json(talk.json())
    else:
        output = talk.get_plain() if plain else Markdown(talk.get_markdown())
        stdout_console.print(output)


def _get_field_values(ctx, interactive, stderr_console):
    talk_field_names = Talk.non_id_further_fields()
    if further_fields_from_options := get_from_options(ctx, talk_field_names):
        return further_fields_from_options

    if not interactive:
        raise exit_with_error("Can't create a talk. No further_fields provided.")

    stderr_console.print("Please enter the values for the further_fields of the talk.")
    entered_further_fields = {
        field_name: Prompt.ask(field_name) for field_name in talk_field_names
    }
    return entered_further_fields
