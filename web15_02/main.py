from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.store.models import db
from src.router import notes, users, auth
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware


def get_app():
    app = FastAPI(title='The API')
    db.init_app(app)

    app.include_router(auth.router)
    app.include_router(notes.router)
    app.include_router(users.router)

    templates = Jinja2Templates(directory="templates")

    @app.get('/', response_class=HTMLResponse)
    def get_index(request: Request):
        return templates.TemplateResponse('index.html', {"request": request})

    app.mount('/source', StaticFiles(directory='./templates/source'), name='source')
    origins = [
        'http://127.0.0.1:5500'
    ]
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=['*'], allow_headers=['*'],
                       allow_credentials=True)

    black_list_ip = ['127.0.0.1']

    @app.middleware('http')
    async def check_ip(request: Request, call_next):
        ip = request.client.host
        if ip in black_list_ip:
            print('Block')
        response = await call_next(request)
        return response

    return app


app = get_app()
