from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from decouple import config
## Information about a Elon as found in wikipedia

info = \
"""
Elon Reeve Musk (/ˈiːlɒn mʌsk/; born June 28, 1971) is a businessman known for his key roles in Tesla, Inc., SpaceX, and Twitter (which he rebranded as X). Since 2025, he has been a senior advisor to United States President Donald Trump and head of the Department of Government Efficiency (DOGE). Musk is the wealthiest person in the world; as of February 2025, Forbes estimates his net worth to be US$384 billion.

Born to a prominent family in Pretoria, South Africa, Musk emigrated to Canada in 1989 and acquired its citizenship via his mother. He moved to the U.S. and studied at the University of Pennsylvania before moving to California to pursue business ventures, and in 1995 co-founded the software company Zip2. After its sale in 1999, he co-founded X.com, an online payment company which later became PayPal, which was acquired by eBay in 2002 for $1.5 billion. In 2002, Musk also became a U.S. citizen.

In 2002, Musk founded SpaceX and became its CEO and chief engineer. The company has since led innovations in reusable rockets and commercial spaceflight. In 2004, Musk joined Tesla, Inc., as an early investor, and became its CEO and product architect in 2008; it has become a market leader in electric vehicles. In 2015, he co-founded OpenAI to advance artificial intelligence research, but left its board in 2018. In 2016, Musk co-founded Neuralink, a company focused on brain–computer interfaces, and in 2017 launched the Boring Company, which aims to develop tunnel transportation. Musk was named Time magazine's Person of the Year in 2021. In 2022, he acquired Twitter, implementing significant changes and rebranding it as X in 2023. In January 2025, he was appointed head of Trump's newly created DOGE.

Musk's political activities and views have made him a polarizing figure. He has been criticized for making unscientific and misleading statements, including COVID-19 misinformation, affirming antisemitic and transphobic comments, and promoting conspiracy theories. His acquisition of Twitter was controversial due to a subsequent increase in hate speech and the spread of misinformation on the service. Musk has engaged in political activities in several countries, including as a vocal and financial supporter of Trump. Musk was the largest donor in the 2024 U.S. presidential election and is a supporter of far-right figures, causes, and political parties.
"""

if __name__ == "__main__":
    print("Welcome to Ice Breaker! Let's get started.")
    summary_template = \
    """
    given the information {info}, about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
    """ 
    summary_prompt_template = PromptTemplate(
                              input_variables=["info"],
                              template=summary_template)
    
    # llm = ChatOpenAI(temperature=0,                ## Determines how creative the model should be
    #                                                ## 0 is the most conservative and 1 is the most creative
    #                  model_name = "gpt-3.5-turbo",
    #                  api_key=OPENAI_KEY
    #                 )

    llm = ChatOllama(temperature=0,                ## Determines how creative the model should be
                                                   ## 0 is the most conservative and 1 is the most creative
                     model_name = "llama3.2",
                     model="llama3.2"
                    )
    chain = summary_prompt_template | llm

    res = chain.invoke(input={"info": info}).content
    print(res)