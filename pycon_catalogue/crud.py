from sqlite_utils import Database
from sqlite_utils.db import NotFoundError

from pycon_catalogue.config import settings
from pycon_catalogue.errors import TalkNotFound
from pycon_catalogue.models import Talk


def talk_crud():
    return Crud(settings.db(), "talks", Talk)


class Crud:
    def __init__(self, db: Database, table_name: str, model) -> None:
        self.table = db.table(table_name)
        self.model = model

    def read_items(self):
        return list(self.table.rows)

    def create(self, properties: dict):
        model = self.model(**properties)
        self.table.insert(model.dict(exclude={"id_"}))
        inserted_id = self.table.last_pk
        return self.read(inserted_id)

    def read(self, item_id: int):
        try:
            return self.model(**self.table.get(item_id))
        except NotFoundError as e:
            raise TalkNotFound(f"Talk with ID {item_id} not found.") from e

    def update(self, item_id: int, properties: dict):
        try:
            self.table.update(item_id, properties)
            return self.read(item_id)
        except NotFoundError as e:
            raise TalkNotFound(f"Talk with ID {item_id} not found.") from e

    def delete(self, item_id: int):
        try:
            self.table.delete(item_id)
        except NotFoundError as e:
            raise TalkNotFound(f"Talk with ID {item_id} not found.") from e
