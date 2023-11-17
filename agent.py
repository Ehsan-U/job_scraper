import json
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, create_extraction_chain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

schema = {
    "properties": {
        "job_title": {"type": "string"},
        "job_description": {"type": "string"},
    },
    "required": ["job_title", "job_description"],
}


class Agent:

    def __init__(self, model: str = "gpt-3.5-turbo", organization: str = None, temperature: float = 0.0):
        self.llm = ChatOpenAI(
            organization=organization,
            model_name=model,
            temperature=temperature,
            request_timeout=30,
        )


    def extract_jobs(self, page: str) -> Dict:
        chain = create_extraction_chain(schema=schema, llm=self.llm)
        return chain.run(page)