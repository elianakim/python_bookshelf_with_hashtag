# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import and_, or_, literal


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

def from_sql_rev(row):
    data = row.__dict__.copy()
    data.pop('_sa_instance_state')
    return data

# [START model]
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publishedYear = db.Column(db.Integer)
    imageUrl = db.Column(db.String(255), default = 'http://placekitten.com/200/300')
    description = db.Column(db.String(4096))
    createdBy = db.Column(db.String(255))
    createdPW = db.Column(db.String(20))  #password 

    def __repr__(self):
        return "<Book(title='%s', author=%s)>" % (self.title, self.author)
# [END model]

class Review(db.Model):
    __tablename__ = 'reviews'

    username = db.Column(db.String(20), primary_key=True)
    bookId = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(4096))
    tag1 = db.Column(db.String(30))
    tag2 = db.Column(db.String(30))
    tag3 = db.Column(db.String(30))


    def __repr__(self):
        return "<review(bookID:%s, rate:%d)>" % (self.bookId, self.rate)


# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Book.query
             .order_by(Book.title)
             .limit(limit)
             .offset(cursor))
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)
# [END list]

# [START list_review]
def list_review(limit = 10, cursor = None, book_id = None):
    cursor = int(cursor) if cursor else 0
    book_id = int(book_id) if book_id else -1 
    query = (Review.query
                .filter(Review.bookId == book_id)
                .limit(limit)
                .offset(cursor))
    print(query.all())
    reviews = builtin_list(map(from_sql_rev, query.all()))
    next_page = cursor + limit if len(reviews) == limit else None
    return (reviews, next_page)
# [END list_review]

# [START book_rate]
def book_rate(id):
    avg_rate = (db.session.query(db.func.avg(Review.rate).label('avgRate')).filter(Review.bookId == id).all())
    count = (db.session.query(db.func.count(Review.rate).label('cnt')).filter(Review.bookId == id).all())
    
    avg_rate = [ar.avgRate for ar in avg_rate]
    count = [c.cnt for c in count]
    return (avg_rate, count)
# [END book_rate]

# [START hashtag]
def hashtag(id):
    ht1 = (db.session.query(Review.tag1.label('tag')).filter(Review.bookId == id))
    ht2 = (db.session.query(Review.tag2.label('tag')).filter(Review.bookId == id))
    ht3 = (db.session.query(Review.tag3.label('tag')).filter(Review.bookId == id))
    hashtag = ht1.union_all(ht2, ht3).subquery()
    hashcnt = (db.session.query(hashtag.columns.tag.label('tag'), db.func.count(hashtag.columns.tag).label('count'))
                         .group_by(hashtag.columns.tag).subquery())
    top5 = (db.session.query(hashcnt.columns.tag)
                      .order_by(hashcnt.columns.count.desc())
                      .limit(5).all())
    return top5

# [END hashtag]    


# [START list]
def search_list(title, year, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    if (len(year) == 0):
        query = (Book.query
                 .filter(Book.title.contains(title))
                 .order_by(Book.id)
                 .limit(limit)
                 .offset(cursor))
    else:
        query = (Book.query
                     .filter(and_(Book.title.contains(title), Book.publishedYear == year))
                     .order_by(Book.id)
                     .limit(limit)
                     .offset(cursor))
    print(query.all())
    books = builtin_list(map(from_sql, query.all()))
    print(books)
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)
# [END list]


# [START search_hash]
def search_hash(hashtag, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0

    htresult =  (db.session.query(Review, Book)
                .filter(Review.bookId == Book.id)
                #.filter(or_(Review.tag1 == hashtag, Review.tag2 == hashtag, Review.tag3 == hashtag))
                .filter(or_(Review.tag1.ilike(r"%{}%".format(hashtag)), literal(hashtag).ilike(r"%{}%".format(Review.tag1))
                            ,Review.tag2.ilike(r"%{}%".format(hashtag)), literal(hashtag).ilike(r"%{}%".format(Review.tag2))
                            ,Review.tag3.ilike(r"%{}%".format(hashtag)), literal(hashtag).ilike(r"%{}%".format(Review.tag3))))
                ).subquery()
    idlist = (db.session.query(htresult.columns.bookId)).subquery()
    result = (db.session.query(htresult).with_entities(Book)
                        .filter(Book.id.in_(idlist))
                        .order_by(Book.id)
                        .limit(limit)
                        .offset(cursor))
    books = builtin_list(map(from_sql_rev, result.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)
# [END search_hash]

# [START read_book]
def read_book(id):
    result = Book.query.get(id)
    if not result:
        return None
    return from_sql(result)
# [END read_book]


# [START create_book]
def create_book(data):
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)
# [END create_book]

# [START create_review]
def create_review(data):
    review = Review(**data)
    db.session.add(review)
    db.session.commit()
    return from_sql_rev(review)
# [END create_book]

# [START update]
def update(data, id):
    book = Book.query.get(id)
    for k, v in data.items():
        setattr(book, k, v)
    db.session.commit()
    return from_sql(book)
# [END update]


def delete(id):
    Book.query.filter_by(id=id).delete()
    Review.query.filter_by(bookId=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
