from agent import Agent
from crawler import Crawler
from pprint import pprint


job_agent = Agent(
    model="gpt-3.5-turbo-1106",
    organization="org-8Y92VdA7tV3akhIJIG5eFOI4",
)
crawler = Crawler()

websites = ["https://www.flexcoaches.com/vacature/productiemedewerker-7/"]
for url ,page_body in crawler.crawl(websites):
    result = job_agent.extract_jobs(page_body)
    pprint(result)