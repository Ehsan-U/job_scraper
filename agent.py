from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
from typing import Dict
from dotenv import load_dotenv

load_dotenv()



class Agent:
    """
    A class that represents an agent that can extract job information from a given HTML page using OpenAI API.
    """

    schema = {
        "properties": {
            "job_title": {"type": "string"},
            "job_description": {"type": "string"},
        },
        "required": ["job_title", "job_description"],
    }


    def __init__(self, model: str = "gpt-3.5-turbo", organization: str = None, temperature: float = 0.0):
        """
        Initializes a new instance of the Agent class.

        Args:
            model (str): The name of the GPT-3 model to use. Defaults to "gpt-3.5-turbo".
            organization (str): The name of the OpenAI organization to use. Defaults to None.
            temperature (float): The temperature to use when generating responses. Defaults to 0.0.
        """
        self.llm = ChatOpenAI(
            organization=organization,
            model_name=model,
            temperature=temperature,
            request_timeout=30,
        )


    def extract_jobs(self, page: str) -> Dict:
        """
        Extracts job information from the given page using the extraction chain.

        Args:
            page (str): The HTML page to extract job information from.

        Returns:
            Dict: A dictionary containing the extracted job information.
        """
        chain = create_extraction_chain(schema=self.schema, llm=self.llm)
        return chain.run(page)
