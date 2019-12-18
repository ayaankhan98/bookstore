from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import sha384

app = Flask(__name__)
engine = create_engine("postgres://hudvklvicrsftt:001855057c2e059c6f477371435a068a479dc3eb63ffc8622860e5c3f22aac5a@ec2-174-129-255-17.compute-1.amazonaws.com:5432/d1f056i6gfrfdd")
db = scoped_session(sessionmaker(bind=engine))

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://hudvklvicrsftt:001855057c2e059c6f477371435a068a479dc3eb63ffc8622860e5c3f22aac5a@ec2-174-129-255-17.compute-1.amazonaws.com:5432/d1f056i6gfrfdd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/reg')
def reg():
    return render_template("signup.html")

@app.route('/auth', methods=["POST"])
def auth():
    session['username'] = request.form.get("username")
    session['password'] = sha384(request.form.get("password").encode()).hexdigest()

    user = db.execute("SELECT * from users WHERE username=:username",
                        {'username':session['username']}).fetchall()
    if len(user) == 0:
        return render_template("signup.html",message="User Not Exist Please Sign Up Here")
    
    if session['password'] == user[0][3]:
        return render_template("main.html",username=session['username'])


@app.route('/register', methods=["POST"])
def signup():
    # getting data input by user in the sign up form
    name = request.form.get("name")
    username = request.form.get("username")
    password = sha384((request.form.get("password")).encode()).hexdigest()

    #check weather user already exist or not
    user = db.execute("SELECT * from users WHERE username=:username",
                        {'username':username}).fetchall()
    
    if len(user)==0:
        db.execute("INSERT INTO users (name,username,password) VALUES (:name, :username, :password)",
                    {'name':name, 'username':username, 'password':password})
        db.commit()
        return render_template('login.html',message="signup successful")
    else:
        return render_template("signup.html", message="Username Already exist")


@app.route('/logout')
def logout():
    return


