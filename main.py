from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
import re
# from flask import abort
import os
os.environ['FLASK_ENV'] = 'development'

app = Flask(__name__)

def escape_js(value):
    """Escape special characters for safe JavaScript insertion."""
    value = re.sub(r'\\', r'\\\\', value)
    value = re.sub(r'"', r'\"', value)
    value = re.sub(r"'", r"\'", value)
    value = re.sub(r'\n', r'\\n', value)
    value = re.sub(r'\r', r'\\r', value)
    return value
app.jinja_env.filters['escape_js'] = escape_js

UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'merah'  # replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ugdt:ugdt@localhost/cred'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # redirect to 'login' view if not authenticated
login_manager.login_message = "Please log in to access this page."

# Define the User model
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)  # New field for user role

    def get_id(self):
        return self.id

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            elif current_user.user_type != required_role:
                session.pop('_flashes', None)
                flash("Access denied: You do not have the required permissions.", "danger")
                return redirect(url_for('unauthorized'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/home')
@login_required
def home():
    return render_template("profile.html")

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
        session.pop('_flashes', None)
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
        # user_type = request.form['user_type']
        user = User.query.filter_by(username=username).first()
        session.pop('_flashes', None)
        if user and password==user.password:
            # session['username'] = user.username
            login_user(user)
            flash('Logged in successfully!', 'success')
            if user.user_type=="student":
                return redirect('/home')
            return redirect((f'/dashboard/{str(user.user_type)}/{str(username)}'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('user-auth.html')
# @app.route('/home')
# def home():
#     return render_template('profile.html')


@app.route('/download/<filename>')
def download_file(filename):
    directory = os.path.join(app.root_path, 'files')
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    name = request.form.get('name')
    roll = request.form.get('roll')
    discription = request.form.get('dis')
    type = request.form.get('type')
    email = request.form.get('email')

    file_path = "id.txt"
    with open(file_path, 'r') as file:
        current_value = int(file.read().strip())
    with open(file_path, 'w') as file:
        file.write(str(current_value+1))

    file = request.files['document']
    file_extension = os.path.splitext(file.filename)[1]
    file.filename = f"{current_value}{file_extension}"
    docname = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    filename = f"{current_value}.txt"
    with open(f"req/{filename}", 'w') as file:
        file.write(f"{current_value}\n{name}\n{roll}\n{discription}\n{email}\n{str(type)}\npending\n{docname}\n{current_user.username}\n")
    return redirect((f'/dashboard/student/1'))
        

@app.route('/dashboard/student/<uname>')
@login_required
@role_required('student')
def dbs(uname): 
    return render_template("student.html")

@app.route('/dashboard/admin/<uname>')
@login_required
@role_required('admin')
def dba(uname):
    return render_template("admin-dash.html")

@app.route('/dashboard/<oper>/<uname>/', defaults={'category': None})
@app.route('/dashboard/<oper>/<uname>/<category>')
@login_required
@role_required('faculty')
def dbf(oper, uname, category):
    request_contents = []
    REQUESTS_DIR = 'req'
    for filename in os.listdir(REQUESTS_DIR):
        filepath = os.path.join(REQUESTS_DIR, filename)
        if os.path.isfile(filepath):
            if os.path.isfile(filepath):
                with open(filepath, 'r') as file:
                    lines = file.read().splitlines()
                    request = {
                        'id': lines[0],
                        'name': lines[1],
                        'roll': lines[2],
                        'description': lines[3],
                        'email': lines[4],
                        'type': lines[5],
                        'status': lines[6],
                        'file_path': f"{lines[7]}"
                    }
                    if (category is not None):
                        if (category != "all"):
                            if (request['type'] != str(category)):
                                continue
                    if (request['status'] == "pending"):
                        request_contents.append(request)
    print(len(request_contents))
    return render_template('approval-dash.html', request_contents=request_contents)


@app.route('/manage_roles')
@login_required
@role_required('admin')
def manage_roles():
    users = User.query.all()  # Fetch all users from the database
    return render_template('manage_roles.html', users=users)

@app.route('/delete_user/<username>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(username):
    user = User.query.get(username)
    session.pop('_flashes', None)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {username} has been deleted.', 'success')
    else:
        flash(f'User {username} not found.', 'error')
    return redirect(url_for('manage_roles'))

@app.route('/add_user',methods=['POST'])
@login_required
@role_required('admin')
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        session.pop('_flashes', None)

        if User.query.filter_by(email=email).first():
            flash('Email address already exists', 'danger')
            return redirect(url_for('login'))
        
        if User.query.filter_by(username=username).first():
            flash('username already exists', 'danger')
            return redirect(url_for('login'))

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

@app.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html'), 403

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash("You've been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/track/')
def track():
    return render_template("tracking.html",user={"status":"","comment":""})

@app.route('/find',methods=['POST'])
def find():
    # url = request.referrer
    id=request.form['requestId']
    # print(os.getcwd())
    file_path ="req/"+str(id)+".txt"
    # print(file_path)
    if os.path.exists(file_path):
        print("geeting here")
        with open(file_path, 'r') as file:
            lines = file.readlines()
        if len(lines)>9:
            user={"status":lines[6],"comment":lines[9]}
        else:
            user={"status":lines[6],"comment":""}
    else:
        user={"status":"not found","comment":""}
    return render_template("tracking.html",user=user)

# @app.route('/responce/<id>/<result>/', defaults={'category': None})
@app.route('/responce/<id>/<result>/')
def responce(id, result):
    url = request.referrer
    file_path = f"req/{id}.txt"
    line_number = 6
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines[line_number] = str(result)+"\n"
    with open(file_path, 'w') as file:
        file.writelines(lines)
    # if (category is None):
    #     return redirect((f'/dashboard/faculty/{current_user.username}'))
    # return redirect((f'/dashboard/faculty/{current_user.username}/{category}'))
    return redirect(url)

@app.route('/history/<uname>')
@login_required
@role_required('student')
def history(uname):
    request_contents = []
    REQUESTS_DIR = 'req'
    for filename in os.listdir(REQUESTS_DIR):
        filepath = os.path.join(REQUESTS_DIR, filename)
        if os.path.isfile(filepath):
            if os.path.isfile(filepath):
                with open(filepath, 'r') as file:
                    lines = file.read().splitlines()
                    if lines[8] != str(uname):
                        continue
                    request = {
                        'id': lines[0],
                        'name': lines[1],
                        'roll': lines[2],
                        'description': lines[3],
                        'email': lines[4],
                        'type': lines[5],
                        'status': lines[6],
                        'file_path': f"{lines[7]}"
                    }
                    request_contents.append(request)
    print(len(request_contents))
    return render_template('history.html', request_contents=request_contents)

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404notfound.html"), 404

if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)