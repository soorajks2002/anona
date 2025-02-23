from src.services.text_generation.openai import OpenAITextGenerationService
from src.schemas.notes import NoteCreationRequest, FullSingleNoteResponse, NotesListResponse, PartialSingleNoteResponse
from src.constants.prompts.text_generation.notes.character_1 import SYSTEM_PROMPT, USER_PROMPT
from src.models.notes import NoteCollectionManager, NoteCollectionModel
from datetime import datetime
import ast
import uuid
from slugify import slugify
from nanoid import generate

class NotesMasterService:
    def __init__(self):
        self.text_generation_service = OpenAITextGenerationService()
        self.collection_manager = NoteCollectionManager()
        
    async def create_note(self, user_request: NoteCreationRequest):
        character_id = user_request.character_id
        topic = user_request.topic
        
        completion_config = dict()
        completion_config["model"] = "gpt-4o-mini"
        completion_config["messages"] = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": USER_PROMPT.format(topic=topic)
            }
        ]
        completion_config["response_format"] = {"type": "json_object"}
        
        llm_response = await self.text_generation_service.generate_text(completion_config)
        llm_response = ast.literal_eval(llm_response)
        
        note_creator = generate(size=1)
        note_slug = str(uuid.uuid4())[:8]
        
        note_instance = NoteCollectionModel(
            _id=generate(size=6),
            note_topic=user_request.topic,
            note_creator=note_creator,
            note_title=llm_response["note_title"],
            note_slug=f'{slugify(llm_response["note_title"])}_{note_slug}',
            note_text=llm_response["note_text"],
            note_created_at=datetime.now()
        )
        
        await self.collection_manager.create_note(note_instance)
        
        response = FullSingleNoteResponse(
            note_id=note_instance.note_id,
            note_slug=note_instance.note_slug,
            note_title=note_instance.note_title,
            note_text=note_instance.note_text,
            note_audio_url=note_instance.note_audio_url,
            note_created_at=note_instance.note_created_at,
            note_creator=note_instance.note_creator,
            note_topic=note_instance.note_topic
        )
        
        return response
    
    
    async def get_all_notes(self, limit: int, offset: int):
        notes_dicts = await self.collection_manager.get_all_notes(limit, offset)
        total_notes = await self.collection_manager.get_note_count()
        
        note_responses = []
        for note in notes_dicts:
            note['note_id'] = note.pop('_id')
            note_responses.append(PartialSingleNoteResponse.model_validate(note))
        
        response = NotesListResponse(
            total_notes=total_notes,
            limit=limit,
            offset=offset,
            has_next=offset + limit < total_notes,
            items=note_responses
        )
        
        return response
    
    async def get_note_by_id(self, note_id: str):
        note_dict = await self.collection_manager.get_note_by_id(note_id)
        if note_dict is None:
            return None
        
        note_dict['note_id'] = note_dict.pop('_id')
        
        response = FullSingleNoteResponse.model_validate(note_dict)
        
        return response