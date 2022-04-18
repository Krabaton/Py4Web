import aiohttp
from aiohttp_jinja2 import template
from src.store.models import Note, Tag


@template('index.html')
async def index(request):
    notes = await request.app["db"].note.query.gino.all()
    return {'title': 'Органайзер', "notes": notes}


@template('note.html')
async def note(request):
    return {'title': 'Органайзер'}


@template('detail.html')
async def detail(request):
    note_id = request.match_info.get('note_id')
    query = request.app["db"].tag.outerjoin(Note).select().where(Note.id == int(note_id))
    note = await query.gino.load(
        Note.distinct(Note.id).load(add_tag=Tag)).one()
    return {'title': 'Органайзер', "note": note}


@template('tag.html')
async def tag(request):
    note_id = request.match_info.get('note_id')
    return {'title': 'Органайзер', "note_id": note_id}


async def create_note(request):
    data = await request.post()
    name = data["name"]
    description = data["description"]
    tag = data["tag"]
    note = await request.app["db"].note.create(name=name, description=description, done=False)
    await request.app["db"].tag.create(name=tag, notes_id=note.id)
    location = request.app.router['index'].url_for()
    return aiohttp.web.HTTPFound(location=location)


async def done_note(request):
    note_id = request.match_info.get('note_id')
    note = await request.app["db"].note.query.where(Note.id == int(note_id)).gino.one()
    await note.update(done=True).apply()

    location = request.app.router['index'].url_for()
    return aiohttp.web.HTTPFound(location=location)


async def delete_note(request):
    note_id = request.match_info.get('note_id')
    note = await request.app["db"].note.query.where(Note.id == int(note_id)).gino.one()
    await note.delete()

    location = request.app.router['index'].url_for()
    return aiohttp.web.HTTPFound(location=location)


async def create_tag(request):
    note_id = request.match_info.get('note_id')
    data = await request.post()
    tag = data["name"]
    await request.app["db"].tag.create(name=tag, notes_id=int(note_id))

    location = request.app.router['index'].url_for()
    return aiohttp.web.HTTPFound(location=f"/detail/{note_id}")
