import model
import csv
import datetime


def load_users(session):
    users_data=open('seed_data/u.user')
    users_data = users_data.readlines()

    for line in users_data:
        row=line.split('|')
        i=row[0].decode("latin-1")
        a=row[1].decode('latin-1')
        g=row[2].decode('latin-1')
        o=row[3].decode('latin-1')
        z=row[4].decode('latin-1')
        user=model.User(id=i, age=a, gender=g, 
                  occupation=o, zipcode=z)

        session.add(user)
    session.commit()


def load_movies(session):

    movies_data=open('seed_data/u.item')
    movies_data = movies_data.readlines()
    
    for line in movies_data:
        row=line.split('|')
        if row[1] != "unknown":
            i=row[0].decode("latin-1")
            #the line below removes the dates from the movie titles 
            #and assigns the title to the variable 'n', in case you were curious
            n=row[1].decode('latin-1')[:-6]
            ra=row[2].decode('latin-1')
            release_date=datetime.datetime.strptime(ra,"%d-%b-%Y")
            imdb=row[3].decode('latin-1')

            movie=model.Movie(id=i, name=n, released_at=release_date, 
                  imdb_url=imdb)

            session.add(movie)

    session.commit() 



def load_ratings(session):

    ratings_data=open('seed_data/u.data')
    ratings_data = ratings_data.readlines()

    for line in ratings_data:
        row=line.split()
        ui=row[0].decode("latin-1")
        mi=row[1].decode('latin-1')
        r=row[2].decode('latin-1')

        rating=model.Rating(user_id=ui, movie_id=mi, rating=r)

        session.add(rating)
    session.commit()

def main(session):
   # load_users(session)
   # load_movies(session)
   # load_ratings(session)
   pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
