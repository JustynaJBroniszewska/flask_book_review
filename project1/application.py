import os

from flask import Flask, session, render_template, request, abort, redirect, flash
from flask_login import LoginManager
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# User_account management
login = LoginManager(app)

# Routes

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login_post', methods=['GET', 'POST'])
def login_post():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return render_template('user_account.html')
    else:
        flash('wrong password!')
        return render_template('login.html')

@app.route("/login")
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('user_account.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@app.route("/user_account")
def user_account():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('user_account.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)