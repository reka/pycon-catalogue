import pytest
from typer.testing import CliRunner

from pycon_catalogue.cli.cli import app

runner = CliRunner(mix_stderr=False)


@pytest.mark.parametrize(
    ("cmd_parts"),
    [
        (["talk", "create", "--short-name", "thing 1"]),
    ],
)
def test_success(cmd_parts):
    result = runner.invoke(app, cmd_parts)

    assert result.exit_code == 0

    assert result.stdout

    # stderr
    assert "New talk created. 🪅" in result.stderr


def test_no_further_fields_no_input():
    result = runner.invoke(app, ["talk", "create", "--no-input"])

    assert result.exit_code == 1
    assert result.stderr == "Can't create a talk. No further_fields provided.\n"


def test_empty_short_name():
    result = runner.invoke(app, ["talk", "create", "--short-name", "", "--no-input"])

    assert result.exit_code == 1
    assert not result.stdout
    assert result.stderr.startswith("Can't create a talk.")
    assert "validation error" in result.stderr
