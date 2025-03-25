"""Configuration for document style mappings."""
from ..prompt_processor.prompt_types import PromptType

STYLE_MAPPING = {
    # Basic styles
    'RTEC'     : PromptType.SYSTEM,
    'MSA'      : PromptType.SYSTEM,
    'MSA-R'    : PromptType.USER,
    'NOT USED' : PromptType.ASSISTANT,
    'RTEC-S'   : PromptType.EXAMPLE,
    
    # # Common variations
    # 'system prompt': PromptType.SYSTEM,
    # 'user prompt': PromptType.USER,
    # 'assistant response': PromptType.ASSISTANT,
    # 'example prompt': PromptType.EXAMPLE,
    
    # # Additional styles can be added here
    # 'question': PromptType.USER,
    # 'answer': PromptType.ASSISTANT,
    # 'instruction': PromptType.SYSTEM,
    # 'sample': PromptType.EXAMPLE,
}