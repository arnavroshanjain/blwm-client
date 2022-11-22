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
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        for userID, user in dictUsers.items():
            if user['email'] == email and user['password'] == password:
                session['userID'] = userID
                return 'True'
    return 'Login failed'

@app.route('/logout')
def logout():
    session.pop('userID', default=None)
    return redirect(url_for('home'))



if __name__ == "__main__":
 app.run(debug=True)
