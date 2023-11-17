from tenacity import wait_exponential, retry
from lxml.html.clean import Cleaner
from lxml.html import fromstring, tostring
from playwright.sync_api import sync_playwright
from dataclasses import dataclass

from logger import logger


@dataclass
class Response:
    status_code: int
    text: str



class Crawler:

    def __init__(self, headless: bool = True, timeout: int = 10):
        """
        Initializes a new instance of the Crawler class.

        Args:
            browser: The browser to mimic TLS fingerprints. Defaults to "firefox".
        """
        self.timeout = timeout * 1000
        self.headless = headless


    def clean(self, response: Response) -> str:
        """
        Cleans the HTML content of a response object by removing unwanted tags.

        Args:
            response: The response object containing the HTML content to be cleaned.

        Returns:
            str: The cleaned text content of the HTML.
        """
        if response:
            html = fromstring(response.text)

            cleaner = Cleaner()
            cleaner.javascript = True
            cleaner.scripts = True
            cleaner.comments = True
            cleaner.style = True
            cleaner.remove_tags = ['svg', 'img']

            html = cleaner.clean_html(html)

            body_elements = html.xpath("//body")
            if body_elements:
                return tostring(body_elements[0], method="html", encoding="unicode", pretty_print=True)
            else:
                return ""
        else:
            return ""


    @retry(wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch(self, url: str) -> Response:
        """
        Fetches the content of the given URL using the session object.

        Args:
            url: The URL to fetch.

        Returns:
            Response: The response object returned by the server.
        """
        try:
            with sync_playwright() as play:
                page = play.firefox.launch(headless=self.headless).new_page()
                page.route("**/*", lambda route: route.abort() if route.request.resource_type == "image"  else route.continue_())
                page.goto(url, timeout=self.timeout)
                content = page.content()
            return Response(status_code=200, text=content)
        except Exception as e:
            raise e


    def crawl(self, urls):
        """
        Crawls a list of URLs and yields the cleaned response body for each URL.

        :return: A generator that yields the cleaned response body for each URL.
        """
        for url in urls:
            logger.info(f"Processing: {url}")
            response = self.fetch(url)
            body = self.clean(response)
            yield url, body





