from dotenv import load_dotenv, find_dotenv
from dotmap import DotMap
import os
import asyncio
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema.messages import AIMessage, HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
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
        self.clientEmbeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-large",
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

    '''Utility/Workaround to call request() in a lamda function in combination with asyncio
    @param: list: prompts
    @return: str: message
    '''
    async def lambdaRequest(self, prompts):
        return self.request(prompts)

    '''Utility to extract text from an image or pdf
    @param: str: instruction
    @param: str: img_path
    @return: str: message
    '''
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

    '''Utility to extract text from a list of images
    @param: str: instruction
    @param: list: img_paths
    @return: list: messages
    '''
    async def extractTextFromImages(self, instruction, img_paths, img_type="png"):
        requests = list(map(lambda img_path: self.extractTextFromImage(instruction, img_path, img_type), img_paths))
        return await asyncio.gather(*requests)

    '''Utility to extract text from a list of images with a list of contexts
    @param: str: instruction
    @param: list: img_paths
    @param: list: contexts
    @return: list: messages
    '''
    async def extractTextFromImagesWithContexts(self, instruction, img_paths, contexts, img_type="png"):
        messages = []
        for index, img_path in enumerate(img_paths):
            context = contexts[index] if type(contexts[index]) == list else [contexts[index]]
            self.addContext(context)
            msg = await self.extractTextFromImage(instruction, img_path, img_type)
            messages.append(msg)
            self.clearContext()
        return messages

    '''Utility to extract text from specific pages
    @param: list: pages (filter)
    @param: list: prompts
    @param: str: instruction
    @param: list: context
    @return: list: messages
    '''
    def extractTextFromFilteredPromptsWithContext(self, pages, prompts, instruction, context):
        filtered_prompts = list(map(lambda page: prompts[page-1], pages))
        return self.requestWithContext(context, [
            *filtered_prompts,
            {
                "type": "text",
                "text": instruction
            },
        ])

    '''Utility to extract text via vectorstore
    @param: str: query
    @param: list: parts of text (data)
    @return: str, list: message, retrieved documents
    '''
    def similaritySearchWithContext(self, query, data, context, chunk_size=1000, k=25):
        # create text chunks
        documents = list(map(lambda item: DotMap({"page_content":item[1], "metadata": DotMap({"page": item[0]+1})}), enumerate(data)))
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
        splits = text_splitter.split_documents(documents)
        # init vectorstore
        vectorstore = Chroma()
        vectorstore.reset_collection()
        vectorstore = Chroma.from_documents(documents=splits, embedding=self.clientEmbeddings)
        retrieved_docs = vectorstore.similarity_search_with_relevance_scores(query, k=k)
        # extract text
        retrieved_text = list(map(lambda item: item[0].page_content, retrieved_docs))
        text_prompts = self.parser.text2prompts(retrieved_text)
        result = self.requestWithContext(context, [
            *text_prompts,
                {
                "type": "text",
                "text": query
            }
        ])
        return [result, retrieved_docs]
