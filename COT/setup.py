from setuptools import setup, find_packages

setup(
    name="rtec-prompt-processor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-docx>=0.8.11",
        "networkx>=2.5",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A system for processing RTEC prompts from documents",
    keywords="rtec, nlp, prompt-engineering",
    python_requires=">=3.7",
)