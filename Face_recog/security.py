import sqlite3
import hashlib 

con = sqlite3.connect('Users.db')
cur = con.cursor()

class Security():
	def __init__ (self, password, username):
		self.password = password
		self.username = username
		
	def hashPassword(self):
		password = self.password
		result = hashlib.md5(password.encode()) 
		self.password = result.hexdigest()
		return self.password

	def addPassword(self):
		s = Security(password, username)
		con = sqlite3.connect('Users.db')
		cur = con.cursor()
		cur.execute("UPDATE USERSPASS SET PassHash=? WHERE UserID=?;", (s.hashPassword(), self.username))
		con.commit()
