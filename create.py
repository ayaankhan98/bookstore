from models import *
from flask import Flask, render_template, request

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://hudvklvicrsftt:001855057c2e059c6f477371435a068a479dc3eb63ffc8622860e5c3f22aac5a@ec2-174-129-255-17.compute-1.amazonaws.com:5432/d1f056i6gfrfdd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()


if __name__=='__main__':
    with app.app_context():
        main()