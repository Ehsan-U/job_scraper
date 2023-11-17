import hrequests
from tenacity import wait_exponential, retry
from hrequests import Response
from lxml.html.clean import Cleaner
from lxml.html import fromstring
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

            text = " ".join(html.xpath("//body//text()")).strip()
            return text
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
        urls = ["https://www.ppsc.gop.pk/Jobs.aspx", "https://www.flexcoaches.com/vacature/productiemedewerker-7/", "https://tech4you.nl/vacatures/"]
        for url in urls:
            response = self.fetch(url)
            body = self.clean(response)
            yield body





