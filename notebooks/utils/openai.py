from dotenv import load_dotenv, find_dotenv
import os
import asyncio
from langchain_openai import ChatOpenAI
from langchain.schema.messages import AIMessage, HumanMessage

class OpenAI:
    def __init__(self, instructions=""):
        load_dotenv(find_dotenv())
        self.cache = []
        self.instructions = instructions
        self.aiMessage = AIMessage(content=[{
                "type": "text",
                "text": instructions
            }])
        self.client = ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model_name="gpt-4o",
            model_kwargs={"top_p": 0, "seed": 42},
            temperature=0,
        )

    def addContext(self, context):
        self.aiMessage = AIMessage(content=[{
                "type": "text",
                "text": self.instructions
            }, *context])

    def clearContext(self):
        self.aiMessage = AIMessage(content=[{
            "type": "text",
            "text": self.instructions
        }])

    def request(self, prompt):        
        instructions = [self.aiMessage, HumanMessage(content=prompt)]
        response = self.client.invoke(instructions)
        self.cache.append(response)
        return response.content

    def requestXTimes(self, prompt, times=3):
        prompt_chain = list(map(lambda i: self.request(prompt), range(times)))
        return asyncio.gather(*prompt_chain)

