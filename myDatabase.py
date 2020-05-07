from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from settings import DATABASE_URL
from werkzeug.security import check_password_hash, generate_password_hash

class MyDatabase:

    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.db = scoped_session(sessionmaker(bind=self.engine))

    def create_db_tables(self):
        metadata = MetaData(bind=self.engine)
        metadata.reflect(only=['books'])
        for c in metadata.tables:
            print(c)
        # self.books = metadata.tables['books'] #нужно??

        try:
            self.users = Table('users', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String),
                            Column('password', String)
                            # keep_existing=True  # we are keeping reflected table if it was previously created by setting in Table object initializer keep_existing flag to True
                            )

        except Exception as e:
            print(e)


        self.reviews = Table('reviews', metadata,
                             Column('id', Integer, primary_key=True),
                             Column('book_id', Integer,
                                    ForeignKey('books.id')),
                             Column('user_id', Integer,
                                    ForeignKey('users.id')),
                             Column('review', String),
                             Column('rating', Integer)
                            #  keep_existing=True
                             )

        try:
            metadata.create_all(self.engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    def print_all_data(self, table="", query=""):
        query = query if query != '' else "SELECT * FROM {};".format(table)
        print(query)

        result = self.db.execute(query)

        for row in result:
            print(row)  # print(row[0], row[1], row[2])
        result.close()
        print("\n")

    def check_user(self, username, password):
        #TODO password

        
        user = username.lower()
        res = self.db.execute("SELECT password FROM users WHERE name = :username",
                                         {"username": user}).fetchone()

        checking = check_password_hash(res["password"], password)
        if user and checking:
            return True
        else:
            return False

    def add_user(self, username, password):
        # check if we already have this user in db and add it

        username = username.lower()
        if self.db.execute("SELECT * FROM users WHERE name = :username", {"username": username}).rowcount == 0:
            # add user
            hashedPassword = generate_password_hash(
                password, method='pbkdf2:sha256', salt_length=8)
            self.db.execute("INSERT INTO users (name, password) VALUES (:name, :password)",
                            {"name": username, "password": hashedPassword})
            self.db.commit()
            return True
        else:
            #user is already in base
            return False

    def get_id(self, username):
        #get user id

        username = username.lower()
        try:
            id = self.db.execute("SELECT id FROM users WHERE name = :username",
                                 {"username": username}).scalar()
            print(id)
            return id
        except Exception as e:
            print(e)

    def search(self, query):
        #book search using user input

        return self.db.execute(
            "SELECT isbn, title, author FROM books WHERE title LIKE '%' || :query || '%'", {"query": query})
       

    def get_book(self, isbn):
        #get book info
        
        return self.db.execute(
            "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()


    def check_review(self, user_id, book_id):
        #check if user have already review for this book

        result = self.db.execute(
            "SELECT * FROM reviews WHERE user_id = :user_id and book_id=:book_id",
            {"user_id": user_id, "book_id": book_id})
        return result.rowcount == 0

    def add_review(self, book_id, user_id, review, rating):       
        #try to insert review
    
        try : 
            self.db.execute(
                "INSERT INTO reviews (book_id, user_id, review, rating) VALUES (:book_id, :user_id, :review, :rating)",
                {"book_id": book_id, "user_id": user_id, "review": review, "rating": rating})
        except Exception as e:
            print (e)
        # self.db.commit()

    def get_reviews(self, book_id):
        #Get a list of reviews for a particular book.

        try:
            result = self.db.execute(
                '''SELECT reviews.review, reviews.rating, users.name FROM reviews INNER JOIN users on users.id=reviews.user_id
                inner join books ON books.id=reviews.book_id where reviews.book_id= :book_id''',
                {"book_id": book_id})
            return result            
        except Exception as e:
            print(e)

