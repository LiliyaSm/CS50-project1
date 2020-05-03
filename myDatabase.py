from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from settings import DATABASE_URL


class MyDatabase:
    # engine = None
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.db = scoped_session(sessionmaker(bind=self.engine))

    def create_db_tables(self):
        metadata = MetaData()

        self.users = Table('users', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', String),
                           Column('password', String),
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
        user = username.lower()
        if self.db.execute("SELECT * FROM users WHERE name = :username", {"username": user}).rowcount == 1:
            return True
        else:
            return False

    def add_user(self, username, password):
        # check if we already have this user in db
        username = username.lower()
        if self.db.execute("SELECT * FROM users WHERE name = :username", {"username": username}).rowcount == 0:
            # add user
            self.db.execute("INSERT INTO users (name, password) VALUES (:name, :password)",
                            {"name": username, "password": password})
            self.db.commit()
            return True
        else:
            return False

    def get_id(self, username):
        username = username.lower()
        try:
            id = self.db.execute("SELECT id FROM users WHERE name = :username",
                                 {"username": username}).scalar()
            print(id)
            return id
        except Exception as e:
            print(e)

    def search(self, query):
        return self.db.execute(
            "SELECT isbn, title, author FROM books WHERE title LIKE '%' || :query || '%'", {"query": query})
        # OR title OR author

    def get_book(self, isbn):
        return self.db.execute(
            "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

    # def user_name(self, username):
    #     try:
    #         id = self.db.execute("SELECT id FROM users WHERE name = :username",
    #                                 {"username": username}).scalar()
    #         print(id)
    #         return id
    #     except Exception as e:
    #         print(e)

