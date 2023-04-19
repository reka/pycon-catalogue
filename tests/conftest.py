from pathlib import Path

import pytest

from pycon_catalogue import config
from pycon_catalogue.crud import talk_crud


@pytest.fixture(autouse=True)
def app_db_path(tmpdir):
    config.settings.db_path = Path(tmpdir / "pycon_test.db")


@pytest.fixture()
def create_basic_talk():
    return talk_crud().create({"short_name": "some name"})
