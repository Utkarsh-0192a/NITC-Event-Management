from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    return "Hello"
    # return render_template("homepage.html")


@app.route('/auth/<oper>', defaults={'user': None, 'uname': None, 'passwd': None})
@app.route('/auth/<oper>/<user>/<uname>/<passwd>')
def auth(oper, user, uname, passwd):
    if oper == "login":
        if uname and passwd:
            return render_template("login_test.html")
        return render_template("user-auth.html")
    else:
        if uname and passwd:
            return render_template("signup_test.html")
        return render_template("register.html")

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

@app.route('/admin-dashboard')
def admin_dashboard():
    return "<h1>dipanshutiwari115@gmail.com</h1>"

@app.route('/approval-dashboard')
def approval_dashboard():
    return "<h2>Approval Dashboard</h2>"

@app.route('/track/<trackid>')
def track_with_id(trackid):
    return f"<h2>No track ID: {trackid}</h2>"

@app.route('/track/')
def track():
    return "<h2>Enter ID:</h2>"

@app.route('/request-dashboard')
def request_dashboard():
    return "<h2>Request Dashboard</h2>"

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404notfound.html"), 404