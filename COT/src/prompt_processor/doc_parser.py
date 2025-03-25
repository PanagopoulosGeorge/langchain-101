from pathlib import Path
from typing import List, Dict, Optional
import docx
import re
import sys
from ..config.prompt_styles import STYLE_MAPPING
from .prompt_types import Prompt, PromptType
import json

class DocumentParser:
    """Parses Word documents containing training prompts"""
    
    def __init__(self, file_path: str, prompt_header: str = 'Prompt', prompt_header_period: str = ':'):
        self.file_path = Path(file_path)
        self._validate_file()
        self.prompt_header = prompt_header
        self.prompt_header_period = prompt_header_period
        
    def _validate_file(self) -> None:
        """Validates that the file exists and is a .docx file"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if self.file_path.suffix != '.docx':
            raise ValueError(f"File must be a .docx file, got: {self.file_path.suffix}")

    
    def _determine_prompt_type(self, header) -> Optional[PromptType]:
        """Determines the type of prompt based on paragraph style and content"""
        # Map common style names to prompt types
        style_mapping = STYLE_MAPPING
        type = None
        # Check style name
        for key, prompt_type in style_mapping.items():
            if key in header:
                type = prompt_type            
        # Fallback: Check content for indicators
        if header.startswith('system:'):
            return PromptType.SYSTEM
        elif header.startswith('user:'):
            return PromptType.USER
        elif header.startswith('assistant:'):
            return PromptType.ASSISTANT
        elif header.startswith('example:'):
            return PromptType.EXAMPLE
            
        return type
    
    def parse(self) -> List[Prompt]:
        """Parses the document and returns a list of Prompt objects."""
        doc = docx.Document(self.file_path)
        sequence = []
        current_prompt = None
        sequence_id = 0
        i = 0
        for paragraph in doc.paragraphs:
            i +=1
            text = paragraph.text.strip()
            if not text:
                continue
                
            # Check for prompt markers
            if text.startswith(self.prompt_header) and text.endswith(self.prompt_header_period):
                # Save previous sequence if it exists
                if current_prompt:
                    sequence.append(current_prompt)
                
                # Determine prompt type
                prompt_type = self._determine_prompt_type(text)
                if not prompt_type:
                    prompt_type = PromptType.USER
                
                current_prompt = Prompt(
                    title=text.replace(self.prompt_header, '').replace(self.prompt_header_period, '').strip(),
                    query = '',
                    prompt_type=prompt_type,
                    sequence_id=sequence_id
                )
                sequence_id += 1
                continue
            if current_prompt:
                current_prompt.query +=  '\n' + text.strip() if current_prompt.query != '' else text.strip()

        return sequence

    def to_json(self, sequence):
        return [prompt.to_dict() for prompt in sequence]
    
    def save_json(self, list_of_dicts, out_file):
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(list_of_dicts, f, indent=4)
            
if __name__ == "__main__":
    file_path = sys.argv[1]
    parser = DocumentParser(file_path)
    parsed_sequence = parser.parse()
    list_of_dicts = parser.to_json(parsed_sequence)
    parser.save_json(list_of_dicts, "output.json")
