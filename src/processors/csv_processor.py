import csv
import io
from .base import FileProcessor

class CSVProcessor(FileProcessor):
    
    def validate_format(self, content: str):
        lines = [line for line in content.strip().split('\n') if line.strip()]
        if len(lines) < 2:
            raise ValueError("Invalid CSV format: Must contain a header row and at least one data row")
        if ',' not in lines[0]:
            raise ValueError("Invalid CSV format: Header must be comma-separated")
        

    def process(self, content: str) -> int:
        self.validate_content(content)
        
        f = io.StringIO(content.strip())
        reader = csv.reader(f)
        
        try:
            header = next(reader, None)
            if header is None:
                return 0
            
            count = sum(1 for row in reader if any(field.strip() for field in row))
            return count
        except Exception as e:
            raise ValueError(f"Invalid CSV: {str(e)}")
