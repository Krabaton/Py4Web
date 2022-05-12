from fastapi import FastAPI
from src.store.models import db
from src.router import notes, users, auth


def get_app():
    app = FastAPI(title='The API')
    db.init_app(app)
    app.include_router(auth.router)
    app.include_router(notes.router)
    app.include_router(users.router)
    return app


app = get_app()