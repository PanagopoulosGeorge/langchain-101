from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from decouple import config
from tools.tools import get_profile_url_tavily

GEMINI_API_KEY = config("GEMINI_API_KEY", default="")
def lookup(name: str):
    """
    Lookup a LinkedIn profile URL given the person's name.

    Parameters:
    -----------
    name : str
        The person's name for which to find the LinkedIn profile URL.

    Returns:
    --------
    str
        The LinkedIn profile URL if found, otherwise an empty string
        or an error message.
    """
    # llm = ChatOllama(temperature = 0.2,
    #                  model_name = "olmo2:13b",
    #                  model = "olmo2:13b")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

    template = """
        Your task is to find the LinkedIn profile of a given person.  

        - Perform a Google search using "{name} LinkedIn".  
        - Extract **only the first valid LinkedIn profile URL** from the results.  
        - If no profile is found, return "No LinkedIn profile found."  
    """


    prompt_template = PromptTemplate(
        input_variables = ["name"],
        template = template
    )

    tools_for_agent = [
        Tool(name = "Crawl Google 4 linkedin profile page",
             func= get_profile_url_tavily,
             description="Useful for finding LinkedIn profile URLs via Google search.")
    ]

    react_prompt = hub.pull("hwchase17/react")
    ###############################################  % introduce agent % #################################################
    agent = create_react_agent(llm = llm,
                                tools = tools_for_agent,
                                prompt = react_prompt)
    
    agent_executor = AgentExecutor(agent = agent, tools = tools_for_agent, verbose=True, handle_parsing_errors=True)
    #####################################################################################################################
    res = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name = name)}
    )
    linkedin_url = res['output']
    return linkedin_url


if __name__ == "__main__":
    linkedin_url = lookup("George Panagopoulos")
    print("Answer is: ", linkedin_url)