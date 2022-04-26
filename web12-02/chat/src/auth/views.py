import aiohttp
from aiohttp import web
import aiohttp_jinja2
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from src.store.models import User


class Main(web.View):
    @template('pages/index.html')
    async def get(self):
        session = await get_session(self.request)
        auth = True if 'user' in session else False
        return {'title': 'Chat', 'auth': auth}


class Login(web.View):
    @template('pages/login.html')
    async def get(self):
        return {'title': 'Chat'}

    async def post(self):
        data = await self.request.post()
        user = await self.request.app["db"].user.query.where(User.email == data['email']).gino.one()
        if user and user.password == data['password']:
            session = await get_session(self.request)
            session['user'] = user.login
            session['user_id'] = user.id
            location = self.request.app.router['main'].url_for()
            return aiohttp.web.HTTPFound(location=location)
        else:
            raise web.HTTPFound('/login')


class SignIn(web.View):
    @template('pages/reg.html')
    async def get(self):
        return {'title': 'Chat'}

    async def post(self):
        data = await self.request.post()
        await self.request.app["db"].user.create(email=data['email'], password=data['password'], login=data['login'])
        location = self.request.app.router['login'].url_for()
        return aiohttp.web.HTTPFound(location=location)


class SignOut(web.View):
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
            location = self.request.app.router['login'].url_for()
            return aiohttp.web.HTTPFound(location=location)
        else:
            raise web.HTTPForbidden(text='Forbidden')

