import os
import requests
from decouple import config


def scrape_linkedin_profile(url: str, mock: bool = True):
    """
    scrape information from linkedIn profiles, Manually scrape the information from a linkedIn profile.
    """
    if mock:
        url = "https://gist.githubusercontent.com/PanagopoulosGeorge/daf1d7e7ba47b40b1fb518a9854aeea8/raw/8a1adeb04aaca387b658e22180b99586c73163b8/linkedin_profile_data.json"
        response = requests.get(url,
                                timeout = 10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {"linkedInUrl": url, 
                  "apikey": config("SCRAPIN_API_KEY")}
        response = requests.get(api_endpoint,
                                params=params,
                                timeout = 10)
    data = response.json().get("person")
    data = {
        k:v for k, v in data.items() 
        if v not in (None, "", [], {}) and 
           k not in ["certifications"]
    }
    return data

if __name__ == "__main__":
    print(scrape_linkedin_profile("https://gr.linkedin.com/in/george-panagopoulos-7282171b0", mock=False))