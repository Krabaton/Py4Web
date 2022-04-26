import aiohttp
from aiohttp import web
import aiohttp_jinja2
from aiohttp_jinja2 import template
from aiohttp_session import get_session

from src.chat.service_weather import get_weather
from src.store.models import User, Messages


class ChatList(web.View):
    @template('pages/chat.html')
    async def get(self):
        session = await get_session(self.request)
        auth = True if 'user' in session else False
        messages = await self.request.app["db"].messages.outerjoin(User).select().limit(25)\
            .order_by(Messages.created.desc()).gino.all()
        return {'title': 'Chat', 'messages': messages, 'auth': auth}


class WebSocket(web.View):
    async def get(self):

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        session = await get_session(self.request)
        login = session['user']
        for _ws in self.request.app['websockets']:
            await _ws.send_str(f'{login} joined')
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            print(msg)
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                elif msg.data.startswith('/weather'):
                    _, city, *rest = msg.data.split(' ')
                    result = await get_weather(city)
                    await ws.send_str(result)
                else:
                    await self.request.app['db'].messages.create(message=msg.data, user_id=int(session['user_id']))
                    for _ws in self.request.app['websockets']:
                        await _ws.send_str(f'{login}: {msg.data}')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        self.request.app['websockets'].remove(ws)
        for _ws in self.request.app['websockets']:
            await _ws.send_str(f'{login} disconnected')
        print('websocket connection closed')

        return ws
