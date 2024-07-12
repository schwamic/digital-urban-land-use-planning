from dotenv import load_dotenv, find_dotenv
import os
import asyncio
from langchain_openai import ChatOpenAI
from langchain.schema.messages import AIMessage, HumanMessage
from utils.parser import Parser

class OpenAI:
    def __init__(self, instructions=""):
        load_dotenv(find_dotenv())
        self.cache = []
        self.parser = Parser()
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

    def requestWithContext(self, context, prompt):
        self.addContext(context)
        response = self.request(prompt)
        self.clearContext()
        return response

    async def requestXTimes(self, prompt, times=3):
        prompt_chain = list(map(lambda i: self.request(prompt), range(times)))
        return await asyncio.gather(*prompt_chain)

    async def extractTextFromImage(self, instruction, img_path, img_type="png"):
        if img_type == "pdf":
            prompts = self.parser.pdf2prompts(img_path)
        else:
            img_prompt = self.parser.image2prompt(img_path)
            prompts = [img_prompt]
        message = self.request([
            *prompts,
            {
                "type": "text",
                "text": instruction,
            },
        ])
        return message

    async def extractTextFromImages(self, instruction, img_paths, img_type="png"):
        requests = list(map(lambda img_path: self.extractTextFromImage(instruction, img_path, img_type), img_paths))
        return await asyncio.gather(*requests)

    async def extractTextFromImagesWithContexts(self, instruction, img_paths, contexts, img_type="png"):
        messages = []
        for index, img_path in enumerate(img_paths):
            context = contexts[index] if type(contexts[index]) == list else [contexts[index]]
            self.addContext(context)
            msg = await self.extractTextFromImage(instruction, img_path, img_type)
            messages.append(msg)
            self.clearContext()
        return messages

    def extractTextFromFilteredPrompts(self, pages, prompts, instruction, context):
        filtered_prompts = list(map(lambda page: prompts[page-1], pages))
        return self.requestWithContext(context, [
            *filtered_prompts,
            {
                "type": "text",
                "text": instruction
            },
        ])
