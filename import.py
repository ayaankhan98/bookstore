import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine("postgresql://postgres:3gk9yy=l@localhost:5432/users")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn , :title, :author, :year)",
                    {'isbn':isbn , 'title':title , 'author':author, 'year':year})
        print(f"Added {isbn}, {title} by {author} in {year}")
    db.commit()

if __name__ == "__main__":
    main()