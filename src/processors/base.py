from abc import ABC, abstractmethod

class FileProcessor(ABC):
    
    @abstractmethod
    def process(self, content: str) -> int:
        pass

    def validate_content(self, content: str):
        if not content or not content.strip():
            raise ValueError("File content cannot be empty")
        self.validate_format(content)

    @abstractmethod
    def validate_format(self, content: str):
        """Validate if the content matches the expected format."""
        pass
