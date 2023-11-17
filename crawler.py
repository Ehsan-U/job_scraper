import hrequests
from tenacity import wait_exponential, retry
from hrequests import Response
from lxml.html.clean import Cleaner
from lxml.html import fromstring, tostring
from typing import Literal


class Crawler:

    def __init__(self, browser: Literal["chrome", "firefox"] = "chrome"):
        self.session = hrequests.Session(browser=browser)


    def clean(self, response: Response) -> str:
        if response.status_code == 200:
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
        try:
            response = self.session.get(url)
            return response
        except Exception as e:
            raise e
        return Response(status_code=404)


    def crawl(self):
        urls = ["https://tech4you.nl/vacatures/"]
        for url in urls:
            response = self.fetch(url)
            body = self.clean(response)
            yield body





