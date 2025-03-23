from tavily import TavilyClient
from decouple import config
TAVILY_API_KEY = config("TAVILY_API_KEY")
def get_profile_url_tavily(name: str):
    """
    Searches for LinkedIn or Twitter Profile Page.
    """
    client = TavilyClient(TAVILY_API_KEY)
    res = client.search(query = f"{name}")
    return res

if __name__ == "__main__":
    print(get_profile_url_tavily("Eden Marco Udemy"))