# prosta implementacja operacji na bazie danych z uzyciem
# biblioteki SQLAlchemy - pierwsze próby

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, and_, or_
from sqlalchemy import ForeignKey, func
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import datetime as date
from datetime import timedelta
import re


Base = declarative_base()


class Reader(Base):
    __tablename__ = "reader"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    mail = Column(String)
    phone = Column(Integer)

    def __repr__(self):
        return "name='%s', surname='%s', mail='%s', phone='%d'" % (
            self.name,
            self.surname,
            self.mail,
            self.phone,
        )


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    publisher = Column(String)
    book_owner = Column(String)
    isbn = Column(Integer)
    pages = Column(Integer)
    category = Column(String)
    description = Column(String)
    state = Column(String)

    def __repr__(self):
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
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"))
    reader_id = Column(Integer, ForeignKey("reader.id"))
    # book = relationship(Book)
    # reader = relationship(Reader)
    order_date = Column(Date)
    return_date = Column(Date)
    rent_date = Column(Date)
    status = Column(String)

    def __repr__(self):
        return (
            "book_id='%d', reader_id='%d', order_dater='%s', return_date='%s', rent_date='%s', status='%s'"
            % (
                self.book_id,
                self.reader_id,
                self.order_date,
                self.return_date,
                self.rent_date,
                self.status
            )
        )


class Baza:
    def __init__(self):
        """
        """

        engine = sqlalchemy.create_engine(
            "sqlite:///sqlalchemy_test.db", echo=True, convert_unicode=True
        )
        Base.metadata.create_all(engine)

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def show_books(self):
        """
        """

        s = self.session.query(Book).all()

        table_header = '<table style="width: 80%;" border="1">\
                        <tbody>\
                        <tr>\
                        <td>No.</td>\
                        <td>Title</td>\
                        <td>Author</td>\
                        <td>Publisher</td>\
                        <td>Book Owner</td>\
                        <td>ISBN</td>\
                        <td>Pages</td>\
                        <td>Genre</td>\
                        <td>Details</td>\
                        <td>Status</td>\
                        </tr>'
        table_footer = "</tbody></table>"

        return_list = table_header

        for item in s:
            return_list += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                str(item.id),
                item.title,
                item.author,
                item.publisher,
                item.book_owner,
                str(item.isbn),
                str(item.pages),
                item.category,
                item.description,
                item.state,
            )

        return_list += table_footer

        return return_list


    def show_users(self):
        """
        """

        s = self.session.query(Reader).all()

        table_header = '<table style="width: 80%;" border="1">\
                        <tbody>\
                        <tr>\
                        <td>No.</td>\
                        <td>Name</td>\
                        <td>surname</td>\
                        <td>Mail</td>\
                        <td>Phone</td>\
                        </tr>'
        table_footer = "</tbody></table>"

        return_list = table_header

        for item in s:
            return_list += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                str(item.id),
                item.name,
                item.surname,
                item.mail,
                str(item.phone),
            )

        return_list += table_footer
        print(return_list)
        return return_list

    def show_orders(self):
        """
        """

        s = self.session.query(Order).filter(Order.status == 'Active').all()

        table_header = '<table style="width: 80%;" border="1">\
                        <tbody>\
                        <tr>\
                        <td>No.</td>\
                        <td>Book title</td>\
                        <td>Reader Name</td>\
                        <td>Reader Surname</td>\
                        <td>Order date</td>\
                        <td>Return date</td>\
                        <td>Rent date</td>\
                        <td>Status</td>\
                        </tr>'
        table_footer = "</tbody></table>"

        return_list = table_header

        for item in s:

            b = self.session.query(Book).filter(Book.id == item.book_id).first()
            r = self.session.query(Reader).filter(Reader.id == item.reader_id).first()
            return_list += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                str(item.id),
                b.title,
                r.name,
                r.surname,
                item.order_date,
                item.return_date,
                item.rent_date,
                item.status
            )

        return_list += table_footer
        print(return_list)
        return return_list

    def add_book(self, params):
        """
        """

        b = Book(
            author=params["author"],
            title=params["title"],
            publisher=params["publisher"],
            book_owner=params["owner"],
            isbn=params["isbn"],
            pages=params["pages"],
            category=params["category"],
            description=params["description"],
            state=params["state"],
        )

        self.session.add(b)
        self.session.commit()

    def add_reader(self, params):
        """
        """

        r = Reader(
            name=params["name"],
            surname=params["surname"],
            mail=params["mail"],
            phone=params["phone"],
        )

        self.session.add(r)
        self.session.commit()

    def add_request(self, bookid, params):
        """
        """

        u = (self.session.query(Reader).filter(
                or_(
                    Reader.name.ilike("%{}%".format(params['name'])),
                    Reader.surname.ilike("%{}%".format(params['surname'])),
                )
            ).all())
        
        userid = u[0].id

        # b = self.session.query(Book).filter(Book.id == bookid)
        # bookid = b.bookid

        req = Order(
            book_id=bookid,
            reader_id=userid,
            order_date=date.now(),
            return_date=date.now() + timedelta(days=60),
            rent_date=date.now(),
            status='Active'
        )

        self.session.add(req)
        self.session.commit()
        self.update_book_status(bookid, 'Rent')
        #TODO: zmienic status ksiazki na pozyczona.

    def update_book_status(self, bookID, newState):
        """
        updates book status.
        """

        book = self.session.query(Book).filter(Book.id == bookID).one()
        book.state = newState
        self.session.commit()

    def return_book(self, rentID):
        """
        updates book status after return.
        """

        order = self.session.query(Order).filter(and_(Order.id == rentID, Order.status == 'Active')).one()
        book = self.session.query(Book).filter(Book.id == order.book_id).one()
        book.state = 'Available'
        order.status = 'Closed'
        self.session.commit()


    def delete_book(self, bookid):
        """
        """

        self.session.query(Book).filter_by(id=bookid).delete()
        self.session.commit()

    def update_book(self, id, params):
        """
        """

        book = self.session.query(Book).filter(Book.id == id).one()

        if params["title"]:
            book.title = params["title"]
        if params["author"]:
            book.author = params["author"]
        if params["publisher"]:
            book.publisher = params["publisher"]
        if params["owner"]:
            book.owner = params["owner"]
        if params["isbn"]:
            book.isbn = params["isbn"]
        if params["pages"]:
            book.pages = params["pages"]
        if params["category"]:
            book.category = params["category"]
        if params["description"]:
            book.description = params["description"]
        if params["state"]:
            book.state = params["state"]
        self.session.commit()

    def search(self, item):
        """
        """

        b = (
            self.session.query(Book)
            .filter(
                or_(
                    Book.title.ilike("%{}%".format(item)),
                    Book.author.ilike("%{}%".format(item)),
                    Book.description.ilike("%{}%".format(item)),
                    Book.publisher.ilike("%{}%".format(item)),
                )
            )
            .all()
        )

        table_header = '<table style="width: 80%;" border="1">\
                        <tbody>\
                        <tr>\
                        <td>No.</td>\
                        <td>Title</td>\
                        <td>Author</td>\
                        <td>Publisher</td>\
                        <td>ISBN</td>\
                        <td>Pages</td>\
                        <td>Genre</td>\
                        <td>Details</td>\
                        <td>Status</td>\
                        </tr>'
        table_footer = "</tbody></table>"

        return_list = table_header

        for item in b:
            return_list += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                str(item.id),
                item.title,
                item.author,
                item.publisher,
                str(item.isbn),
                str(item.pages),
                item.category,
                item.description,
                item.state,
            )

        return_list += table_footer
        return return_list


# Helpers
### THOSE ONEs DOENST HAVE SENSE TO BE EXTRACTED OUTSIDE FUCNTION. THEY ARE USED ONLY IN ONE FUNCTION EACH.
def book_table_header():
    return '<table style="width: 80%;" border="1">\
            <tbody>\
            <tr>\
            <td>No.</td>\
            <td>Title</td>\
            <td>Author</td>\
            <td>Publisher</td>\
            <td>Book Owner</td>\
            <td>ISBN</td>\
            <td>Pages</td>\
            <td>Genre</td>\
            <td>Details</td>\
            <td>Status</td>\
            </tr>'


def book_table_row(item):
    """
    """
    row = "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            str(item.id),
            item.title,
            item.author,
            item.publisher,
            item.book_owner,
            str(item.isbn),
            str(item.pages),
            item.category,
            item.description,
            item.state,
        )
    return row

def user_table_header():
    return '<table style="width: 80%;" border="1">\
            <tbody>\
            <tr>\
            <td>No.</td>\
            <td>Name</td>\
            <td>surname</td>\
            <td>Mail</td>\
            <td>Phone</td>\
            </tr>'

def user_table_row(item):
    return "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
            str(item.id),
            item.name,
            item.surname,
            item.mail,
            str(item.phone),
        )

table_footer = "</tbody></table>"

