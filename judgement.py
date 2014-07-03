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
    print email
    password=request.form['password']
    print password
    user = model.user_by_email(email, password) #add get user by email to model
    print 'almost to the loop'
    if user:
        print "user=true!"
        print user.email
        session['user'] = [user.email, user.password]
        print session
        flash("Successfully logged in")
        return redirect('/user_list')
    else:
        print "No user"
        flash("Account not found.")
        return redirect("/")

@app.route("/logout")
def process_logout():
    session.clear()
    flash("Successfully logged out")
    return redirect("/")

@app.route('/user_list')
def user_list():
    return render_template('user_list.html')



if __name__ == "__main__":
    app.run(debug=True)

