
#  Automating RTEC Prompting

  

A Python module for interacting with Large Language Models (LLMs) using LangChain. This module currently supports Google's Gemini and Ollama models, providing a simple interface for generating responses to prompts.

  ## Overview
  This prototype aims to automate the process of interacting with LLMs using structured prompts in the RTEC format. Given a document containing a series of structured prompts, that are categorized in the following section, the main task is to programmatically prompt this series to a specified LLM for generating responses, extracting the answers that will be then validated against the ground truth (simLP). The system handles both training prompts and testing prompts for maritime situational awareness (MSA) scenarios.

-   Maritime Situational Awareness (MSA)

## Categorization (will be useful for later on)
There are 4 main categories used when trying to characterize a prompt:
1. System
2. User
3. Assistant
4. Example

see config/prompt_styles.py for reference.

## Features

  

- Support for multiple LLM providers:

	- Google Gemini
	- Ollama
	- GPT (needs api key)

- Token usage tracking

- Simple prompt management.

  

## Installation

  

1. Clone this repository

2. Install the required dependencies:

```bash

pip  install  -r requirements.txt

```
## How to execute
1.   Copy the original document file containing the prompts within the COT directory. 
2. setup the environment variables: within COT directory, create an env file containing the following variables:

    - GEMINI_API_KEY=<your-gemini-api-key>
	- OPENAI_API_KEY=<your-openai-api-key>
    - TAVILY_API_KEY=<your-tavily-api-key> 			# if you want to execute the example within misc	
    - SCRAPIN_API_KEY=<your-scrapin-api-key> 		# if you want to execute the example  within misc
    - LANGSMITH_TRACING=true                        # These three environment variables are required for prompt tracing
    - LANGSMITH_API_KEY=<your-langsmith-api-key>
	- LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
3. within this directory execute: 
```bash
python -m src.prompt_processor.doc_parser <name_of_the_file>.docx
```
4. if a file name output.json is created within the same directory, containing the prompts serialized, you can then execute:
```bash
python start_prompting.py
```

  

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

  

-  `model_name`: The name of the LLM model to use (default: 'gemini-2.0-flash')

-  `temperature`: Controls the randomness of the output (default: 0)

- 0: More focused and deterministic

- 1: More creative and varied