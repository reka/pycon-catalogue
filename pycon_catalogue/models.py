from pydantic import BaseModel, Field, ValidationError


class BasePyConCatalogueModel(BaseModel):
    @classmethod
    def non_id_further_fields(cls):
        all_further_fields = set(cls.schema()["properties"].keys())
        all_further_fields.remove("id")
        return all_further_fields

    @classmethod
    def all_simple_field_errors(cls, validation_error: ValidationError):
        return all(cls.is_simple_field_error(e) for e in validation_error.errors())

    @classmethod
    def is_simple_field_error(cls, e: dict) -> bool:
        return len(e["loc"]) == 1 and e["loc"][0] in cls.non_id_further_fields()


class Talk(BasePyConCatalogueModel):
    id_: int | None = Field(None, alias="id")
    short_name: str = Field(min_length=5, max_length=64)

    speaker_name: str | None

    title: str | None

    youtube_video_id: str | None

    def get_markdown(self) -> str:
        return f"""# {self.short_name}

ID: {self.id_}

* {self.speaker_name}

* {self.title}

* {self.youtube_video_id}

"""

    def get_plain(self) -> str:
        return f"""ID: {self.id_}
short_name: {self.short_name}

speaker_name: {self.speaker_name}

title: {self.title}

youtube_video_id: {self.youtube_video_id}

"""
