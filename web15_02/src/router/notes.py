from typing import List
from fastapi import APIRouter, Response, status, Depends, HTTPException

from src.lib.oauth2 import get_current_user
from src.repository import notes
from src.schemas.notes import NoteModel, NoteResponse
from src.schemas.users import UserModel

router = APIRouter(prefix='/notes', tags=['notes'])


@router.get('/', response_model=List[NoteResponse])
async def get_all_notes(current_user: UserModel = Depends(get_current_user)):
    all_notes = await notes.get_all_notes()
    return all_notes


@router.get('/{id}', response_model=NoteResponse)
async def get_all_notes(id: int, current_user: UserModel = Depends(get_current_user)):
    note = await notes.get_note(id)
    print(note)
    if note is None:
        raise HTTPException(status_code=404, detail=f'Note with id {id} not found')
    return note


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=NoteResponse)
async def create_note(note: NoteModel, current_user: UserModel = Depends(get_current_user)):
    new_note = await notes.create_note(note)
    return new_note


@router.put('/{id}', response_model=NoteResponse)
async def create_note(note: NoteModel, id: int, current_user: UserModel = Depends(get_current_user)):
    update_note = await notes.update_note(id, note)
    return update_note


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def create_note(id: int, current_user: UserModel = Depends(get_current_user)):
    await notes.delete_note(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
