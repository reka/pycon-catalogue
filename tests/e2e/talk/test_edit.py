from typer.testing import CliRunner

from pycon_catalogue.cli.cli import app
from pycon_catalogue.crud import talk_crud

runner = CliRunner(mix_stderr=False)


def test_non_interactive_update_short_name(create_basic_talk):
    talk_id = create_basic_talk.id_

    result = runner.invoke(
        app,
        [
            "talk",
            "edit",
            str(talk_id),
            "--no-input",
            "--short-name",
            "updated short_name",
        ],
    )

    assert result.exit_code == 0

    updated_talk = talk_crud().read(talk_id)
    assert updated_talk.short_name == "updated short_name"


def test_non_interactive_no_options(create_basic_talk):
    result = runner.invoke(
        app, ["talk", "edit", str(create_basic_talk.id_), "--no-input"]
    )

    assert result.exit_code == 1
    assert result.stderr == "Nothing to update.\n"


def test_not_existing():
    result = runner.invoke(app, ["talk", "edit", "42"])

    assert result.exit_code == 1
    assert not result.stdout
    assert result.stderr == "Talk with ID 42 not found.\n"
