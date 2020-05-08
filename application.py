import os
from flask import Flask, session, render_template, request,  redirect, url_for, jsonify, flash
from flask_session import Session
import myDatabase
from goodreads import goodreads
from loginRequired import login_required

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
db = myDatabase.MyDatabase()
db.create_db_tables()
db.print_all_data("users")
db.print_all_data("reviews")


@app.route("/", methods=["POST", "GET"])
def index():
    #initial page with login fields

    if 'user_id' in session:
        return redirect(url_for("search"))

    username = request.form.get("username")
    password = request.form.get("password")
    if request.method == "POST":
        # check for empty fields
        if not (username and password):
            flash('Fill in all the fields!', 'danger')
            return render_template("index.html")
        #check in base
        success = db.check_user(username, password)
        if success:
            # add to session and redirect to search page
            session["user_id"] = db.get_id(username)
            session["username"] = username
            return redirect(url_for("search"))
        else:
            flash('Incorrect username or password', 'danger')
            return render_template("index.html")

    return render_template("index.html")


@app.route("/signUp", methods=["POST", "GET"])
def signUp():
    # Register user

    if 'user_id' in session:
        return redirect(url_for("search"))

    #get user input
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "POST":    
        #Ensure username and password was submitted
        if not (username and password):
            flash('Fill in all the fields!', 'danger')
            return render_template("signUp.html")
        print(username, password)

        success = db.add_user(username, password)
        if not success:
            # name already is in the base
            flash('This name is already in use! :( Choose another one.', 'danger')
            return render_template("signUp.html")
        else:
            # Store user log in info
            session["user_id"] = db.get_id(username)
            session["username"] = username

            flash('Account created', 'success')
            return redirect(url_for("search"))  # redirect on search page

    return render_template("signUp.html")


@app.route("/search",  methods=["GET"])
@login_required
def search():
    #Serching page

    # get user input
    query = request.args.get("search")
    if request.method == "GET" and query:
        result = db.search(query)
        return render_template("search.html", search=result)
    return render_template("search.html")


@app.route('/sign_out')
def sign_out():
    # Log user out 

    # remove the user id and username from the session if it's there, otherwise returns None
    #https://stackoverflow.com/questions/49510684/how-to-remove-session-flask-python3
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/book_page/<string:isbn>", methods=["POST", "GET"])
@login_required
def book_page(isbn):
    #individual book page

    # USER input
    review = request.form.get("review")
    rating = request.form.get("rating")

    #get reviews and book info from database
    book = db.get_book(isbn)
    reviews = db.get_reviews(book.id)
    review_counts = goodreads(isbn)

    # check if user has already review for this book
    no_review = db.check_review(session["user_id"], book.id)

    if request.method == "POST" and review and rating and no_review:
        # add review to the base
        db.add_review(book.id, session["user_id"], review, rating)
        reviews = db.get_reviews(book.id)
        flash('Review has been successfully submitted', 'success')
        return render_template("book_page.html", book=book, reviews=reviews, no_review=False, review_counts=review_counts)

    return render_template("book_page.html", book=book, reviews=reviews, no_review=no_review, review_counts=review_counts)


@app.route('/api/<isbn>')
@login_required
def book_api(isbn):
    # API returns ditails about a single book

    book = db.get_book(isbn)

    # make sure isbn exists
    if book is None:
        return jsonify({"error": "Invalid isbn"}), 404
    # get review info from goodreads
    review_counts = goodreads(isbn)

    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.publication_year,
        "isbn": isbn,
        "review_count": review_counts.get("work_ratings_count"),
        "average_score": review_counts.get("average_rating")
    })


if __name__ == '__main__':

    # Also "FLASK_DEBUG": "1" in launch.json
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
