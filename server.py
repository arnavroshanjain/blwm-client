from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('blwmDB.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/login', methods=["POST","GET"])
def loginPage():
    return render_template('loginPage.html',title="Login Page")

@app.route('/login_request', methods=["POST","GET"])
def login_request():
    print("test")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    conn=get_db_connection()
    users = conn.execute('SELECT * FROM tbl_users').fetchall()
    conn.close()

    for i in users:
        print(email,i["email"], password, i["password"])
        if email == i['email'] and password == i['password']:
            session['email'] = i['email']
            print(f"the email is:{email}")
            print(f"the pass is:{password}")
            return 'True'
    return 'email or password incorect please try again'


@app.route('/logout')
def logout():
    session.pop('userID', default=None)
    return redirect(url_for('home'))



if __name__ == "__main__":
 app.run(debug=True)
