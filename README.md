# CS50 project 1

This is a book review website. Users can register for a website and then log in using their username and password. Once they log in, they can search for books. On an individual book page, they can leave reviews for a book and see information about the book including the reviews made by other people. 
application.py - the main file contains all functions to render Flask pages. 
goodreads.py - file getting information by using Goodreads API.
import.py - creates a table and imports data from the CSV file.
login_required.py - login required decorator
myDatabase.py - creates tables and provides SELECT, INSERT and other database access commands.
The folder "templates" contains HTML files for rendering pages: search page, login page and so on. Layout.html contains an HTML skeleton of the header and body and displays the flashed messages if there are any.
