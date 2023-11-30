from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_transformers import Html2TextTransformer
from langchain.docstore.document import Document
from langchain.callbacks import get_openai_callback
from typing import Dict, List
from dotenv import load_dotenv
import logging

from crawler import Response
load_dotenv()
logging.getLogger("langchain").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


class Agent:
    """
    A class that represents an agent that can extract job information from a given HTML page using OpenAI API.
    """

    schema: Dict = {
        "properties": {
            "job_title": {"type": "string"},
            "job_description": {"type": "string"},
            "job_page_url": {"type": "string"},
        },
        "required": ["job_title", "job_description", "job_page_url"],
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
            max_retries=3
        )


    def clean(self, response: Response) -> str:
        """
        Cleans the HTML content of a response object by removing unwanted tags.

        Args:
            response: The response object containing the HTML content to be cleaned.

        Returns:
            str: The cleaned text content of the HTML.
        """
        if response:
            html2text_obj = Html2TextTransformer(ignore_links=False)
            docs = html2text_obj.transform_documents([
                Document(page_content=response.text, metadata={"source": response.url})
            ])
            return docs[0].page_content + ' ' + response.url 
        else:
            return ""


    def extract_jobs(self, response: Response) -> List[Dict]:
        """
        Extracts job information from the given page using the extraction chain.

        Args:
            page (str): The HTML page to extract job information from.

        Returns:
            List: A list of dictionaries containing the extracted jobs information.
        """
        text = self.clean(response)

        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=15360,
            chunk_overlap=0,
        )
        splits = splitter.split_text(text)

        chain = create_extraction_chain(schema=self.schema, llm=self.llm)

        combined_results = []
        with get_openai_callback() as cb:
            for split in splits:
                try:
                    split_results = chain.run(split)
                except Exception:
                    pass
                else:
                    combined_results.extend(split_results)

        return [{**result, "token_cost": str(round(cb.total_cost, 3))} for result in combined_results if result]
