import sys
from pathlib import Path
import json
import os
from decouple import config
# Add the src directory to Python path
src_path = Path(__file__).parent / 'src'
sys.path.append(str(src_path))

from llm_interface.langchain_client import LLMClient

def main():
    client = LLMClient(model_name="gemini-2.0-flash", temperature=0)
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGSMITH_ENDPOINT'] = config("LANGSMITH_ENDPOINT", default="")
    os.environ['LANGSMITH_API_KEY'] = config("LANGSMITH_API_KEY", default="")
    os.environ['LANGSMITH_PROJECT'] = client.model_name
    # Define your prompts
    prompts = [
        {"query": "What is the capital of France?"},
        {"query": "Explain quantum computing in simple terms."},
        {"query": "What are the main principles of machine learning?"}
    ]
    
    # Set the prompts, if no prompts set, then prompts that will be used are from output.json.
    # client.prompts = prompts
    
    # Generate responses
    responses, input_tokens, output_tokens = client.generate()
    
    # Save to responses.json
    with open('responses.json', 'w', encoding='utf-8') as f:
        json.dump(responses, f, indent=4, ensure_ascii=False)
    
    print(f"Responses saved to responses.json")
    print(f"Total input tokens: {input_tokens}")
    print(f"Total output tokens: {output_tokens}")

if __name__ == "__main__":
    main()