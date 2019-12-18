from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Reader(Base):
    """
    Reader table definition
    """

    __tablename__ = "readersList"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    mail = Column(String)
    phone = Column(Integer)

    def __repr__(self):
        """
        string representation of reader record
        """

        return "name='%s', surname='%s', mail='%s', phone='%d'" % (
            self.name,
            self.surname,
            self.mail,
            self.phone,
        )


class Book(Base):
    """
    Book table definition
    """

    __tablename__ = "booksList"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publisher = Column(String, default="")
    book_owner = Column(String, default="Luxoft")
    isbn = Column(Integer)
    pages = Column(Integer)
    category = Column(String, default="")
    description = Column(String, default="")
    state = Column(String, default="Available")

    def __repr__(self):
        """
        string representation of book record
        """

        return (
                "Title= '%s', Author= '%s', Publisher= '%s', Book owner= '%s',ISBN= '%s', Pages= '%d', Genre= '%s', Details= '%s', State= '%s'\n"
                % (
                    self.title,
                    self.author,
                    self.publisher,
                    self.book_owner,
                    self.isbn,
                    self.pages,
                    self.category,
                    self.description,
                    self.state,
                )
        )


class Order(Base):
    """
    Book order table definition
    """

    __tablename__ = "ordersList"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("booksList.id"))
    reader_id = Column(Integer, ForeignKey("readersList.id"))
    order_date = Column(Date)
    return_date = Column(Date)
    rent_date = Column(Date)
    status = Column(String)

    def __repr__(self):
        """
        string representation of book order record
        """

        return (
                "book_id='%d', reader_id='%d', order_dater='%s', return_date='%s', rent_date='%s', status='%s'"
                % (
                    self.book_id,
                    self.reader_id,
                    self.order_date,
                    self.return_date,
                    self.rent_date,
                    self.status,
                )
        )


class Wish(Base):
    """
    Wishlist table definition
    """

    __tablename__ = "wishList"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publisher = Column(String)
    score = Column(Integer)  # how many workers want that book

    def __repr__(self):
        """
        string representation of book record
        """

        return (
                "Title= '%s', Author= '%s', Publisher= '%s', Score= '%d'\n"
                % (
                    self.title,
                    self.author,
                    self.publisher,
                    self.score,
                )
        )
