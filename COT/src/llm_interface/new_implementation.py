
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain_google_genai import ChatGoogleGenerativeAI

from decouple import config
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

"""
chat_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

"""
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                              model_name="gemini-2.0-flash",
                              temperature=0,
                              google_api_key=config("GEMINI_API_KEY"),
                              verbose=True,
                              )

memory = ConversationBufferMemory()
conversation = ConversationChain(memory=memory, llm=model, verbose = True)


def invoke_chat_template(chat_template, model):
    """
    Invokes a chat template with the given model
    
    Args:
        chat_template: ChatPromptTemplate object containing the messages
        model: Language model to use for generation
    
    Returns:
        The model's response
    """
    # Format the messages from the template
    messages = chat_template.format_messages()
    
    # Get the response from the model
    response = model(messages)
    
    return response


def invoke_chat_template_show_conversation(chat_template, model):
    """
    Invokes a chat template with the given model
    
    Args:
        chat_template: ChatPromptTemplate object containing the messages
        model: Language model to use for generation
    
    Returns:
        The model's response
    """
    history_prompts = chat_template[:-1]
    users_prompt = chat_template[-1].prompt.template
    chat_llm_chain = LLMChain(
    llm = model,
    prompt = history_prompts,
    verbose = True,
    memory = memory,
    )
    return chat_llm_chain.predict(human_input = users_prompt)

