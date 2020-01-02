from datetime import datetime as date
from datetime import timedelta

import sqlalchemy
from sqlalchemy import and_, or_
from sqlalchemy.orm import sessionmaker
from tables import Order, Book, Reader, Base, Wish


class Baza:
    """
    class of handlers form db operations
    """

    def __init__(self):
        """
        """

        engine = sqlalchemy.create_engine(
            "sqlite:///sqlalchemy_test.db?check_same_thread=False", echo=True, convert_unicode=True
        )
        Base.metadata.create_all(engine)

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

### Books ###

    @staticmethod
    def __generate_table_footer():
        """
        """

        return "</tbody></table>"
    

    def get_all_books(self):
        books = self.session.query(Book).all()
        arr = list()
        for item in books:
            arr.append(item.serialized())
        return arr


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


    def add_book(self, params):
        """
        """

        book = Book(
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

        self.session.add(book)
        self.session.commit()
        return book.serialized()


    def delete_book(self, bookid):
        """
        """
        book = self.session.query(Book).filter_by(id=bookid).one()
        self.session.delete(book)
        self.session.commit()
        return book.serialized()

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
        return book.serialized()

### Readers ###

    def get_all_readers(self):
        users = self.session.query(Reader).all()
        arr = list()
        for item in users:
            arr.append(item.serialized())
        return arr


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
        return r.serialized()


    def delete_reader(self, reader_id):
        """
        """
        reader = self.session.query(Reader).filter_by(id=reader_id).one()
        self.session.delete(reader)
        self.session.commit()
        return reader.serialized()


    def update_reader(self, id, params):
        """
        """

        reader = self.session.query(Reader).filter(Reader.id == id).one()

        if params["name"]:
            reader.name = params["name"]
        if params["surname"]:
            reader.surname = params["surname"]
        if params["mail"]:
            reader.mail = params["mail"]
        if params["phone"]:
            reader.phone = params["phone"]
        
        self.session.commit()
        return reader.serialized()

### Orders ###

    def show_orders(self):
        """
        """

        s = self.session.query(Order).filter(Order.status == 'Active').all()

        table_header = '<table id="table" class="display">\
                        <thead>\
                        <tr>\
                        <th>No.</th>\
                        <th>Book title</th>\
                        <th>Reader Name</th>\
                        <th>Reader Surname</th>\
                        <th>Order date</th>\
                        <th>Return date</th>\
                        <th>Rent date</th>\
                        <th>Status</th>\
                        </tr>\
                        </thead>\
                        <tbody>'

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

        return_list += self.__generate_table_footer()

        return return_list


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


    def add_to_wishlist(self, params):
        """
        adding new book to whish list with starting score 1
        """

        wishes = Wish(
            title=params["title"],
            author=params["author"],
            publisher=params["publisher"],
            score=1,  # one on beginning
        )

        self.session.add(wishes)
        self.session.commit()

    def increment_score(self, title):
        """
        """

        # maybe we will choose it by book ID not title. since title must be exact same
        book = self.session.query(Wish.filter(Book.title == title)).one()

        book.score += 1
        self.session.commit()

    def show_wishlist(self):
        """
        """

        s = self.session.query(Wish).all()

        table_header = '<table id="table" class="display">\
                        <thead>\
                        <tr>\
                        <th>No.</th>\
                        <th>Book title</th>\
                        <th>Book author</th>\
                        <th>Publisher</th>\
                        <th>Score</th>\
                        </tr>\
                        </thead>\
                        <tbody>'

        return_list = table_header

        for item in s:
            return_list += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                str(item.id),
                item.title,
                item.author,
                item.publisher,
                item.score,
            )

        return_list += self.__generate_table_footer()

        return return_list
