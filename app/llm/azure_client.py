import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load .env variables
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def chat_completion(messages: list[str]) -> str:
    """
    Sends messages to Azure OpenAI and returns the response text.
    """
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "user", "content": msg} for msg in messages
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
