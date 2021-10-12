from typing import Any, List

from bottle import redirect, request, route, run, template  # type: ignore
from sqlalchemy.orm import Session
from bayes import NaiveBayesClassifier
from db import News, session
from scraputils import get_last_url, get_news


def get_news_list(s: Session) -> List[News]:
    return s.query(News).filter(News.label == None).all()


@route("/")
@route("/news")
def news_list() -> Any:
    s = session()
    rows = get_news_list(s)
    return template("news_template", rows=rows)


def add_label_to_db(s: Session, news_id: str, label: str) -> None:
    s.query(News).filter(News.id == news_id).update({"label": label})


@route("/add_label/")
def add_label() -> None:
    s = session()
    label = request.query.label
    news_id = request.query.id
    if label is not None:
            if news_id is not None:
                add_label_to_db(s, news_id, label)
                s.commit()
    redirect("/news")


def is_new_exists(s: Session, title: str, author: str) -> bool:
    return bool(s.query(News).filter(News.title == title, News.author == author).first())


def get_news_in_db(s: Session) -> None:
    count_of_getting_news = 1
    news = get_news(get_last_url(), count_of_getting_news)

    for new in news:
        if is_new_exists(s, str(new.get("title")), str(new.get("author"))):
            continue

        news_db = News(**new)
        s.add(news_db)


@route("/update")
def update_news() -> None:
    s = session()
    get_news_in_db(s)
    s.commit()
    redirect("/news")


def get_classified_news(
    s: Session,
) -> List[News]:
    _class_to_points = {
        "good": 1,
        "maybe": 0,
        "never": -1,
    }
    rows = s.query(News).filter(News.label != None).all()

    bayes_ml_model = NaiveBayesClassifier(0.05)
    bayes_ml_model.fit([row.title for row in rows], [row.label for row in rows])

    raw_rows = s.query(News).filter(News.label == None).all()
    classes = [_class_to_points[y] for y in bayes_ml_model.predict([row.title for row in raw_rows])]

    rows = [row for row, _class in sorted(zip(raw_rows, classes), key=lambda pair: pair[1], reverse=True)]
    return rows


@route("/classify")
def classify_news():
    s = session()
    rows = get_classified_news(s)
    return template("news_template", rows=rows)


if __name__ == "__main__":
    run(host="localhost", port=8080)
