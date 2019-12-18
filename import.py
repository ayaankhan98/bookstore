import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine("postgres://hudvklvicrsftt:001855057c2e059c6f477371435a068a479dc3eb63ffc8622860e5c3f22aac5a@ec2-174-129-255-17.compute-1.amazonaws.com:5432/d1f056i6gfrfdd")
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