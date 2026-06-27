import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.factory.processor_factory import ProcessorFactory

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s' 
)
logger = logging.getLogger(__name__)

def process_file(file_type, file_content):
    
    try:
        processor = ProcessorFactory.get_processor(file_type)
        count = processor.process(file_content)
        return {"record_count": count}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise ValueError(f"Error processing {file_type} file: {str(e)}")

if __name__ == "__main__":
    
    csv_data = "id,name\n1,John\n2,Mary"
    json_data = '[{"id":1}, {"id":2}]'
    xml_data = '<root><record>1</record><record>2</record></root>'
    
    try:
        res_csv = process_file('csv', csv_data)
        logger.info(f"CSV Result: {res_csv}")
        
        res_json = process_file('json', json_data)
        logger.info(f"JSON Result: {res_json}")
        
        res_xml = process_file('xml', xml_data)
        logger.info(f"XML Result: {res_xml}")
    except Exception as e:
        logger.error(f"Execution failed: {e}")
