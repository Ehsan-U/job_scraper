from tenacity import wait_exponential, retry, stop_after_attempt
from playwright.sync_api import sync_playwright
from dataclasses import dataclass
from src.db import DB

from src.logger import logger


@dataclass
class Response:
    status_code: int
    text: str
    url: str

# t@VPQ595ycQ_#wL

class Crawler:

    def __init__(self, mysql: DB, headless: bool = True, timeout: int = 20):
            """
            Initializes the Crawler object.

            Args:
                mysql (DB): The MySQL database object.
                headless (bool, optional): Whether to run the browser in headless mode. Defaults to True.
                timeout (int, optional): The timeout value in seconds. Defaults to 10.
            """
            self.mysql = mysql
            self.timeout = timeout * 1000
            self.headless = headless


    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def fetch(self, url: str) -> Response:
            """
            Fetches the content of a web page.

            Args:
                url (str): The URL of the web page to fetch.

            Returns:
                Response: The response object containing the fetched content.

            Raises:
                Exception: If an error occurs during the fetching process.
            """
            try:
                with sync_playwright() as play:
                    browser = play.firefox.launch(headless=self.headless)
                    page = browser.new_page()
                    page.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())
                    page.goto(url, timeout=self.timeout)
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(self.timeout)
                    content = page.content()
                    page.close()
                return Response(status_code=200, text=content, url=url)
            except Exception as e:
                raise e


    def crawl(self, urls):
            """
            Crawls the given list of URLs and yields the response for each URL.

            Args:
                urls (list): A list of URLs to crawl.

            Yields:
                Response: The response object for each crawled URL.
            """
            for url in urls:
                exists_or_expired = self.mysql.lookup(url, table="individual")
                if not exists_or_expired:
                    logger.info(f"Processing: {url}")
                    response = self.fetch(url)
                    yield response
                else:
                    logger.info(f"Skipped (already exists): {url}")





