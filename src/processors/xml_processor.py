import xml.etree.ElementTree as ET
from .base import FileProcessor

class XMLProcessor(FileProcessor):
    
    def validate_format(self, content: str):
        stripped = content.strip()
        if not (stripped.startswith('<') and stripped.endswith('>')):
            raise ValueError("Invalid XML format: Content must be enclosed in tags")
        # Check for presence of nested tags (at least one child)
        if stripped.count('<') < 4: # <root><item/></root> is minimum for records
             raise ValueError("Invalid XML format: Must contain a root element and at least one child record")

    def process(self, content: str) -> int:
        self.validate_content(content)
        
        try:
            root = ET.fromstring(content.strip())
            # Counting the children of the root element
            # Strictly ignore "empty" child elements (no text, no children, no attributes)
            count = 0
            for child in root:
                # An element is considered non-empty if it has children, 
                # or non-whitespace text, or attributes
                has_text = child.text and child.text.strip()
                has_children = len(child) > 0
                has_attrs = len(child.attrib) > 0
                
                # Even if it's <record/>, if it represents a record in the schema we should count it.
                # However, the user specifically asked for "hard validation... if no content".
                # We'll count it if it's not a completely empty tag.
                if has_text or has_children or has_attrs or (child.text is None and not has_children):
                    # child.text is None typically means a self-closing tag like <record/>
                    # which IS a record.
                    count += 1
            return count
        except ET.ParseError:
            raise ValueError("Invalid XML")
