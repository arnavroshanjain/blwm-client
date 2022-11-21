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
    
if __name__ == "__main__":
 app.run(debug=True)
