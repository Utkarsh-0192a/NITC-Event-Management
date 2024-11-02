from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route('/login',methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def login():
    return render_template("tracking.html")


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    name = request.form.get('name')
    roll = request.form.get('roll')
    discription = request.form.get('dis')
    type = request.form.get('type')

    file_path = "id.txt"
    with open(file_path, 'r') as file:
        current_value = int(file.read().strip())
    with open(file_path, 'w') as file:
        file.write(str(current_value+1))

    file = request.files['document']
    file_extension = os.path.splitext(file.filename)[1]
    file.filename = f"{current_value}{file_extension}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    filename = f"{current_value}.txt"
    with open(f"req/{filename}", 'w') as file:
        file.write(f"{name}\n{roll}\n{discription}\n{str(type)}\npending")
    return "Hello"
        

@app.route('/dashboard/<oper>/<uname>')
def dashboard(oper, uname):
    if oper == "student":
        return render_template("student.html")
    elif oper == "admin":
        return render_template("admin-dash.html")
    elif oper == "faculty":
        request_contents = []
        REQUESTS_DIR = 'req'
        for filename in os.listdir(REQUESTS_DIR):
            filepath = os.path.join(REQUESTS_DIR, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r') as file:
                    content = file.read()
                    request_contents.append(content)
        
        return render_template('approval-dash.html', request_contents=request_contents)

@app.route('/track/')
def track():
    return render_template("tracking.html")

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404notfound.html"), 404

# # Open the file in read mode
# with open("example.txt", 'r') as file:
#     # Loop through each line in the file
#     for line in file:
#         print(line.strip())  # `strip()` removes extra whitespace and newline characters
