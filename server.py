from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
from datetime import date 
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

@app.route('/register/teacher', methods=['POST', 'GET'])
def register_teacher():

	if check_login()[0] != True:
		return redirect(url_for('signUp'))
	elif check_login()[1] != None:
		return redirect(url_for('homepage'))
	
	conn = get_db_connection()
	subjects = conn.execute('SELECT * FROM tbl_subjects').fetchall()
	user_info = conn.execute(f'SELECT * FROM tbl_users WHERE user_id = {session["login"]}').fetchall()
	conn.close()

	return render_template('register_teacher.html', subjects=subjects, user_info=user_info)

@app.route('/register/teacher_request', methods=['POST', 'GET'])
def register_teacher_request():



	if request.method == 'POST':  
		subject_ids = request.form['subject_ids']
		subject_ids = subject_ids.split(' ')
		teacher_description = request.form['teacher_description']
		ks_list = [request.form['ks1'],
				request.form['ks2'],
				request.form['ks3'],
				request.form['ks4'],
				request.form['ks5']]

	try:
		conn = get_db_connection()
		for id in subject_ids[:-1]:
			conn.execute(f'INSERT INTO tbl_teacher_subjects (subject_id, user_id) VALUES ({id}, {session["login"]})')
			conn.commit()
		for index, ks in enumerate(ks_list):
			if ks == 'true':
				keystage = index + 1
				conn.execute(f'INSERT INTO tbl_teacher_keystages (keystage, user_id) VALUES ({keystage}, {session["login"]})')
				conn.commit()
		conn.execute('INSERT INTO tbl_teacher_description (user_id, description) VALUES (?, ?)', (session["login"], teacher_description))
		conn.execute(f'UPDATE tbl_users SET supply_teacher = 1 WHERE user_id = {session["login"]}')
		conn.commit()
		conn.close()
		return 'true'
	except:
		return 'false'

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
	sql_request = conn.execute(f'SELECT * FROM tbl_users INNER JOIN tbl_teacher_keystages ON tbl_users.user_id = tbl_teacher_keystages.user_id INNER JOIN tbl_subjects ON tbl_teacher_subjects.subject_id=tbl_subjects.subject_id INNER JOIN tbl_teacher_subjects ON tbl_users.user_id = tbl_teacher_subjects.user_id INNER JOIN tbl_teacher_description ON tbl_users.user_id = tbl_teacher_description.user_id WHERE tbl_users.user_id = {id} GROUP BY tbl_teacher_subjects.subject_id').fetchall()
	keystages = conn.execute(f'SELECT * FROM tbl_teacher_keystages WHERE user_id = {session["login"]}').fetchall()
	description = conn.execute(f'SELECT * FROM tbl_teacher_description WHERE user_id = {session["login"]}').fetchall()
	user = conn.execute(f'SELECT * FROM tbl_users WHERE user_id = {session["login"]}').fetchall()
	subject_names = conn.execute(f'SELECT * FROM tbl_teacher_subjects AS ts INNER JOIN tbl_subjects AS s ON ts.subject_id = s.subject_id WHERE ts.user_id = {session["login"]}').fetchall()

	return render_template('teacherProfile.html',keystages = keystages, subject_names=subject_names, user=user, description=description, user_info = sql_request)


@app.route('/user/update', methods=['POST','GET'])
def update_profile():

	if request.method == 'POST':
		firstName = request.form['inputFName']
		lastName = request.form['inputLName']
		email = request.form['inputEmail']
		user_id = session["login"]
		keyStage=request.form['keyStages']
		# subject_id= request.form['subject_id']
		description= request.form['description']
		# subject_name=request.form['subject_name']

	print (firstName, lastName, email, user_id)

	conn = get_db_connection()

	conn.execute(f'UPDATE tbl_users SET first_name = ?, last_name = ?, email = ? WHERE user_id=?;', (firstName, lastName, email, user_id))
	conn.commit()
	conn.execute(f'UPDATE tbl_teacher_keystages SET keystage = ? WHERE user_id=?;', (keyStage, user_id))
	conn.commit()
	conn.execute(f'UPDATE tbl_teacher_description SET description = ? WHERE user_id=?;',(user_id, description))
	print(user_id)
	conn.commit()
	conn.close()
	return 'true'



	for row in school_id:
		current_id=row['school_id']
	conn.execute('INSERT INTO tbl_listings (school_id, listing_subject, listing_keystage, listing_date, listing_start_time, listing_end_time) VALUES (?,?, ?, ?, ?, ?)',
	(current_id, subject, keystage, calendar, startTime, endTime))
	conn.commit()
	conn.close()

	return render_template('jobListing.html')


@app.route('/listing', methods=['POST','GET'])
def listed():
	today = date.today()

	conn = get_db_connection()
	subs = conn.execute(f"SELECT * FROM tbl_subjects").fetchall()


	school_id = conn.execute(f'SELECT school_id FROM tbl_users WHERE user_id = {session["login"]}').fetchall()
	fields = conn.execute(f'SELECT * FROM tbl_listings WHERE school_id = {school_id[0]["school_id"]}').fetchall()
	conn.close()

	return render_template('jobListing.html', today=today,subs=subs,fields=fields)

@app.route('/listing_delete', methods=['GET', 'POST'])
def listing_delete():
	listed = request.form['lists']
	conn = get_db_connection()
	conn.execute(f'DELETE FROM tbl_listings WHERE listing_id = {listed}')
	conn.commit()
	conn.close()

	return redirect(url_for('listed'))

@app.route('/listing_request', methods=['POST','GET'])
def listing_request():
	if request.method == 'POST':
		subject = request.form['subject']
		keystage = request.form['keystage']
		calendar = request.form['date']
		startTime = request.form['startTime']
		endTime = request.form['endTime']

	conn = get_db_connection()
	school_id = conn.execute(f'SELECT school_id FROM tbl_users WHERE user_id = {session["login"]}').fetchall()

	for row in school_id:
		current_id=row['school_id']
	conn.execute('INSERT INTO tbl_listings (school_id, listing_subject, listing_keystage, listing_date, listing_start_time, listing_end_time) VALUES (?,?, ?, ?, ?, ?)',
	(current_id, subject, keystage, calendar, startTime, endTime))
	conn.commit()
	conn.close()

	return render_template('jobListing.html')

@app.route('/school_profile/<school_id>', methods=['POST','GET'])
def school_profile(school_id):
	print ('OUTPUT:',school_id)
	conn=get_db_connection()
	id = escape(school_id)
	school_info = conn.execute(f'SELECT * FROM tbl_schools WHERE school_id = {id}').fetchall()
	today = date.today()
	subs = conn.execute(f"SELECT * FROM tbl_subjects").fetchall()
	conn.close()
	return render_template('school_profile.html', title='School Profile', school_profile = school_info, today=today,subs=subs)
	

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
		
@app.route('/view_listings')
def view_listings():

	if check_login()[0] != True:
		return redirect(url_for('loginPage'))
	elif check_login()[1] != 'teacher':
		return redirect(url_for('homepage'))

	try:
		conn = get_db_connection()
		listings = conn.execute(f'SELECT * FROM tbl_teacher_subjects AS s INNER JOIN tbl_teacher_keystages AS k ON s.user_id = k.user_id INNER JOIN tbl_subjects ON s.subject_id = tbl_subjects.subject_id INNER JOIN tbl_listings AS l ON s.subject_id = l.listing_subject INNER JOIN tbl_listings AS l2 ON k.keystage = l2.listing_keystage INNER JOIN tbl_schools ON tbl_schools.school_id = l.school_id WHERE s.user_id = {session["login"]} AND l.accepted_by IS NULL GROUP BY l.listing_id').fetchall() 
		conn.close()
	except:
		return redirect(url_for('homepage'))

	return render_template('view_listings.html', listings = listings)

@app.route('/view_listings/accept_listing', methods=['GET', 'POST'])
def accept_listing():
	if request.method == 'POST':
		listing_id = request.form['listing_id']
	try:
		conn = get_db_connection()
		conn.execute(f'UPDATE tbl_listings SET accepted_by = {session["login"]} WHERE listing_id = {listing_id}')
		conn.commit()
		return 'true'
	except:
		return 'Failed to accept listing'
	finally:
		conn.close()
		

@app.route('/account')
def account():

	conn = get_db_connection()
	user = conn.execute(f'SELECT * FROM tbl_users WHERE user_id = {session["login"]}').fetchall()
	conn.close()

	user_type = check_login()
	print ('oskadok', user_type[1])
	if user_type[1] == 'teacher':
		return(redirect(url_for('show_user_profile', user_id = session['login'])))
	elif user_type[1] == 'school':
		return(redirect(url_for('school_profile', school_id=user[0]['school_id'])))
	else:
		return redirect(url_for('homepage'))

if __name__ == "__main__":
	app.run(debug=True)
