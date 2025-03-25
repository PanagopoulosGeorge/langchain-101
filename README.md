# Chain of Thought (COT) Module

A Python module for interacting with Large Language Models (LLMs) using LangChain. This module currently supports Google's Gemini and Ollama models, providing a simple interface for generating responses to prompts.

## Features

- Support for multiple LLM providers:
  - Google Gemini
  - Ollama
- Token usage tracking
- Simple prompt management
- JSON-based response storage

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install langchain-core langchain-openai langchain-ollama langchain-google-genai python-decouple
```

3. Set up your environment variables:
   - For Gemini: Set `GEMINI_API_KEY` in your environment or `.env` file

## Basic Example

Here's a simple example demonstrating how to use the LangchainClient:

```python
from llm_interface.langchain_client import LangchainClient

# Initialize the client with Gemini model
client = LangchainClient(model_name="gemini-2.0-flash", temperature=0)

# Define your prompts
prompts = [
    {"query": "What is the capital of France?"},
    {"query": "Explain quantum computing in simple terms."}
]

# Set the prompts
client.prompts = prompts

# Generate responses
responses, input_tokens, output_tokens = client.generate()

# Print the responses
for response in responses:
    print(f"\nQuery: {response['query']}")
    print(f"Response: {response['response']}")
    print(f"Input tokens: {response['input_tokens']}")
    print(f"Output tokens: {response['output_tokens']}")

print(f"\nTotal input tokens: {input_tokens}")
print(f"Total output tokens: {output_tokens}")
```

Expected output:
```
Query: What is the capital of France?
Response: The capital of France is Paris.
Input tokens: 7
Output tokens: 8

Query: Explain quantum computing in simple terms.
Response: Quantum computing is a type of computing that uses quantum mechanics to process information. Unlike classical computers that use bits (0s and 1s), quantum computers use quantum bits or qubits, which can exist in multiple states at once. This allows quantum computers to solve certain complex problems much faster than traditional computers.
Input tokens: 9
Output tokens: 45

Total input tokens: 16
Total output tokens: 53
```

## Configuration

The LangchainClient can be configured with the following parameters:

- `model_name`: The name of the LLM model to use (default: 'gemini-2.0-flash')
- `temperature`: Controls the randomness of the output (default: 0)
  - 0: More focused and deterministic
  - 1: More creative and varied

## Input Format

Prompts should be provided as a list of dictionaries, where each dictionary must contain a 'query' key:

```python
prompts = [
    {"query": "Your first question here"},
    {"query": "Your second question here"}
]
```

## Response Format

The `generate()` method returns a tuple containing:
1. A list of response dictionaries, each containing:
   - Original query
   - Generated response
   - Input token count
   - Output token count
2. Total input tokens
3. Total output tokens

## Error Handling

The module includes error handling for:
- Invalid API keys
- Unsupported models
- Incorrect prompt format
- Missing query keys in prompts

## Limitations

- Currently supports only Gemini and Ollama models
- Requires appropriate API keys for each service
- Input prompts must be in JSON format with a 'query' field

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.