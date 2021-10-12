from sqlalchemy import Column, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite://")
session = sessionmaker(bind=engine)


class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)
    __table_args__ = (
        UniqueConstraint(
            "title", "author", name="title_author_unique_pair", sqlite_on_conflict="IGNORE"
        ),
    )


Base.metadata.create_all(bind=engine)
