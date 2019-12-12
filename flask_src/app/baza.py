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

    def __repr__(self):
        return (
            "book_id='%d', reader_id='%d', order_dater='%s', return_date='%s', rent_date='%s'"
            % (
                self.book_id,
                self.reader_id,
                self.order_date,
                self.return_date,
                self.rent_date,
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
        )

        self.session.add(req)
        self.session.commit()
        self.update_book_status(bookid, 'Rent')
        #TODO: zmienic status ksiazki na pozyczona.

    def update_book_status(self, bookID, newState):
        """
        updates book status.
        """

        book = self.session.query(Book).filter(id == bookID)
        book.state = newState
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

    #################################################
    def dry_test(self):
        """
        """

        book1 = Book(
            title="Szczerze",
            author="Tusk Donald",
            publisher="Agora",
            book_owner="Empik",
            isbn=33965284,
            pages=250,
            category="Biography",
            description="",
            state="Dostepna",
        )

        book2 = Book(
            author="Petitcollin Christel",
            title="Jak mniej myśleć. Dla analizujących bez końca i wysoko wrażliwych",
            publisher="Feeria",
            book_owner="Empik",
            isbn=31560139,
            pages=232,
            category="Psychology",
            description="",
            state="Dostepna",
        )

        reader1 = Reader(
            name="Marcin",
            surname="Iwaniuk",
            mail="MIwaniuk@luxoft.com",
            phone=503866282,
        )

        self.session.add(book1)
        self.session.add(book2)
        self.session.add(reader1)
        self.session.commit()

        zam = Order(
            book_id=book2.id,
            reader_id=reader1.id,
            order_date=date(2019, 12, 6),
            return_date=date(2020, 2, 14),
            rent_date=date(2019, 12, 29),
        )
        self.session.add(zam)
        self.session.commit()

        s = self.session.query(Book).all()
        print(s)


# q = session.query(Order).first()
# # print(dir(Order))
# # print(dir(q))
# b = session.query(Book).filter(Book.id == q.book_id).first()
# r = session.query(Reader).filter(Reader.id == q.reader_id).first()
# print(b.title)
# print(r.name)
# print(q.order_date)
# print(q.return_date)
# print(q.rent_date)
