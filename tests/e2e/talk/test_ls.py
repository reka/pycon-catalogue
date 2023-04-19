from typer.testing import CliRunner

from pycon_catalogue.cli.cli import app

runner = CliRunner(mix_stderr=False)


def test_empty_db():
    result = runner.invoke(app, ["talk", "ls"])

    assert result.exit_code == 0


def test_1_existing_talk(create_basic_talk):
    result = runner.invoke(app, ["talk", "ls"])

    assert result.exit_code == 0
    assert create_basic_talk.short_name in result.stdout


def test_1_existing_talk_plain(create_basic_talk):
    result = runner.invoke(app, ["talk", "ls", "--plain"])

    assert result.exit_code == 0
    assert len(result.stdout.splitlines()) == 1
    assert create_basic_talk.short_name in result.stdout

    # In the test,
    # the header and separator rows aren't printed.
    assert not result.stderr


def test_1_existing_talk_json(create_basic_talk):
    result = runner.invoke(app, ["talk", "ls", "--json"])

    assert result.exit_code == 0
    assert create_basic_talk.short_name in result.stdout
