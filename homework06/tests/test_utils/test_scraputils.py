import os
import unittest

import responses
from bs4 import BeautifulSoup  # type: ignore
from scraputils import extract_news, extract_next_page, get_news


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), "data/newest_example.html"), "r") as f:
            self.response_body = f.read()
        self.response = [
            {
                "author": "AUTHOR 1",
                "comments": 0,
                "points": 100,
                "title": "TITLE 1",
                "url": "URL 1",
            },
            {
                "author": "AUTHOR 2",
                "comments": 102,
                "points": 101,
                "title": "TITLE 2",
                "url": "URL 2",
            },
        ]
        self.parser = BeautifulSoup(self.response_body, "html.parser")

    def test_extract_news(self) -> None:
        self.assertEqual(self.response, extract_news(self.parser))

    def test_extract_next_page(self) -> None:
        response = "newest?next=NEXT"
        self.assertEqual(response, extract_next_page(self.parser))

    @responses.activate
    def test_get_news(self) -> None:
        responses.add(
            responses.GET, "https://news.ycombinator.com/", body=self.response_body, status=200
        )

        responses.add(
            responses.GET,
            "https://news.ycombinator.com/newest?next=NEXT",
            body=self.response_body,
            status=200,
        )

        response = self.response + self.response

        self.assertEqual(response, get_news("https://news.ycombinator.com/", 2))
