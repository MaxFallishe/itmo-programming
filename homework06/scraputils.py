from typing import Dict, List, Union

import requests
import lxml
from bs4 import BeautifulSoup  # type: ignore

last_url = "https://news.ycombinator.com/newest"


def get_last_url() -> str:
    return last_url


def extract_news(parser: BeautifulSoup) -> List[Dict[str, Union[str, int]]]:
    parse_flag_1 = "athing"
    news_list = []

    rows_in_table_of_hackernews_news = parser.table.find("table", {"class": "itemlist"}).findAll("tr")
    count_of_hackernews_news =  len(rows_in_table_of_hackernews_news)
    for i in range(count_of_hackernews_news):
        tr = rows_in_table_of_hackernews_news[i]
        if tr.get("class") is not None and parse_flag_1 in tr.get("class"):
            i += 1
            info_tr = rows_in_table_of_hackernews_news[i]

            main_link = tr.find("a", {"class": "storylink"})
            title = main_link.text
            title_href = main_link["href"]

            points_span = info_tr.find("span", {"class": "score"})
            points = int(points_span.text.replace(" points", "").replace(" point", ""))

            author_link = info_tr.find("a", {"class": "hnuser"})
            author = author_link.text

            comments_link = info_tr.findAll("a")[-1]

            comments_start_value = 0
            comments = comments_start_value
            if comments_link.text.find("comment") != -1:
                comments = int(
                    comments_link.text.replace("\xa0comments", "").replace("\xa0comment", "")
                )

            news_list.append(
                {
                    "author": author,
                    "comments": comments,
                    "points": points,
                    "title": title,
                    "url": title_href,
                }
            )

    return news_list


def extract_next_page(parser: BeautifulSoup) -> str:
    more_links = parser.find("a", {"class": "morelink"})
    return str(more_links["href"])


def get_news(url: str, n_pages: int = 1) -> List[Dict[str, Union[str, int]]]:
    global end_url

    news = []
    while n_pages:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1

    end_url = url

    return news
