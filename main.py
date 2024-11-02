from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
os.environ['FLASK_ENV'] = 'development'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'merah'  # replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ugdt:ugdt@localhost/cred'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)  # New field for user role

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("user-auth.html")

@app.route('/auth/<oper>')
def auth(oper):
    if oper == "login":
        return render_template("user-auth.html")
    else:
        return render_template("register.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_type = request.form['user_type']
        if password != confirm_password:
            flash("Passwords do not match!", 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email address already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('username already exists', 'danger')
            return redirect(url_for('register'))

        # Create a new user instance
        new_user = User(username=username, email=email, password=password, user_type=user_type)

        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully!')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding user to the database.')
            print(e)  # Optional: Print the error for debugging

    return render_template('register.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        user = User.query.filter_by(username=username).first()
        
        if user and password==user.password:
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect((f'/dashboard/{str(user.user_type)}/{str(username)}'))
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('user-auth.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        email = request.form['email']
        permissionType = request.form['permissionType']
        dis = request.form['dis']
        return f"{name} {roll} {email} {dis} {permissionType}"
    else:
        return "nope"
        

@app.route('/dashboard/<oper>/<uname>')
def dashboard(oper, uname):
    # if oper is None or uname is None:
    #     return render_template("user-auth.html")
    if oper == "student":
        return render_template("student.html")
    elif oper == "admin":
        return render_template("admin-dash.html")
    elif oper == "faculty":
        return render_template("approval-dash.html")

@app.route('/manage_roles')
def manage_roles():
    users = User.query.all()  # Fetch all users from the database
    return render_template('manage_roles.html', users=users)

@app.route('/delete_user/<username>', methods=['POST'])
def delete_user(username):
    user = User.query.get(username)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {username} has been deleted.', 'success')
    else:
        flash(f'User {username} not found.', 'error')
    return redirect(url_for('manage_roles'))

@app.route('/add_user',methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']

        if User.query.filter_by(email=email).first():
            flash('Email address already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('username already exists', 'danger')
            return redirect(url_for('register'))

        # Create a new user instance
        new_user = User(username=username, email=email, password=password, user_type=user_type)

        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully!')
            return redirect(url_for('admin-dash'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding user to the database.')
            print(e)  # Optional: Print the error for debugging

    return render_template('manage_roles.html')

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     session.pop('username', None)
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('login'))

@app.route('/track/')
def track():
    return render_template("tracking.html")

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404notfound.html"), 404

if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)