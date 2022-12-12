from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
from werkzeug.utils import secure_filename
from markupsafe import escape

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'

def check_login():
	try:
		user_id = session['login']
	except KeyError:
		return False, None
	conn = get_db_connection()
	info = conn.execute(f'SELECT * FROM tbl_users WHERE user_id = {user_id}').fetchall()
	conn.close()
	for row in info:
		print (row['supply_teacher'])
		if row['supply_teacher'] != None:
			return True, 'teacher'
		elif row['school_id'] != None:
			return True, 'school'
		else:
			return True, None
	return False, None

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

	if check_login()[0] != True:
		return redirect(url_for('loginPage'))
	elif check_login()[1] != None:
		return redirect(url_for('homepage'))

	return render_template('create_school.html', schoolLogo = 'none')

@app.route('/register/school_request', methods=['POST', 'GET'])
def create_school_request():
	if request.method == 'POST':
		name = request.form['name']
		address = request.form['address']
		email = request.form['email']
		phone_number = request.form['phone_number']
		website = request.form['website']
		conn = get_db_connection()
		conn.execute('INSERT INTO tbl_schools (school_name, school_address, school_logo, school_email, school_phone_number, school_website,creator_user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
		(name, address, 'logo', email, phone_number, website, session['login']))
		conn.commit()
		id_row = conn.execute('SELECT school_id FROM tbl_schools WHERE school_name = ? AND creator_user_id = ?',
		(name, session['login'])).fetchall()
		school_id = id_row[-1]['school_id']
		user_id = session['login']
		conn.execute(f'UPDATE tbl_users SET school_id = {school_id} WHERE user_id = {user_id}')
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

	conn=get_db_connection()
	users = conn.execute('SELECT * FROM tbl_users').fetchall()
	conn.close()
	for row in users:
		if row['email'] == email:
			return 'Email is already in use'

	conn = get_db_connection()
	conn.execute('INSERT INTO tbl_users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)',
	(name, lastName, email, password))
	conn.commit()
	conn.close()

	conn=get_db_connection()
	users = conn.execute('SELECT * FROM tbl_users').fetchall()
	conn.close()

	for row in users:
		if row['email'] == email:
			session['login'] = row['user_id']

	return 'true'

@app.route('/login', methods=["POST","GET"])
def loginPage():
	return render_template('loginPage.html',title="Login Page")

@app.route('/login_request', methods=["POST","GET"])
def login_request():
	if request.method == 'POST':
		print("hello")
		print(request)
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

			if check_login()[1] == None:
				return 'register partially complete'

			return 'True'
	return 'email or password incorrect please try again'

@app.route('/logout')
def logout():
	session.pop('login', default=None)
	return redirect(url_for('homepage'))

@app.route('/register/user_select')
def user_select():

	if check_login()[0] != True:
		return redirect(url_for('loginPage'))
	elif check_login()[1] != None:
		return redirect(url_for('homepage'))

	user_id = session['login']

	conn = get_db_connection()
	name_row = conn.execute(f'SELECT first_name FROM tbl_users WHERE user_id = {user_id}').fetchall()
	conn.close()

	for row in name_row:
		name = row['first_name']

	return render_template('user_select.html', title='User select', name=name)
@app.route('/teacherProfile')
def teacherProfile():
	return render_template('teacherProfile.html')


@app.route('/user/<user_id>',methods=['POST','GET'])

def show_user_profile(user_id):
	if check_login()[0] != True:
		return redirect(url_for('loginPage'))
	print (str(user_id) != str(session['login'])) # true
	if str(user_id) != str(session['login']):
		return redirect(url_for('homepage'))

	print('OUTPUT:',user_id)

	conn=get_db_connection()
	id=escape(user_id)
	# sql_request = conn.execute(f'SELECT * FROM tbl_users WHERE user_id = {id}').fetchall()
	sql_request = conn.execute(f'SELECT * FROM tbl_users INNER JOIN tbl_teacher_keystages ON tbl_users.user_id = tbl_teacher_keystages.user_id INNER JOIN tbl_teacher_subjects ON tbl_users.user_id = tbl_teacher_subjects.user_id INNER JOIN tbl_teacher_description ON tbl_users.user_id = tbl_teacher_description.user_id WHERE tbl_users.user_id = {id}').fetchall()

	return render_template('teacherProfile.html',user_info = sql_request)


@app.route('/user/update', methods=['POST','GET'])
def update_profile():

	if request.method == 'POST':
		firstName = request.form['inputFName']
		lastName = request.form['inputLName']
		email = request.form['inputEmail']
		user_id = session["login"]
		keyStages=request.form['keyStages']

	print (firstName, lastName, email, user_id)

	conn = get_db_connection()

	conn.execute(f'UPDATE tbl_users SET first_name = ?, last_name = ?, email = ? WHERE user_id=?;', (firstName, lastName, email,user_id))
	conn.execute(f'UPDATE tbl_teacher_keystages SET key_stages = ? WHERE user_id=?;', (keyStages, user_id))
	print(user_id)
	conn.commit()
	conn.close()
	return 'true'

@app.route('/school_profile/<school_id>', methods=['POST','GET'])
def school_profile(school_id):
	print ('OUTPUT:',school_id)
	conn=get_db_connection()
	id = escape(school_id)
	school_info = conn.execute(f'SELECT * FROM tbl_schools WHERE school_id = {id}').fetchall()
	conn.close()
	return render_template('school_profile.html', title='School Profile', school_profile = school_info)


@app.route('/school_profile/update_school_info', methods=['POST','GET'] )
def update():
	if request.method == 'POST':
		school_name = request.form['school_name']
		school_address = request.form['school_address']
		school_logo = request.form['school_logo']
		school_email = request.form['school_email']
		school_phone_number = request.form['school_phone_number']
		school_website = request.form['school_website']
		school_id = request.form['school_id']
	try:
		conn = get_db_connection()
		conn.execute(f'UPDATE tbl_schools SET school_name = ?, school_address = ?, school_logo = ?, school_email = ?, school_phone_number = ?, school_website = ? WHERE school_id = ?',
		(school_name, school_address, school_logo, school_email, school_phone_number, school_website, school_id))
		conn.commit()
		conn.close()
		return "True"
	except:
		return "False"


if __name__ == "__main__":
	app.run(debug=True)
