from agent import Agent
from crawler import Crawler
import json
from json import JSONDecodeError
from pprint import pprint
import re


def load_json(json_str):
    try:
        json_str = json_str.strip("```").lstrip("json").replace('\n','')
        json_str = re.sub("\s+", ' ',json_str)
        return json.loads(json_str)
    except JSONDecodeError as e:
        return {}


job_agent = Agent(
    model="gpt-3.5-turbo-1106",
    organization="org-8Y92VdA7tV3akhIJIG5eFOI4",
    system_message="Review the given HTML page to identify and extract job information. The page may feature either one job listing or several. Adapt your parsing approach based on this variability.",
)
crawler = Crawler()
for page in crawler.crawl():
    result = job_agent.extract_jobs(page)
    jobs = load_json(result["output"])
    pprint(jobs)