from fastapi import APIRouter, status, Query
from src.schemas.notes import NoteCreationRequest
from src.schemas import StandardResponse
from src.services.master_service.notes import NotesMasterService

notes_router = APIRouter()
notes_master_service = NotesMasterService()

@notes_router.post("", 
                   response_model=StandardResponse,
                   status_code=status.HTTP_201_CREATED)
async def create_note(
    request: NoteCreationRequest
):
    master_service_response = await notes_master_service.create_note(request)
    
    response = StandardResponse(
        success=True,
        message="Note created successfully",
        data=master_service_response.model_dump()
    )
    
    return response
    
@notes_router.get("")
async def get_all_notes(
    limit:int = Query(default=10, ge=1, le=100),
    offset:int = Query(default=0, ge=0)
):
    master_service_response = await notes_master_service.get_all_notes(limit, offset)
    
    response = StandardResponse(
        success=True,
        message="Notes fetched successfully",
        data=master_service_response.model_dump()
    )
    
    return response
 
 
@notes_router.get("/{note_id}")
async def get_note_by_id(note_id: str):
    master_service_response = await notes_master_service.get_note_by_id(note_id)
    
    response = StandardResponse(
        success=True,
        message="Note fetched successfully",
        data=master_service_response.model_dump()
    )
    
    return response

@notes_router.put("/{note_id}")
async def update_note(note_id: str):
    pass

@notes_router.delete("/{note_id}")
async def delete_note(note_id: str):
    pass

@notes_router.post("/{note_id}/audio")
async def create_note_audio(note_id: str):
    pass

@notes_router.get("/{note_id}/audio")
async def get_note_audio(note_id: str):
    pass