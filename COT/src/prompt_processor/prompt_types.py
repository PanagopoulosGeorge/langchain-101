from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class PromptType(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    EXAMPLE = "EXAMPLE"

@dataclass
class Prompt:
    """Represents a single prompt in the training sequence"""
    title: str
    query: str
    prompt_type: PromptType
    sequence_id: int
    dependencies: Optional[List[int]] = None  # IDs of prompts that must come before this one

    def to_dict(self) -> Dict[str, Any]:
        """Convert prompt to dictionary format"""
        return {
            "title": self.title,
            "query": self.query,
            "prompt_type": self.prompt_type.value,
            "sequence_id": self.sequence_id,
            "dependencies": self.dependencies
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Prompt':
        """Create a Prompt instance from dictionary data"""
        return cls(
            title=data["title"],
            query=data["query"],
            prompt_type=PromptType(data["prompt_type"]),
            sequence_id=data["sequence_id"],
            dependencies=data.get("dependencies")
        )