import pytest
from src.main import process_file
from src.factory.processor_factory import ProcessorFactory

def test_csv_processing_valid():
    content = "id,name\n1,John\n2,Mary"
    result = process_file('csv', content)
    assert result == {"record_count": 2}

def test_json_processing_valid():
    content = '[{"id":1}, {"id":2}]'
    result = process_file('json', content)
    assert result == {"record_count": 2}

def test_xml_processing_valid():
    content = '<root><record/><record/></root>'
    result = process_file('xml', content)
    assert result == {"record_count": 2}


def test_unsupported_file_type():
    with pytest.raises(ValueError, match="is not supported"):
        process_file('yaml', 'key: value')

def test_empty_content_csv():
    with pytest.raises(ValueError, match="File content cannot be empty"):
        process_file('csv', '')

def test_empty_content_json():
    with pytest.raises(ValueError, match="File content cannot be empty"):
        process_file('json', '  ')


def test_malformed_json():
    with pytest.raises(ValueError, match="Invalid JSON"):
        process_file('json', '[{"id":1}, {"id":2}') 

def test_malformed_xml():
    with pytest.raises(ValueError, match="Invalid XML"):
        process_file('xml', '<root><record/><record>') 

def test_csv_only_header():
    content = "id,name"
    with pytest.raises(ValueError, match="Must contain a header row and at least one data row"):
        process_file('csv', content)

def test_csv_empty_rows():
    content = "id,name\n1,John\n\n2,Mary\n  \n"
    result = process_file('csv', content)
    assert result == {"record_count": 2}

def test_csv_invalid_format():
    with pytest.raises(ValueError, match="Invalid CSV"):
        process_file('csv', 'just some text without commas')

def test_json_invalid_format():
    with pytest.raises(ValueError, match="Invalid JSON"):
        process_file('json', 'id: 1, name: John') 

def test_xml_invalid_format():
    with pytest.raises(ValueError, match="Invalid XML"):
        process_file('xml', 'root record /root') 

def test_csv_whitespace_rows():
    content = "id,name\n1,John\n   ,   \n2,Mary\n\n"
    result = process_file('csv', content)
    assert result == {"record_count": 2}

def test_json_empty_elements():
    content = '[{"id":1}, {}, {"id":2}, " ", null]'
    result = process_file('json', content)
    assert result == {"record_count": 2}

def test_xml_empty_elements():
    content = '<root><record>1</record><record>  </record><record>2</record></root>'
    result = process_file('xml', content)
    assert result == {"record_count": 2}

def test_factory_singleton():
    p1 = ProcessorFactory.get_processor('csv')
    p2 = ProcessorFactory.get_processor('csv')
    assert p1 is p2

def test_process_file_unexpected_exception(mocker):
    # Mock ProcessorFactory.get_processor to return something that fails
    # This hits the 'except Exception' block in main.py
    from src.factory.processor_factory import ProcessorFactory
    mocker.patch.object(ProcessorFactory, 'get_processor', side_effect=Exception("Simulated error"))
    
    with pytest.raises(ValueError, match="Error processing csv file"):
        process_file('csv', "some content")
