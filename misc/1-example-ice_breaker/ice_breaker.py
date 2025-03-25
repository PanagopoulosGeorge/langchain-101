from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from decouple import config
from third_parties.linkedIn import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parser import summary_parser, Summary
from typing import Tuple
from decouple import config
from langchain_google_genai import ChatGoogleGenerativeAI
GEMINI_API_KEY = config("GEMINI_API_KEY", default="")
import os
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGSMITH_ENDPOINT'] = config("LANGSMITH_ENDPOINT", default="")
os.environ['LANGSMITH_API_KEY'] = config("LANGSMITH_API_KEY", default="")
os.environ['LANGSMITH_PROJECT'] = 'llm-repro'
def ice_break_with(name: str) -> Tuple:
    linkedin_username = linkedin_lookup_agent(name = name)
    # linkedin_username = "https://www.linkedin.com/in/george-panagopoulos-7282171b0/"
    try:
        url = linkedin_username[linkedin_username.index('http'):].strip('.')
    except ValueError:
        print("No valid LinkedIn URL found.")
        return "No valid LinkedIn URL found."
    print("Url found: ", url)
    linkedin_data = scrape_linkedin_profile(url=url, mock = False)
    summary_template = \
        """
        given the LinkedIn information "{info} LinkedIn", please produce a small descriptive summary of that person.
        """ 
    summary_prompe_template = PromptTemplate(input_variables=["info"], 
                                                template=summary_template,    
                                            )
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

    # chain = summary_prompe_template | llm
    chain = summary_prompe_template | llm
    res = chain.invoke({"info": linkedin_data})
    return res.content,  linkedin_data.get('photoUrl')

if __name__ == "__main__":
    print("🚀 Ice Breaker Application 🚀")
    print("")
    print("This app helps you generate a quick summary and interesting facts about professionals based on their LinkedIn profiles.")
    print("Simply enter a name, and we'll fetch insights to help you start a conversation!")
    print("")
    
    # search_name = str(input("Enter the name to search on LinkedIn: "))   
    summary = ice_break_with('George Panagopoulos Netcompany')
    print(summary)