import scraputils
from bs4 import BeautifulSoup
import requests


def test_next_page_parser():
    url = "https://news.ycombinator.com/"
    for i in range(2, 5):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_url = scraputils.extract_next_page(soup)
        assert next_url == "news?p=" + str(i)
        url = "https://news.ycombinator.com/" + next_url
