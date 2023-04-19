from pycon_catalogue.constants import TASKS_TABLE


def init_db(db):
    db[TASKS_TABLE].create(
        {
            "id": int,
            "short_name": str,
            "speaker_name": str,
            "title": str,
            "youtube_video_id": str,
        },
        pk="id",
    )
    db[TASKS_TABLE].create_index(["short_name"], unique=True)
