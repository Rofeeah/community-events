# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request, redirect
from flask_pymongo import PyMongo
from flask import session
import os

# -- Initialization section --
app = Flask(__name__)

# events = [
#         {"event":"First Day of Classes", "date":"2019-08-21"},
#         {"event":"Winter Break", "date":"2019-12-20"},
#         {"event":"Finals Begin", "date":"2019-12-01"}
#     ]

# name of database
app.secret_key = os.getenv('SECRET_KEY')
uri = os.getenv('PASSWORD')
app.config['MONGO_DBNAME'] = 'database'

# URI of database
app.config['MONGO_URI'] = f'mongodb+srv://admin:{uri}@cluster0.njpjs.mongodb.net/database?retryWrites=true&w=majority'

mongo = PyMongo(app)
# app.secret_key = 'J\xf3\xa99\x16E\xbe\xfaZ\xaaX\x804g\x12\x96'

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    # session.clear()
    events = mongo.db.events
    events = events.find({})
    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database
    events = mongo.db.events2
    # insert new data
    events.insert({"event": "first day of school in nyc","date": "2021-09-13"})
    events.insert({"event": "Rofeeah goes off to college!","date": "2021-08-29"})
    # return a message to the user
    return "event added"

@app.route('/events/new',methods = ["GET","POST"])
def new_events():
    if request.method == "GET":
        return render_template("newevent.html")
    else:
        event_name = request.form["event_name"]
        event_date = request.form["event_date"]
        user_name = request.form["user_name"]
        events = mongo.db.events
        events.insert({
            "events": event_name,
            "date": event_date,
            "user": user_name
        })
        return redirect("/")


@app.route("/signup",methods =["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        users = mongo.db.users
        user = {
            "username": request.form["username"],
            "password": request.form["password"]
        }
        # checks if the username already exists in the database
        existing_user = users.find_one({"username": user["username"]})
        # make condition to check if username already exists in mongo
        if existing_user is None:
            # adds our user data into mogo
            users.insert(user)
            # tell the browser session who the user is
            session["username"] = request.form["username"]
            return render_template("index.html")
        else:
            return "That username is taken."

@app.route("/logout",methods =["GET","POST"])
def logout():
    # removes session
    session.clear()
    return redirect("/")

@app.route("/login",methods =["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        users = mongo.db.users
        user = {
            "username": request.form["username"],
            "password": request.form["password"]
        }
        # checks if the username already exists in the database
        existing_user = users.find_one({"username": user["username"]})
        # make condition to check if username already exists in mongo
        if existing_user:
            # if it does exist, check if the password matches
            if user['password'] == existing_user['password']:
                session['username'] = user['username']
                return redirect('/')
            else:
                error = "That is not the correct password."
                return render_template('login.html', error = error)

                # tell the browser session who the user is
                # session["username"] = request.form["username"]
                # return render_template("index.html")
        else:
            return "That username does not exist. Make sure to sign up!"

