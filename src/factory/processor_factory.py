import threading
from src.processors.csv_processor import CSVProcessor
from src.processors.json_processor import JSONProcessor
from src.processors.xml_processor import XMLProcessor

class ProcessorFactory:
    
    _processor_classes = {
        'csv': CSVProcessor,
        'json': JSONProcessor,
        'xml': XMLProcessor
    }
    
    _instances = {}
    _lock = threading.Lock()
    
    @classmethod
    def get_processor(cls, file_type: str):
        file_type = file_type.lower()
        
        if file_type not in cls._instances:
            with cls._lock:
                if file_type not in cls._instances:
                    processor_class = cls._processor_classes.get(file_type)
                    if not processor_class:
                        raise ValueError(f"Unsupported file type : {file_type} is not supported")
                    cls._instances[file_type] = processor_class()
            
        return cls._instances[file_type]
