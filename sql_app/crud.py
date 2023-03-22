from sqlalchemy import (
    and_,
    or_,
)
from .models import *


def initial_app():
    ins = settings.insert().values(
        url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
        api = "None",
        count = '5',
        language = "ru",
    )
    conn = engine.connect()
    conn.execute(ins)
    conn.close()
    return "ok"


def new_url(url: str):
    upd = settings.update().where(settings.c.id == 1).values(
        url = url
    )
    conn = engine.connect()
    conn.execute(upd)
    conn.close()
    return "ok"


def new_api(api: str):
    upd = settings.update().where(settings.c.id == 1).values(
        api = api
    )
    conn = engine.connect()
    conn.execute(upd)
    conn.close()
    return "ok"


def new_language(language: str):
    upd = settings.update().where(settings.c.id == 1).values(
        language = language
    )
    conn = engine.connect()
    conn.execute(upd)
    conn.close()
    return "ok"


def select_settings():
    sel = settings.select().where(settings.c.id == 1)
    conn = engine.connect()
    data = conn.execute(sel).fetchone()
    conn.close()
    if data is not None:
        return dict(data)
    else:
        return None


def new_count(count: str):
    upd = settings.update().where(settings.c.id == 1).values(
        count = count
    )
    conn = engine.connect()
    conn.execute(upd)
    conn.close()
    return "ok"


def reset_settings():
    upd = settings.update().where(settings.c.id == 1).values(
        url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
        api = "None",
        count = '5',
        language = "ru",

    )
    conn = engine.connect()
    conn.execute(upd)
    conn.close()
    return "ok"
