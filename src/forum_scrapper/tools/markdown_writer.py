from crewai_tools import BaseTool
import hashlib
from datetime import datetime
from typing import Any, Type, Optional
from pydantic import BaseModel

# Schema definition for tool input arguments
class MarkdownWriterToolSchema(BaseModel):
    content: str  # Required content to be written to the file
    file_name: Optional[str] = None  # Optional: The name of the file to create

class MarkdownWriterTool(BaseTool):
    name: str = "MarkdownWriterTool"
    description: str = "A tool to write formatted markdown content to a file."
    args_schema: Type[BaseModel] = MarkdownWriterToolSchema  # Use the schema for input validation

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def _run(self, **kwargs: Any) -> str:
        # Validate inputs against the schema
        inputs = self.args_schema(**kwargs)

        content = inputs.content  # Extract content from validated input
        file_name = inputs.file_name

        if not content:
            raise ValueError("No content provided to write to the markdown file.")

        # Generate a dynamic filename if not provided
        if not file_name:
            # Use a timestamp or a hash to create a unique file name
            hash_object = hashlib.md5(content.encode())
            file_hash = hash_object.hexdigest()[:8]  # First 8 chars of the hash
            file_name = f"discussion_{file_hash}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        try:
            # Write the content to the specified markdown file
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(content)
            return f"Markdown content successfully written to {file_name}."
        except Exception as e:
            raise RuntimeError(f"Failed to write markdown content to file: {str(e)}")
