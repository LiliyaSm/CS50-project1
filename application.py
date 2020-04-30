import os
from flask import Flask, session, render_template, request,  redirect, url_for
from flask_session import Session
import myDatabase

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


@app.route("/", methods=["POST", "GET"])
def index():
    if 'user_id' in session:
        return redirect(url_for("search"))

    username = request.form.get("username")
    password = request.form.get("password")
    if request.method == "POST":
        #проверка на пустые поля
        if not (username and password):
            return render_template("index.html", error="Заполните все поля!")
        #check in base
        success = db.check_user(username, password)
        if success:
            session["user_id"] = db.get_id(username)
            session["username"] = username

            print(session)
            # redirect to search page
            return redirect(url_for("search"))  
        else:
            return render_template("index.html", error="Incorrect username or password")

    return render_template("index.html")


@app.route("/signUp", methods=["POST", "GET"])
def signUp():
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method == "POST":
        if not (username and password):            
            return render_template("signUp.html", error="Заполните все поля!")
        print(username, password)

        success = db.add_user(username, password)
        #name already is in the base
        if not success:
            return render_template("signUp.html", error="This name is already in use! :( Choose another one.")
        else:

            session["user_id"] = db.get_id(username)
            session["username"] = username
            print(session)
            return redirect(url_for("search"))  # redirect on search page


    return render_template("signUp.html")


@app.route("/search")
def search():
    if 'user_id' in session:
        print(session)
        return render_template("search.html", username=session["username"])

    return redirect(url_for("index"))


@app.route('/sign_out')
def sign_out():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':

    app.jinja_env.auto_reload = True #дебаг и development если true то по идее работает и так 
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
