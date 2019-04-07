from flask import Flask, flash, redirect, render_template, request, session, abort
from time import sleep
import os
import datetime
import sqlite3
import RPi.GPIO as GPIO
import security
 
app = Flask(__name__)

#connect to the security module for password authentication and creation
hashPsw = ""
userID = ""
ID = ""


#Setting up the GPIO pins for communicating with the board for controlling the arm
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

#Define which pin is for which drink
americanoPin = 31
cappuccinoPin = 33
lattePin = 35
teaPin = 37
 
@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html')
		
@app.route("/americanoWebOrder")
def americanoWebOrder():
	GPIO.output(americanoPin, GPIO.HIGH)
	sleep(1)
	GPIO.output(americanoPin, GPIO.LOW)
	con = sqlite3.connect('Users.db')
	cur = con.cursor()
	cur.execute("UPDATE USERS SET AMERICANO=AMERICANO+1 WHERE ID=?;", (ID,))
	return render_template('americanoWebOrder.html')
	
@app.route("/cappuccinoWebOrder")
def cappuccinoWebOrder():
	GPIO.output(cappuccinoPinPin, GPIO.HIGH)
	sleep(1)
	GPIO.output(cappuccinoPinPin, GPIO.LOW)
	con = sqlite3.connect('Users.db')
	cur = con.cursor()
	cur.execute("UPDATE USERS SET CAPPUCCINO=CAPPUCCINO+1 WHERE ID=?;", (ID,))
	return render_template('cappuccinoWebOrder.html')
	
@app.route("/latteWebOrder")
def latteWebOrder():
	GPIO.output(lattePin, GPIO.HIGH)
	sleep(1)
	GPIO.output(lattePin, GPIO.LOW)
	con = sqlite3.connect('Users.db')
	cur = con.cursor()
	cur.execute("UPDATE USERS SET LATTE=LATTE+1 WHERE ID=?;", (ID,))
	return render_template('latteWebOrder.html')
	
@app.route("/teaWebOrder")
def teaWebOrder():
	GPIO.output(teaPin, GPIO.HIGH)
	sleep(1)
	GPIO.output(teaPin, GPIO.LOW)
	con = sqlite3.connect('Users.db')
	cur = con.cursor()
	cur.execute("UPDATE USERS SET TEA=TEA+1 WHERE ID=?;", (ID,))
	return render_template('teaWebOrder.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
	password = request.form['psw']
	userID = request.form['id']
	try:
		con = sqlite3.connect('Users.db')
		cur = con.cursor()
		cur.execute("SELECT ID FROM USERSPASS WHERE UserID=?;", (userID,))
		ID = cur.fetchall()
		cur.execute("SELECT PassHash FROM USERSPASS WHERE UserID=?;", (userID,))
		passHash = cur.fetchall()
		if password == passHash:
			session['logged_in'] = True
			print ("Hey ya!")
		else:
			flash('wrong password!')
		return home()
	except:
		return home()

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=80)
