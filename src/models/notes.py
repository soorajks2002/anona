from src.core.database import db
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteCollectionModel(BaseModel):
    note_id: str = Field(alias="_id")
    note_topic: str
    note_slug: str
    note_title: str
    note_text: str
    note_creator: str
    note_audio_url: Optional[str] = None
    note_created_at: datetime
    
    class Config:
        populate_by_name = True
        
class NoteCollectionListModel(BaseModel):
    note_id: str = Field(alias="_id")
    note_slug: str
    note_title: str
    note_created_at: datetime
    
    class Config:
        populate_by_name = True

class NoteCollectionManager:
    collection_name = "notes"
    
    @staticmethod
    async def get_collection():
        return db.get_database()[NoteCollectionManager.collection_name]
    
    @staticmethod
    async def create_note(note: NoteCollectionModel):
        collection = await NoteCollectionManager.get_collection()
        document = note.model_dump(by_alias=True)
        response = await collection.insert_one(document)
        return response

    @staticmethod
    async def get_all_notes(limit: int, offset: int) -> list[dict]:
        collection = await NoteCollectionManager.get_collection()
        notes_cursor = await collection.find().skip(offset).limit(limit).to_list(length=None)
        return notes_cursor
    
    @staticmethod
    async def get_note_count() -> int:
        collection = await NoteCollectionManager.get_collection()
        count = await collection.count_documents({})
        return count
    
    @staticmethod
    async def get_note_by_id(note_id: str) -> dict:
        collection = await NoteCollectionManager.get_collection()
        note = await collection.find_one({"_id": note_id})
        return note