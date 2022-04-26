import base64

from aiohttp import web
import aiohttp_jinja2
import jinja2
from cryptography import fernet
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from src.middlewares import authorize, error_middleware
from src.routes import setup_routes
from src.settings import config
from src.store.accessor import DBAccessor

app = web.Application()

fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))

app.middlewares.append(authorize)
app.middlewares.append(error_middleware)

aiohttp_jinja2.setup(app,
    loader=jinja2.PackageLoader('src', 'templates'))

app.router.add_static('/static', path='src/static', name='static')

setup_routes(app)

app["config"] = config
app["db"] = DBAccessor()
app["db"].setup(app)
app["websockets"] = []

if __name__ == '__main__':
    web.run_app(app, port=config["common"]["port"])
