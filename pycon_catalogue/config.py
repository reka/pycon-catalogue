from pathlib import Path

from pydantic import BaseSettings, Field
from sqlite_utils import Database

from pycon_catalogue.initialize import init_db


class Settings(BaseSettings):
    db_path: Path = Field(
        Path.home() / "pycon-catalogue.db", env="PYCON_CATALOGUE_DB_PATH"
    )

    def db(self) -> Database:
        # Move to constructor.
        if not self.db_path.exists():
            db = Database(self.db_path)
            init_db(db)

        return Database(self.db_path)


settings: Settings = Settings()
