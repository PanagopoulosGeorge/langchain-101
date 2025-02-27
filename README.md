## Prompt Template

### Understanding Prompts

Large Language Models (LLMs) process input known as prompts, which serve as queries to generate responses. 

#### Example Prompt

```
I want you to write a cool, funny jingle for a {product} product.

The jingle should be 1 sentence.

product = cat food
```

#### Generated Output

```
🎶 "For purrs so loud and tails so spry, [Brand Name] cat food—one bite, they fly!" 🎶 😺✨
```

#### Challenge: Parameterizing Prompts

What if we want to use programmatic access to LLMs and dynamically pass parameters into the prompt?

#### Example with Parameterization

```
I want you to write a cool, funny jingle for a {product} product.

The jingle should be 1 sentence.

product = Sports shoes
```

#### Parameter:

- product = Sports shoes

#### Generated Output

```
🎶 "Run so fast, you'll leave your shadow behind—[Brand Name] sports shoes, speed redefined!" 🏃‍♂️💨
```

**Prompt templates** help to translate user input and parameters into instructions for a language model. This can be used to guide a model's response, helping it understand the context and generate relevant and coherent language-based output.

```py
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

prompt_template.invoke({"topic": "cats"})
```

## ChatPromptTemplates

These prompt templates are used to format a list of messages. These "templates" consist of a list of templates themselves. For example, a common way to construct and use a ChatPromptTemplate is as follows:

```py
from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])

prompt_template.invoke({"topic": "cats"})
```



[->] [Chat Models](./docs/chat-models.md)

