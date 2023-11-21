from tenacity import wait_exponential, retry, stop_after_attempt
from playwright.sync_api import sync_playwright
from dataclasses import dataclass


from logger import logger


@dataclass
class Response:
    status_code: int
    text: str
    url: str



class Crawler:

    def __init__(self, headless: bool = True, timeout: int = 10):
        """
        Initializes a new instance of the Crawler class.

        Args:
            browser: The browser to mimic TLS fingerprints. Defaults to "firefox".
        """
        self.timeout = timeout * 1000
        self.headless = headless


    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
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
        Crawls a list of URLs and yields the cleaned response body for each URL.

        :return: A generator that yields the cleaned response body for each URL.
        """
        for url in urls:
            logger.info(f"Processing: {url}")
            response = self.fetch(url)
            yield response





