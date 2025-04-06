import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompt_parser import PromptLoader
from typing import Dict, Any, List, Optional, Union
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek
from pathlib import Path
import json
from decouple import config

# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

class LangchainClient:
    """LLM client implementation using Langchain"""
    
    def __init__(self, model_name='gemini-2.0-flash', temperature=0, prompts_path='output.json'):
        """
        Initialize LangchainClient with dynamic prompt loading
        
        Args:
            model_name: Name of the LLM model to use
            temperature: Temperature setting for generation
            prompts_path: Path to the JSON file containing parsed prompts
        """
        self.model_name = model_name
        self.temperature = temperature
        self.llm = self._create_llm()
        self.prompts_path = Path(prompts_path)
        self.prompt_loader = self._initialize_prompt_loader()
        self._prompts = self._load_prompts()  # Use private variable for storage
    
    def _initialize_prompt_loader(self) -> PromptLoader:
        """
        Initialize the PromptLoader with the specified prompts file
        
        Returns:
            PromptLoader instance for dynamic prompt template retrieval
        """
        return PromptLoader(self.prompts_path)
    
    def _load_prompts(self) -> List[Dict]:
        """
        Load and return prompts using the PromptLoader
        
        Returns:
            List of prompt dictionaries
        """
        return self.prompt_loader.prompts

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
                raise ValueError("API key required for Gemini models")
            return ChatGoogleGenerativeAI(
                temperature=self.temperature,
                model_name=self.model_name,
                model=self.model_name,
                google_api_key=api_key
            )
        elif 'deepseek' in self.model_name.lower():
            api_key = config("DEEPSEEK_API_KEY")
            if not api_key:
                raise ValueError("API key required for DeepSeek models")
            return ChatDeepSeek(
                temperature=self.temperature,
                model_name=self.model_name,
                api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")

    @property
    def prompts(self) -> List[Dict]:
        """Get the prompts."""
        return self._prompts

    @prompts.setter
    def prompts(self, value: List[Dict]):
        """Set prompts for the LangchainClient."""
        if not isinstance(value, List):
            raise ValueError("Prompts must be a list")
        for prompt in value:
            if not 'query' in prompt:
                raise ValueError("Each prompt must contain a 'query' key")
        self._prompts = value
        
    def get_prompt_by_title(self, title: str) -> Optional[Dict]:
        """
        Retrieve a prompt by its title using the PromptLoader.
        
        Args:
            title: The title of the prompt to retrieve
            
        Returns:
            The prompt dictionary or None if not found
        """
        return self.prompt_loader.get_prompt_by_title(title)
    
    def get_prompts_by_type(self, prompt_type: str) -> List[Dict]:
        """
        Retrieve all prompts of a specific type using the PromptLoader.
        
        Args:
            prompt_type: The type of prompts to retrieve
            
        Returns:
            List of prompt dictionaries matching the specified type
        """
        return self.prompt_loader.get_prompts_by_type(prompt_type)

    def create_chat_template(self, train_prompt_types=None, user_prompt=None):
        """
        Create a ChatPromptTemplate using the PromptLoader.
        
        Args:
            train_prompt_types: List of prompt types to include in the template
            user_prompt: Title of the user prompt to include
            
        Returns:
            A ChatPromptTemplate instance
        """
        if train_prompt_types is None:
            train_prompt_types = ["BACKGROUND-KNOWLEDGE", "DOMAIN", "EXAMPLE"]
            
        return self.prompt_loader.create_chat_prompt_template(
            train_prompt_types=train_prompt_types,
            user_prompt=user_prompt
        )
    
    def generate(self, user_prompt=None, train_prompt_types=None):
        """
        Generate a response using the LLM and dynamically created chat template.
        
        Args:
            user_prompt: Title of the user prompt to include
            train_prompt_types: List of prompt types to include in the template
            
        Returns:
            The model's response
        """
        chat_template = self.create_chat_template(
            train_prompt_types=train_prompt_types,
            user_prompt=user_prompt
        )
        
        # Format the messages from the template
        messages = chat_template.format_messages()
        
        # Get the response from the model
        response = self.llm(messages)
        
        return response

class LLMEvaluator:
    def __init__(self, client: LangchainClient):
        """
        Initialize LLMEvaluator with a LangchainClient instance
        Args:
            client: An instance of LangchainClient to interact with the LLM
        """
        self.client = client
        self.styling = "*" * 68
    
    def get_test_cases(self):
        return self.client.get_prompts_by_type("USER")

    def generate_test_results(self, file_path) -> str:
        """
        generate model responses on the test results of the model prompts.
        Args:
            prompt: The prompt string to evaluate
        """
        test_cases = self.get_test_cases()
        results = {}
        print(f"Found {len(test_cases)} test cases")

        for i in range(len(test_cases)):
            time.sleep(1)
            test_prompt = test_cases[i]['title']
            print(self.styling)
            print(f"Processing test case {i + 1} ({test_prompt}) of {len(test_cases)}."  +  "*".rjust(68 - len(f"Processing test case {i + 1} ({test_prompt}) of {len(test_cases)}.")))
            print(self.styling)
            time.sleep(0.5)
            print("Sending request to LLM.." +  "*".rjust(68 - len("Sending request to LLM..")))
            time.sleep(0.5)
            print(self.styling)
            response = self.client.generate(user_prompt=test_prompt).content
            print("Response generated for test prompt: \n\n")
            time.sleep(0.5)
            print(response)
            results[test_prompt] = {**test_cases[i], "response": response}
            time.sleep(0.5)
            print(f"Processing test case {i + 1} ({test_prompt}) of {len(test_cases)} completed successfully."  +  "*".rjust(68 - len(f"Processing test case {i + 1} ({test_prompt}) of {len(test_cases)} completed successfully.")))
            print(self.styling)
            print(34*" " + "|", 34*" " + "v", sep ='\n') 
            time.sleep(1)
        print(34*" " +"FINISHED OK.")
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=4)
        return results


# At the bottom of the file
if __name__ == "__main__":
    model_name = sys.argv[1]
    temerature = sys.argv[2]
    file_path = sys.argv[3]
    client = LangchainClient(model_name=model_name, temperature=temerature)
    model_evaluator = LLMEvaluator(client)
    model_evaluator.generate_test_results(file_path)
