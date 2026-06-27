import json
from .base import FileProcessor

class JSONProcessor(FileProcessor):
    
    def validate_format(self, content: str):
        stripped = content.strip()
        if not (stripped.startswith('[') and stripped.endswith(']')):
            raise ValueError("Invalid JSON format: Content must be a JSON array (starting with '[' and ending with ']')")

    def process(self, content: str) -> int:
        self.validate_content(content)
        
        try:
            data = json.loads(content)
            
            if not isinstance(data, list):
                # If it's a single object, we only count it if it's not empty
                return 1 if (isinstance(data, dict) and data) else 0
                
            # Count elements that are not empty dictionaries or whitespace-only strings
            count = 0
            for item in data:
                if isinstance(item, dict):
                    if item: # Ignore empty dictionaries {}
                        count += 1
                elif isinstance(item, str):
                    if item.strip(): # Ignore whitespace strings " "
                        count += 1
                elif item is not None:
                    count += 1
            return count
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON")
