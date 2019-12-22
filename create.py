from models import *
from flask import Flask, render_template, request

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:3gk9yy=l@localhost:5432/users"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()


if __name__=='__main__':
    with app.app_context():
        main()