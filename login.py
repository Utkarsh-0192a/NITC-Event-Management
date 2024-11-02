from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
# //from werkzeug.security import generate_password_hash, check_password_hash

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
    #return "Hello"
    return render_template("user-auth.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_type = request.form['user_type']
        flash(username,password)
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
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
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('user-auth.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    return f"Hello, {session['username']}! Welcome to your dashboard."

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
