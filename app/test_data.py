import baza
import random
from datetime import datetime as date
from datetime import timedelta

from tables import Book, Reader, Order

def add_test_data():
    add_db_items(generate_test_books())
    add_db_items(generate_test_readers())
    add_db_items(generate_test_orders())

def add_db_items(items):
    db = baza.Baza()
    for item in items:
        db.session.add(item)

    db.session.commit()

def generate_test_orders():
    db = baza.Baza()
    readers = db.session.query(Reader).all()
    books = db.session.query(Book).all()
    orders = list()
    for reader in readers:
        orders.append(Order(
            book_id=books[random.randint(0, len(books)-1)].id,
            reader_id=reader.id,
            order_date=date.now(),
            return_date=date.now() + timedelta(days=60),
            rent_date=date.now(),
            status="Active"
        )) 

    return orders

def generate_test_readers():
    return [
        Reader(
            name="Marcin",
            surname="Iwaniuk",
            mail="miwaniuk@luxoft.com",
            phone=12345,
        ),Reader(
            name="Jakub",
            surname="Stelmaszek",
            mail="JStelmaszek@luxoft.com",
            phone=123456,
        ),Reader(
            name="Nick",
            surname="Karpov",
            mail="mkarpov@luxoft.com",
            phone=1234567,
        )
    ]

def generate_test_books():
    books = [
        Book(
            title="Clean Code",
            author="Martin Robert",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="Death by Meeting",
            author="Lencioni Patrick",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="The Ideal Team Player",
            author="Lencioni Patrick",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="The Culture Map : Breaking Through the Invisible Boundaries of Global Business",
            author="Meyer Erin",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="Leadership",
            author="Goleman Daniel",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="Influence",
            author="Cialdini Robert",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="Linux Kernel Development 3e",
            author="Love Robert",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="First, Break All The Rules",
            author="Gallup Press",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="Getting Things Done",
            author="Allen David",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="Five Dysfunctions of a Team: A Leadership Fable",
            author="Lencioni Patrick",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="Go Put Your Strengths to Work",
            author="Buckingham Marcus",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="First Things First",
            author="Stephen R. Covey",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        ),
        Book(
            title="Getting to yes",
            author="William Ury , Fisher Roger",
            isbn=random.randint(1500,10000),
            pages=random.randint(15,1000)
        )
    ]
    return books