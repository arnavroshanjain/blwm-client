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

@app.route('/register/school')
def create_school():
    return render_template('create_school.html')

@app.route('/register/school_request', methods=['POST', 'GET'])
def create_school_request():
    
    if request.method == 'POST': 
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone_number = request.form['phone_number']
        # logo = request.files['logo']
        website = request.form['website']

        conn = get_db_connection()
        conn.execute('INSERT INTO tbl_schools (school_name, school_address, school_logo, school_email, school_phone_number, school_website,creator_user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (name, address, 'logo', email, phone_number, website, 1))
        conn.commit()
        conn.close()
        return 'True'

    return 'Failed to create school, please try again.'

if __name__ == "__main__":
 app.run(debug=True)
