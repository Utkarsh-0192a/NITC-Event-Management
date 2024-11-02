from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
import re

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

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("user-auth.html")

@app.route('/history/<uname>')
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
        file.write(f"{current_value}\n{name}\n{roll}\n{discription}\n{email}\n{str(type)}\npending\n{docname}")
    return redirect((f'/dashboard/student/1'))

@app.route('/download/<filename>')
def download_file(filename):
    directory = os.path.join(app.root_path, 'files')
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/dashboard/<oper>/<uname>/', defaults={'category': None})
@app.route('/dashboard/<oper>/<uname>/<category>')
def dashboard(oper, uname, category):
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

@app.route('/track/')
def track():
    return render_template("tracking.html")

@app.route('/responce/<id>/<result>')
def responce(id, result):
    file_path = f"req/{id}.txt"
    line_number = 6
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines[line_number] = str(result)+"\n"
    with open(file_path, 'w') as file:
        file.writelines(lines)
    return redirect((f'/dashboard/faculty/0'))

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404notfound.html"), 404

# # Open the file in read mode
# with open("example.txt", 'r') as file:
#     # Loop through each line in the file
#     for line in file:
#         print(line.strip())  # `strip()` removes extra whitespace and newline characters
