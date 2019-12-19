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

menu = {'login':"Login",'signup':"Sign Up",'logout':"Logout"}

@app.route('/')
@app.route('/home')
def index():
    username = session.get('username')
    if username is None:
        return render_template("index.html",login=menu['login'], signup=menu['signup'])
    name = (db.execute("SELECT name FROM users WHERE username=:username",{'username':username}).fetchall())[0][0]
    return render_template("index.html",username=name, logout=menu['logout'])

@app.route('/login')
def login():
    if session.get('username') is None:
        return render_template('login.html',login=menu['login'], signup=menu['signup'])
    name = (db.execute("SELECT name FROM users WHERE username=:username",{'username':username}).fetchall())[0][0]
    return render_template("main.html",username=name, logout=menu['logout'])
    

@app.route('/reg')
def reg():
    return render_template("signup.html",login=menu['login'], signup=menu['signup'])

@app.route('/auth', methods=["POST"])
def auth():
    username = request.form.get("username")
    password = sha384(request.form.get("password").encode()).hexdigest()

    user = db.execute("SELECT * from users WHERE username=:username",
                        {'username':username}).fetchall()
    if len(user) == 0:
        return render_template("signup.html",message="User Not Exist Please Sign Up Here",login=menu['login'], signup=menu['signup'])
    
    if password == user[0][3]:
        session['username'] = username
        name = user[0][1]
        return render_template("main.html",username=name, logout=menu['logout'])
    else:
        return render_template('login.html',message="Invalid Used Id Or Password",login=menu['login'], signup=menu['signup'])


@app.route('/register', methods=["POST"])
def signup():
    # getting data input by user in the sign up form
    name = request.form.get("name")
    username = request.form.get("username")
    password = sha384((request.form.get("password")).encode()).hexdigest()

    #check weather user already exist or not
    user = db.execute("SELECT * FROM users WHERE username=:username",
                        {'username':username}).fetchall()
    
    if len(user)==0:
        db.execute("INSERT INTO users (name,username,password) VALUES (:name, :username, :password)",
                    {'name':name, 'username':username, 'password':password})
        db.commit()
        return render_template('login.html',message="signup successful",login=menu['login'], signup=menu['signup'])
    else:
        return render_template("signup.html", message="Username Already exist",login=menu['login'], signup=menu['signup'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    name = (db.execute("SELECT name FROM users WHERE username=:username",{'username':session['username']}).fetchall())[0][0]
    return render_template("main.html",username=name, logout=menu['logout'])


@app.route('/search', methods=["POST"])
def search():
    username = session.get('username')
    if username is None:
        return render_template("index.html",login=menu['login'], signup=menu['signup'])
    name = (db.execute("SELECT name FROM users WHERE username=:username",{'username':session['username']}).fetchall())[0][0]
    search_by = request.form.get("search_by")
    search_text = request.form.get("search_text")
    bookList =[]
    if search_by == 'isbn':
        books = db.execute("SELECT * FROM books WHERE isbn=:isbn",
                            {'isbn':search_text}).fetchall()
        if not books:
            return render_template("main.html",username=name,logout=menu['logout'],message="No book with specified ISBN Number")
        for book in books:
            book = dict(book)
            bookList.append(book)
        return render_template("main.html",username=name,logout=menu['logout'],books=bookList)
    
    search_text = "%"+search_text+"%"
    if search_by == 'author':
        books = db.execute("SELECT * FROM books WHERE author LIKE :search_text",
                            {'search_text':search_text}).fetchall()
        if not books:
           return render_template("main.html",username=name,logout=menu['logout'],message="No book with specified Author Name") 
        
        for book in books:
            book = dict(book)
            bookList.append(book)
        return render_template("main.html",username=name,logout=menu['logout'],books=bookList)

    if search_by == 'title':
        books = db.execute("SELECT * FROM books WHERE title LIKE :search_text",
                            {'search_text':search_text}).fetchall()
        
        if not books:
            return render_template("main.html",username=name,logout=menu['logout'],message="No book with specified Title")
        
        for book in books:
            book = dict(book)
            bookList.append(book)
        return render_template("main.html",username=name,logout=menu['logout'],books=bookList)

    return render_template("main.html",username=name, logout=menu['logout'])

@app.route('/book/<int:book_id>')
def book(book_id):
    username = session.get('username')
    if username is None:
        return render_template("index.html",login=menu['login'], signup=menu['signup'],message="Please Login First")
    book = db.execute("SELECT * FROM books WHERE book_id=:book_id",
                        {'book_id':book_id}).fetchall()
    book = dict(book[0])
    return render_template("book.html",book=book)

@app.route('/review')
def review():
    return