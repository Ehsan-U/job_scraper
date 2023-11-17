import hrequests
from tenacity import wait_exponential, retry
from hrequests import Response
from lxml.html.clean import Cleaner
from lxml.html import fromstring, tostring
from typing import Literal



class Crawler:

    def __init__(self, browser: Literal["chrome", "firefox"] = "chrome"):
        """
        Initializes a new instance of the Crawler class.

        Args:
            browser: The browser to mimic TLS fingerprints. Defaults to "chrome".
        """
        self.session = hrequests.Session(browser=browser)


    def clean(self, response: Response) -> str:
        """
        Cleans the HTML content of a response object by removing unwanted tags.

        Args:
            response: The response object containing the HTML content to be cleaned.

        Returns:
            str: The cleaned text content of the HTML.
        """
        if response and response.status_code == 200:
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
            response = self.session.get(url)
            return response
        except Exception as e:
            raise e


    def crawl(self):
        """
        Crawls a list of URLs and yields the cleaned response body for each URL.

        :return: A generator that yields the cleaned response body for each URL.
        """
        urls = ["https://tech4you.nl/vacatures/", "https://www.flexcoaches.com/vacature/productiemedewerker-7/"]
        for url in urls:
            response = self.fetch(url)
            body = self.clean(response)
            yield url, body





