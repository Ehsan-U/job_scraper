from agent import Agent
from crawler import Crawler
from db import DB
import datetime
import random
from urllib.parse import urljoin


# Setup for the MySQL database connection
mysql = DB(
    server="localhost",
    user="user",
    password="pass",
    db="jobs",
    max_age = 2         # days
)
# List of websites to scrape job data from
websites = mysql.get_urls(table="urls")


# Initialize agent for job information extraction using a specific AI model
job_agent = Agent(
    model="gpt-3.5-turbo-1106",  # AI model identifier
    organization="org-8Y92VdA7tV3akhIJIG5eFOI4",  # Organization ID under which the model operates
)


# Initialize crawler for website scraping
crawler = Crawler(mysql)


def make_abs_url(base, url):
    if url:
        if url.startswith("http"):
            return url
        else:
            return urljoin(base, url)


# Iterate over websites to scrape job data
for response in crawler.crawl(websites):
    # Record the start time of the scraping process
    start_time = datetime.datetime.now()

    # Extract job information from the crawled response
    jobs = job_agent.extract_jobs(response)

    # Record the end time of the scraping process
    end_time = datetime.datetime.now()

    # Prepare job records for database insertion
    records = [
        (
            random.randint(1, 99999),  # Random ID for the job record
            job["job_title"],          # Extracted job title
            job["job_description"],    # Extracted job description
            job["token_cost"],         # Associated cost in tokens for the job
            start_time,                # Scraping process start time
            end_time,                  # Scraping process end time
            make_abs_url(response.url, job.get("job_page_url",'')),       # Extracted job page url
            response.url               # Source of the job
        )
        for job in jobs  # Loop through each job extracted
    ]

    # Insert the job records into the 'jobs' table of the database
    mysql.insert(records, table="jobs", duplicates_key=response.url)
    

