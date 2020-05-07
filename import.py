from settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
import csv
import traceback
from sqlalchemy.orm import scoped_session, sessionmaker


def create_books():
    #create table "books" and import data from books.csv

    engine = create_engine(DATABASE_URL)
    db = scoped_session(sessionmaker(bind=engine))
    metadata = MetaData()

    books = Table('books', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('isbn', String),
                    Column('title', String),
                    Column('author', String),
                    Column('publication_year', Integer),
                        )
    try:
        metadata.create_all(engine)
        print("Table created")
    except Exception as e:
        print("Error occurred during Table creation!")
        traceback.print_exc()
        print(e)

    with open('books.csv', 'r') as f:
        reader = csv.DictReader(f, delimiter=',') # Skip the header row automatically
        for row in reader:
            insert_query = "INSERT INTO books (isbn, title, author, publication_year) VALUES (:isbn, :title, :author, :publication_year)"
            print(row)
            db.execute(insert_query, {"isbn": row["isbn"], "title": row["title"],
                                      "author": row["author"], "publication_year": row["year"]})
        db.commit()


if __name__ == '__main__':
    create_books()


