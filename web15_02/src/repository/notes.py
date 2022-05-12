from fastapi import status, HTTPException
from src.store.models import DbNotes, db


async def create_note(note):
    new_note = await DbNotes.create(title=note.title, content=note.content)
    return new_note


async def get_all_notes():
    all_notes = await db.all(DbNotes.query)
    return all_notes


async def get_note(id: int):
    note = await DbNotes.get(id)
    return note


async def update_note(id: int, u_note):
    note = await DbNotes.get(id)
    if note is None:
        raise HTTPException(status_code=404, detail=f'Note with id {id} not found')
    await note.update(title=u_note.title, content=u_note.content).apply()
    return note


async def delete_note(id: int):
    note = await DbNotes.get(id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Note with id {id} not found')
    await note.delete()
    return note
