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

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')




@app.route('/register_request', methods=['POST','GET'])
def registerRequest():

    if request.method == 'POST':
        name = request.form['name']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']


    conn = get_db_connection()
    conn.execute('INSERT INTO tbl_users (first_name, last_name, email, password,supply_teacher) VALUES (?, ?, ?, ?,0)',
    (name, lastName, email, password))
    conn.commit()
    conn.close()
    return 'true'

if __name__ == "__main__":
 app.run(debug=True)
