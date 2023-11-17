import json
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class JobListing(BaseModel):
    Title: str = Field(description="The job title")
    Description: str = Field(description="The job description")

class JobListings(BaseModel):
    Jobs: List[JobListing] = Field(description="List of job listings")


class Agent:
    parser = PydanticOutputParser(pydantic_object=JobListings)

    def __init__(self, model: str = "gpt-3.5-turbo", organization: str = None, temperature: float = 0.0, system_message: str = "You are helpful assistant."):
        self.llm = ChatOpenAI(
            organization=organization,
            model_name=model,
            temperature=temperature,
            request_timeout=30,
        )
        self.system_message = system_message


    def extract_jobs(self, page: str) -> Dict:
        prompt = ChatPromptTemplate(
            input_variables=['page'],
            messages=[
                SystemMessagePromptTemplate.from_template(self.system_message.strip() + "\n{format_instructions}"),
                HumanMessagePromptTemplate.from_template("{page}")
            ],
            partial_variables={'format_instructions': self.parser.get_format_instructions()}
        )

        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            output_key='output',
        )

        return chain({
            "page": json.dumps(page)
        })