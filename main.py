from agent import Agent
from crawler import Crawler
from pprint import pprint


job_agent = Agent(
    model="gpt-3.5-turbo-1106",
    organization="org-8Y92VdA7tV3akhIJIG5eFOI4",
)
crawler = Crawler()
for page in crawler.crawl():
    result = job_agent.extract_jobs(page)
    pprint(result)