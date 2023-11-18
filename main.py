import csv
from agent import Agent
from crawler import Crawler
from pprint import pprint
from pymongo import MongoClient


############################################

def insert_into_mongo(list_of_dicts, mongo_uri="mongodb://root:example@localhost:27017/"):
    db_name="db"
    collection_name="Jobs"
    # Connect to the MongoDB instance
    client = MongoClient(mongo_uri)

    # Select the database and collection
    db = client[db_name]
    collection = db[collection_name]

    # Insert the documents
    if list_of_dicts:
        collection.insert_many(list_of_dicts)
    else:
        print("No data to insert.")

    # Close the connection
    client.close()


def load_sites():
    with open("urls.csv") as f:
        reader = csv.reader(f)
        next(reader)
        return [row[0] for row in reader]

####################################
job_agent = Agent(
    model="gpt-3.5-turbo-1106",
    organization="org-8Y92VdA7tV3akhIJIG5eFOI4",
)
crawler = Crawler()

websites = load_sites()
for url ,page_body in crawler.crawl(websites):
    result = job_agent.extract_jobs(page_body)
    insert_into_mongo(result)
