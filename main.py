from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    return "Hello"
    # return render_template("homepage.html")

@app.route('/auth/<oper>/<uname>/<passwd>')
def authEval(oper, uname, passwd):
    if oper == "login":
        return render_template("homepage.html")
    else:
        return render_template("homepage.html")

@app.route('/auth/<oper>')
def auth(oper):
    if oper == "login":
        return render_template("Login")
    else:
        return render_template("homepage.html")

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