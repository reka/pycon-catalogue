from typer.testing import CliRunner

from pycon_catalogue.cli.cli import app

runner = CliRunner(mix_stderr=False)


def test_delete_existing_talk(create_basic_talk):
    result = runner.invoke(app, ["talk", "delete", str(create_basic_talk.id_)])

    assert result.exit_code == 0
    assert result.stderr == "Talk has been deleted.\n"


def test_not_existing():
    result = runner.invoke(app, ["talk", "delete", "42"])

    assert result.exit_code == 1
    assert not result.stdout
    assert result.stderr == "Talk with ID 42 not found.\n"
