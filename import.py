from settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import csv
from sqlalchemy.orm import scoped_session, sessionmaker


def books():
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
        print("Tables created")
    except Exception as e:
        print("Error occurred during Table creation!")
        print(e)

    with open('books.csv', 'r') as f:
        order = ["isbn", "title", "author", "publication year"]
        reader = csv.DictReader(f, fieldnames=order)
        next(reader)  # Skip the header row.
        reader = list(reader)
        for row in reader:
            insert_query = "INSERT INTO books (isbn, title, author, publication_year) VALUES (:isbn, :title, :author, :publication_year)"            
            print(row)
            db.execute(insert_query, {"isbn": row["isbn"], "title": row["title"], "author": row["author"], "publication_year": row["publication year"]})

    db.commit()
    

if __name__ == '__main__':
    books()


