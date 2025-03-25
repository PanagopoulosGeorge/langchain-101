from typing import Dict, Any, List, Optional, Union
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from pathlib import Path
import json
from decouple import config

class LangchainClient:
    """LLM client implementation using Langchain"""
    
    def __init__(self, model_name = 'gemini-2.0-flash', temperature = 0):
        """
        Initialize LangchainClient
        """
        self.model_name = model_name
        self.temperature = temperature
        self.llm = self._create_llm()
        self._prompts = self._load_prompts()  # Use private variable for storage
    
    def _load_prompts(self) -> Dict[str, Any]:
        """
        Load and return prompts for the LangchainClient.
        """
        prompts_path = Path('output.json')
        with prompts_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _create_llm(self):
        """Create Langchain LLM instance"""

        if 'ollama' in self.model_name.lower():
            return ChatOllama(
                temperature=self.temperature,
                model_name=self.model_name,
                model=self.model_name
            )
        elif 'gemini' in self.model_name.lower():
            api_key = config("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("API key required for OpenAI models")
            return ChatGoogleGenerativeAI(
                temperature=self.temperature,
                model_name=self.model_name,
                model=self.model_name,
                google_api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported model: {model_name}")
            
    def generate(self) -> List[Dict[str, Any]]:
        """Generate responses using Langchain"""
        responses = []
        total_input_tokens, total_output_tokens = 0, 0
        for prompt in self._prompts:
            prompt_template = PromptTemplate(template="{query}")
            chain = prompt_template | self.llm 
            response = chain.invoke({"query": prompt["query"]})
            prompt_response_consolidation = {**prompt, "response": response.content, "input_tokens": response.usage_metadata['input_tokens'],"output_tokens": response.usage_metadata['output_tokens']}
            total_input_tokens += response.usage_metadata['input_tokens']
            total_output_tokens += response.usage_metadata['output_tokens']
            responses.append(prompt_response_consolidation)
        return responses, total_input_tokens, total_output_tokens

    @property
    def prompts(self) -> List[Dict]:
        """Get the prompts."""
        return self._prompts

    @prompts.setter
    def prompts(self, value: List[Dict]):
        """Set prompts for the LangchainClient."""
        if not isinstance(value, List):
            raise ValueError("Prompts must be a dictionary")
        for prompt in value:
            if not 'query' in prompt:
                raise ValueError("Each prompt must contain a 'query' key")
        self._prompts = value

if __name__ == "__main__":
    client = LangchainClient(model_name="gemini-2.0-flash", temperature=0)
    prompts = [{"query": "What is the capital of France?"}, 
               {"query": "Explain the Markov property."}]
    client.prompts = prompts
    responses = client.generate()
    print(responses)