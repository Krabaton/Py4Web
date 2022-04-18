from aiohttp import web
import aiohttp_jinja2
import jinja2
from src.routes import setup_routes

# async def handle(request):
#     name = request.match_info.get('name', "Anonymous")
#     text = "Hello, " + name
#     return web.Response(text=text)
from src.settings import config
from src.store.accessor import DBAccessor

app = web.Application()

aiohttp_jinja2.setup(app,
    loader=jinja2.PackageLoader('src', 'templates'))

setup_routes(app)
app["config"] = config
app["db"] = DBAccessor()
app["db"].setup(app)

if __name__ == '__main__':
    web.run_app(app, port=config["common"]["port"])
