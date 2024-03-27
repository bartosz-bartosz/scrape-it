import lxml.etree
import lxml.html
import unicodedata

import src.page

class PageContent:
    def __init__(
        self, url: str, status_code: int, headers: dict, body: bytes, raw_html: str
    ):
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.raw_html = raw_html

    @property
    def encoding(self) -> str | None:
        content_type = self.headers["content-type"].split(";")
        try:
            encoding = content_type[1].strip().split("=")[1].strip()
            return "latin1" if encoding == "latin-1" else encoding
        except IndexError:
            return None

    @property
    def html_tree(self) -> lxml.etree.ElementTree:
        tree_parser = lxml.html.HTMLParser(remove_comments=True, recover=True)
        normalized_html = unicodedata.normalize("NFKC", unquote(self.raw_html.strip()))
        return lxml.html.fromstring(normalized_html, parser=tree_parser)

