from flask import Flask, session, render_template, redirect, request, flash
import model

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
# app.jinja_env.undefined = jinja2.StrictUndefined



@app.route("/")
def index():
    #user_list = model.Session.query(model.User).limit(5).all()
    return render_template("signin_form.html")

@app.route('/signup', methods=["GET"])
def signup_user():
    return render_template('signup_form.html')

@app.route('/signup', methods=["POST"])
def add_user():
    email = request.form['email']
    gender = request.form['gender']
    password = request.form['password']
    age = request.form['age']
    zipcode = request.form['zip'] 
    occupation=request.form['occupation']
    user = model.User(email = email, password = password, occupation=occupation, age = age, zipcode = zipcode, gender = gender)
    user.add_user()
    return redirect("/")

@app.route("/", methods=["POST"])
def process_login():
    email = request.form['email']
    password=request.form['password']
    user = model.user_by_email(email, password) #add get user by email to model
    if user:
        session['user'] = [user.email, user.password]
        flash("Successfully logged in")
        return redirect('/home_page')
    else:
        flash("Account not found.")
        return redirect("/")

@app.route("/logout")
def process_logout():
    session.clear()
    flash("Successfully logged out")
    return redirect("/")

@app.route('/home_page')
def home_page():
    user=model.user_by_email(session['user'][0], session['user'][1])
    user_id=user.id
    ratings=model.Session.query(model.Rating).filter_by(user_id=user_id).all()
    return render_template('home_page.html', ratings=ratings)

@app.route('/user_list') 
def user_list():
    all_users=model.get_all_users()
    return render_template('user_list.html', all_users=all_users)

@app.route('/movie_list')
def movie_list():
    return render_template('movie_list.html')

@app.route('/users_ratings/<int:id>')
def display_users_ratings(id):
    ratings=model.Session.query(model.Rating).filter_by(user_id=id).all()
    return render_template('users_ratings.html', ratings=ratings, id=id)

@app.route('/rate_movie/<int:id>', methods = ['GET'])
def rate_movie_form(id):
    movie=model.Session.query(model.Movie).filter_by(id= id).one()
    print movie.name
    return render_template('rate_movie.html', movie = movie, id = id)

@app.route('/rate_movie/<int:id>', methods=['POST'])
def rate_movie(id):
    #Add an if statement to see if they've rated it before so they
    #can't rate the same movie twice.
    stars=request.form['rating']
    print stars
    user=model.user_by_email(session['user'][0], session['user'][1])
    print user
    user_id=user.id
    print user_id
    movie_id=id
    print movie_id
    new_rating=model.Rating(rating=stars, movie_id=movie_id, user_id=user_id)
    print new_rating
    new_rating.add_rating()
    return redirect('/home_page')


if __name__ == "__main__":
    app.run(debug=True)

