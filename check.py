from sqlalchemy import create_engine
from flask import jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import sha384

engine = create_engine("postgresql://postgres:3gk9yy=l@localhost:5432/users")
db = scoped_session(sessionmaker(bind=engine))


def main():
    name = input("name : ")
    username = input("username : ")
    password = input("password :")
    #check weather user already exist or not
    user = db.execute("SELECT * from users WHERE username=:username",
                        {'username':username}).fetchall()
    
    print(user[0][3])
    if len(user)==0:
        db.execute("INSERT INTO users (name,username,password) VALUES (:name, :username, :password)",
                    {'name':name, 'username':username, 'password':password})
        db.commit()
        print("user registered")
    else:
        print("already exist")

if __name__=="__main__":
    main()