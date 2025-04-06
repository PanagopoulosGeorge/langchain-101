import sys
from pathlib import Path
import json
import os
from decouple import config
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

customer_review = """\
This leaf blower is pretty amazing.  It has four settings:\
candle blower, gentle breeze, windy city, and tornado. \
It arrived in two days, just in time for my wife's \
anniversary present. \
I think my wife liked it so much she was speechless. \
So far I've been the only one using it, and I've been \
using it every other morning to clear the leaves on our lawn. \
It's slightly more expensive than the other leaf blowers \
out there, but I think it's worth it for the extra features.
"""

review_template = """\
For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? \
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product \
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list.

Format the output as JSON with the following keys:
gift
delivery_days
price_value

text: {text}
"""
prompt_template = ChatPromptTemplate.from_template(review_template)

messages = prompt_template.format_messages(text=customer_review)

out = model(messages)

# out.content = out.content.replace('```','')
# out.content
# start_idx = out.content.index('{')
# end_idx = out.content.rindex('}') + 1
# print(out.content[start_idx:end_idx])

print(out.content)

from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

gift_schema = ResponseSchema(name="gift", description="A schema for parsing gift-related responses")
delivery_days_schema = ResponseSchema(name = 'delivery_days')
price_value_schema = ResponseSchema(name="price_value", description="A schema for parsing price-related responses")
response_schemas = [gift_schema, delivery_days_schema, price_value_schema]