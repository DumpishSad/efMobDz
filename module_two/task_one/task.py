from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class Genre(Base):
    __tablename__ = 'genre'
    genre_id = Column(Integer, primary_key=True)
    name_genre = Column(String, nullable=False)
    books = relationship('Book', back_populates='genre')


class Author(Base):
    __tablename__ = 'author'
    author_id = Column(Integer, primary_key=True)
    name_author = Column(String, nullable=False)
    books = relationship('Book', back_populates='author')


class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True)
    name_city = Column(String, nullable=False)
    days_delivery = Column(Integer, nullable=False)
    clients = relationship('Client', back_populates='city')


class Client(Base):
    __tablename__ = 'client'
    client_id = Column(Integer, primary_key=True)
    name_client = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('city.city_id'))
    email = Column(String, nullable=False)
    city = relationship('City', back_populates='clients')
    buys = relationship('Buy', back_populates='client')


class Book(Base):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('author.author_id'))
    genre_id = Column(Integer, ForeignKey('genre.genre_id'))
    price = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)
    author = relationship('Author', back_populates='books')
    genre = relationship('Genre', back_populates='books')
    buy_books = relationship('BuyBook', back_populates='book')


class Buy(Base):
    __tablename__ = 'buy'
    buy_id = Column(Integer, primary_key=True)
    buy_description = Column(String, nullable=True)
    client_id = Column(Integer, ForeignKey('client.client_id'))
    client = relationship('Client', back_populates='buys')
    buy_books = relationship('BuyBook', back_populates='buy')
    buy_steps = relationship('BuyStep', back_populates='buy')


class BuyBook(Base):
    __tablename__ = 'buy_book'
    buy_book_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    book_id = Column(Integer, ForeignKey('book.book_id'))
    amount = Column(Integer, nullable=False)
    buy = relationship('Buy', back_populates='buy_books')
    book = relationship('Book', back_populates='buy_books')


class Step(Base):
    __tablename__ = 'step'
    step_id = Column(Integer, primary_key=True)
    name_step = Column(String, nullable=False)
    buy_steps = relationship('BuyStep', back_populates='step')


class BuyStep(Base):
    __tablename__ = 'buy_step'
    buy_step_id = Column(Integer, primary_key=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    step_id = Column(Integer, ForeignKey('step.step_id'))
    date_step_beg = Column(DateTime, nullable=False)
    date_step_end = Column(DateTime, nullable=True)
    buy = relationship('Buy', back_populates='buy_steps')
    step = relationship('Step', back_populates='buy_steps')


DATABASE_URL = "postgresql://postgres:2362@localhost:5432/moduleTwo"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
