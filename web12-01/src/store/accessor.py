from aiohttp import web
from src.store.models import Note, Tag, db


class DBAccessor:
    def __init__(self):
        self.note = Note
        self.tag = Tag
        self.db = None

    def setup(self, app: web.Application):
        app.on_startup.append(self._on_connect)
        app.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, app: web.Application):
        self.config = app["config"]["postgres"]
        await db.set_bind(self.config["database_url"])
        self.db = db

    async def _on_disconnect(self, app: web.Application):
        if self.db is not None:
            await self.db.pop_bind().close()
