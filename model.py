from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


# ENGINE = None
# Session = None

ENGINE = create_engine("sqlite:///ratings.db", echo = False)
Session = scoped_session(sessionmaker(bind = ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = Session.query_property()

### Class declarations go here

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    gender = Column(String, nullable = True)
    occupation = Column(String, nullable = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable = True)
    zipcode = Column(String(15), nullable=True)

    def add_user(self):
        Session.add(self)
        Session.commit()

def user_by_email(email, password):
    user = Session.query(User).filter_by(email=email).filter_by(password=password).first()
    return user

class Movie(Base):
    __tablename__="movies"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = True)
    released_at= Column(DateTime, nullable = True)
    imdb_url = Column(String, nullable = True)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = True)
    rating = Column(Integer, nullable = True)

    user = relationship("User", backref = backref("ratings", order_by = id))
    movie = relationship("Movie", backref = backref("ratings", order_by = id))



### End class declarations
# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///ratings.db", echo = True)
#     Session = sessionmaker(bind = ENGINE)

#     return Session()

def main():
    """In case we need this for something"""
    print 'sup my homies'

if __name__ == "__main__":
    main()
