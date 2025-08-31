from langchain.chat_models import init_chat_model
import os
import getpass
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

chat_model = init_chat_model(model="llama3-8b-8192",
                model_provider="groq",
        )

def chatmodel(input: str) -> str:
    respone = chat_model.invoke(input=input)
    # print(respone)
    return respone.content