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
@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/contact', methods=['POST','GET'])
def login_request():



   if request.method == 'POST':
        first_name = request.form['FirstName']
        last_Name = request.form['LastName']
        email = request.form['Email']
        number = request.form['Numbers']
        comment = request.form['Comments']
        
    conn = get_db_connection()
    conn.execute('INSERT INTO tbl_contact (first_name, last_name, email, phone_number, comments) VALUES (?, ?, ?, ?, ?)',
    (FirstName, LastName, Email, Numbers, Comments))
    conn.commit()
    conn.close()
    return 'true'
    
if __name__ == "__main__":
 app.run(debug=True)
