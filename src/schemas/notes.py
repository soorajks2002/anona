from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class NoteCreationRequest(BaseModel):
    topic: str
    character_id: str
    
    
class NoteBase(BaseModel):
    note_id: str
    note_slug: str
    note_title: str
    note_created_at: datetime


class FullSingleNoteResponse(NoteBase):
    note_text: str
    note_audio_url: Optional[str] = None
    note_creator: str
    note_topic: str
    
    class Config:
        populate_by_name = True
        
        
class PartialSingleNoteResponse(NoteBase):
    """Used for list views where we don't need all the note details"""
    pass


class NotesListResponse(BaseModel):
    total_notes: int
    limit: int
    offset: int
    has_next: bool
    items: List[PartialSingleNoteResponse]