from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
app = Flask(__name__)

app.config['SECRET_KEY'] = 'SuperSecretKey'

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


@app.route('/contact_request', methods=['POST','GET'])
def contact_request():

	if request.method == 'POST':
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		email = request.form['email']
		number = request.form['number']
		comment = request.form['comment']
  
	conn = get_db_connection()
	conn.execute('INSERT INTO tbl_contact (first_name, last_name, email, number, comment) VALUES (?, ?, ?, ?, ?)',
	(first_name, last_name, email, number, comment))
	conn.commit()
	conn.close()
	return 'Thanks for contacting us we will get back to you soon'

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
        (name, address, 'logo', email, phone_number, website, session['login']))
        conn.commit()
        conn.close()
        return 'True'
    return 'Failed to create school, please try again.'

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
            session['login'] = i['user_id']
            print(f"the email is:{email}")
            print(f"the pass is:{password}")
            return 'True'
    return 'email or password incorrect please try again'

@app.route('/logout')
def logout():
    session.pop('login', default=None)
    return redirect(url_for('homepage'))

@app.route('/register/user_select')
def user_select():

	user_id = session['login']

	conn = get_db_connection()
	name_row = conn.execute(f'SELECT first_name FROM tbl_users WHERE user_id = {user_id}')
	conn.close()

	for row in name_row:
		name = name_row['first_name']

	return render_template('user_select.html', title='User select', name=name)

if __name__ == "__main__":
	app.run(debug=True)
