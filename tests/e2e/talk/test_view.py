from typer.testing import CliRunner

from pycon_catalogue.cli.cli import app

runner = CliRunner(mix_stderr=False)


def test_existing(create_basic_talk):
    result = runner.invoke(app, ["talk", "view", str(create_basic_talk.id_)])

    assert result.exit_code == 0
    assert result.stdout


def test_existing_plain(create_basic_talk):
    result = runner.invoke(app, ["talk", "view", str(create_basic_talk.id_), "--plain"])

    assert result.exit_code == 0
    assert result.stdout


def test_existing_json(create_basic_talk):
    result = runner.invoke(app, ["talk", "view", str(create_basic_talk.id_), "--json"])

    assert result.exit_code == 0
    assert result.stdout


def test_not_existing():
    result = runner.invoke(app, ["talk", "view", "42"])

    assert result.exit_code == 1
    assert not result.stdout
    assert result.stderr == "Talk with ID 42 not found.\n"
