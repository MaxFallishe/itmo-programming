import random
import unittest
from typing import Dict, Union
from unittest.mock import MagicMock

import main
from main import add_label_to_db, get_classified_news, get_news_in_db, get_news_list
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, News


def sqlobject_to_dict(row: News) -> Dict[str, Union[str, int]]:
    d = dict(row.__dict__)
    d.pop("_sa_instance_state", None)
    return d


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        engine = create_engine("sqlite://")
        self.session = sessionmaker(bind=engine)
        Base.metadata.create_all(bind=engine)

    def test_func_news_list(self) -> None:
        session = self.session()
        raw_rows = get_news_list(session)
        self.assertEqual([], raw_rows)  # test empty

        # pre
        test_news = [
            {
                "author": "AUTHOR 1",
                "comments": 0,
                "points": 100,
                "title": "TITLE 1",
                "url": "URL 1",
                "label": None,
            },
            {
                "author": "AUTHOR 2",
                "comments": 102,
                "points": 101,
                "title": "TITLE 2",
                "url": "URL 2",
                "label": None,
            },
        ]
        for new in test_news:
            news_db = News(**new)
            session.add(news_db)
        session.commit()

        # exec and test
        rows = [sqlobject_to_dict(row) for row in get_news_list(session)]

        test_news = [
            {
                "id": 1,
                "author": "AUTHOR 1",
                "comments": 0,
                "points": 100,
                "title": "TITLE 1",
                "url": "URL 1",
                "label": None,
            },
            {
                "id": 2,
                "author": "AUTHOR 2",
                "comments": 102,
                "points": 101,
                "title": "TITLE 2",
                "url": "URL 2",
                "label": None,
            },
        ]
        self.assertEqual(test_news, rows)  # test filled

        # pre
        session.query(News).filter(News.id == 1).update({"label": "good"})
        test_news = [
            {
                "id": 2,
                "author": "AUTHOR 2",
                "comments": 102,
                "points": 101,
                "title": "TITLE 2",
                "url": "URL 2",
                "label": None,
            }
        ]

        # exec and test
        rows = [sqlobject_to_dict(row) for row in get_news_list(session)]
        self.assertEqual(test_news, rows)  # test filled and labeled

    def test_func_add_label(self) -> None:
        session = self.session()

        # pre
        test_news = [
            {
                "author": "AUTHOR 1",
                "comments": 0,
                "points": 100,
                "title": "TITLE 1",
                "url": "URL 1",
                "label": None,
            },
            {
                "author": "AUTHOR 2",
                "comments": 102,
                "points": 101,
                "title": "TITLE 2",
                "url": "URL 2",
                "label": None,
            },
        ]
        for new in test_news:
            news_db = News(**new)
            session.add(news_db)
        session.commit()

        # exec
        add_label_to_db(session, "1", "bad")
        session.commit()

        # test
        rows = [sqlobject_to_dict(row) for row in session.query(News).all()]
        test_news = [
            {
                "id": 1,
                "author": "AUTHOR 1",
                "comments": 0,
                "points": 100,
                "title": "TITLE 1",
                "url": "URL 1",
                "label": "bad",
            },
            {
                "id": 2,
                "author": "AUTHOR 2",
                "comments": 102,
                "points": 101,
                "title": "TITLE 2",
                "url": "URL 2",
                "label": None,
            },
        ]
        self.assertEqual(test_news, rows)  # test filled and labeled

    def test_func_update_news(self) -> None:
        # pre
        session = self.session()
        test_news = [
            {
                "author": "AUTHOR 1",
                "comments": 0,
                "points": 100,
                "title": "TITLE 1",
                "url": "URL 1",
                "label": None,
            },
            {
                "author": "AUTHOR 2",
                "comments": 102,
                "points": 101,
                "title": "TITLE 2",
                "url": "URL 2",
                "label": None,
            },
        ]
        main.get_news = MagicMock(
            return_value=test_news
        )  # module testing, replace get_news with mock function

        # exec
        get_news_in_db(session)

        # test
        rows = [sqlobject_to_dict(row) for row in session.query(News).all()]
        test_news = [
            {
                "id": 1,
                "author": "AUTHOR 1",
                "comments": 0,
                "points": 100,
                "title": "TITLE 1",
                "url": "URL 1",
                "label": None,
            },
            {
                "id": 2,
                "author": "AUTHOR 2",
                "comments": 102,
                "points": 101,
                "title": "TITLE 2",
                "url": "URL 2",
                "label": None,
            },
        ]
        self.assertEqual(test_news, rows)  # test filled

    def test_func_classify_news(self) -> None:
        # pre

        good_words = ["a", "b", "c"]
        maybe_words = ["d", "e", "f"]
        bad_words = ["j", "h", "i"]

        # train data

        good_title = " ".join(good_words)
        maybe_title = " ".join(maybe_words)
        bad_title = " ".join(bad_words)

        # test data

        # 3 random good titles
        good_titles = [" ".join([random.choice(good_words) for _ in range(2)]) for _ in range(3)]
        # 3 random good/maybe titles
        good_maybe_titles = [
            " ".join([random.choice(good_words), random.choice(maybe_words)]) for _ in range(3)
        ]
        # 3 random maybe titles
        maybe_titles = [" ".join([random.choice(maybe_words) for _ in range(2)]) for _ in range(3)]
        # 3 random good/bad titles
        maybe_bad_titles = [
            " ".join([random.choice(maybe_words), random.choice(bad_words)]) for _ in range(3)
        ]
        # 3 random bad titles
        bad_titles = [" ".join([random.choice(bad_words) for _ in range(2)]) for _ in range(3)]
        # all generated titles together
        test_titles = good_titles + good_maybe_titles + maybe_titles + maybe_bad_titles + bad_titles

        session = self.session()
        # init with train data
        test_news = [
            {
                "author": "1",
                "comments": 0,
                "points": 0,
                "title": good_title,
                "url": "",
                "label": "good",
            },
            {
                "author": "2",
                "comments": 0,
                "points": 0,
                "title": maybe_title,
                "url": "",
                "label": "maybe",
            },
            {
                "author": "3",
                "comments": 0,
                "points": 0,
                "title": bad_title,
                "url": "",
                "label": "never",
            },
        ]
        # fill with test data
        for title in test_titles:
            test_news.append(
                {
                    "author": str(len(test_news)),
                    "comments": 0,
                    "points": 0,
                    "title": title,
                    "url": "",
                    "label": None,
                }
            )
        random.shuffle(test_news)  # shuffle to add in random order

        for new in test_news:
            news_db = News(**new)
            session.add(news_db)
        session.commit()

        # exec
        rows = [row.__dict__.get("title") for row in get_classified_news(session)]

        # test
        good_index = rows.index(random.choice(good_titles))
        maybe_index = rows.index(random.choice(maybe_titles))
        bad_index = rows.index(random.choice(bad_titles))
        index_order_check = good_index < maybe_index < bad_index

        self.assertEqual(True, index_order_check)
