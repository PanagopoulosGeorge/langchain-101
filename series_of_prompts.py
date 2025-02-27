from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from decouple import config
prompts = [
    "What is the capital of France?",
    "Explain what martingales are.",
    "Summarize the principles of risk management."
]

def create_prompt_template(template_str):
    return PromptTemplate(template=template_str)

def create_llm(model_name, temperature=0):
    if model_name == "llama3.2":
        return ChatOllama(temperature=temperature, model_name=model_name, model=model_name)
    elif model_name == "gpt-3.5-turbo":
        OPENAI_KEY = config('OPENAI_API_KEY')
        return ChatOpenAI(temperature=temperature, model_name=model_name, api_key=OPENAI_KEY)
    else:
        raise ValueError(f"Unsupported model: {model_name}")

def get_responses(prompts, llms):
    responses = {}
    for model_name, model in llms.items():
        if model_name not in responses:
            responses[model_name] = {}
        for i, prompt in enumerate(prompts):
            chain = create_prompt_template("{query}") | model
            response = chain.invoke({"query": prompt})
            responses[model_name][f"Prompt {i+1}"] = response.content
    return responses

def print_responses(responses):
    for model, results in responses.items():
        print(f"\nModel: {model}")
        for prompt, response in results.items():
            print(f"{prompt}: {response}\n")

if __name__ == "__main__":
    llms = {
        "llama3.2": create_llm("llama3.2"),
    }

    responses = get_responses(prompts, llms)
    print_responses(responses)