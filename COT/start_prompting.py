import sys
from pathlib import Path
import json

# Add the src directory to Python path
src_path = Path(__file__).parent / 'src'
sys.path.append(str(src_path))

from llm_interface.langchain_client import LangchainClient

def main():
    client = LangchainClient(model_name="gemini-2.0-flash", temperature=0)
    
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