from abc import ABC, abstractmethod

class BaseTextGenerationService(ABC):
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass


    @abstractmethod
    def generate_text_stream(self, prompt: str):
        pass