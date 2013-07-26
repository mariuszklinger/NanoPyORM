#!/usr/bin/python

"""
ORM styled class
"""

import MySQLdb

class Database():

	USER = None
	PASSWORD = None
	HOST = None
	DBNAME = None
	conn = None
	
	def __init__(self, h, u, p, dbname):
		self.USER = u
		self.PASSWORD = p
		self.HOST = h
		self.DBNAME = dbname
		
		self.conn = MySQLdb.connect(host=self.HOST, user=self.USER, passwd=self.PASSWORD, db=self.DBNAME)

db = Database("localhost", "root", "", "ex1")
		
class Table(): 
	
	db = None
	ID = None

	def __init__(self, db):
		self.db = db
		
	def __getitem__(self, k):
		return self
	
	@classmethod
	def select(cls):
		cursor = db.conn.cursor()
		cursor.execute("SELECT * FROM %s;" % cls.__name__)
		
		result_array = []
		for row in cursor.fetchall():
		
			result_array.append(cls(db, *row))
			
		return result_array
		
	@staticmethod
	def save(o):
		cursor = db.conn.cursor()
		sql = "INSERT INTO %s(%s) VALUES (%s);" % ((o.__class__.__name__,) + (",".join(o.values),) + (o.values_t,))

		format_array = []
		for key in  o.values:
			format_array.append(o.__dict__[key]) 
			
		cursor.execute(sql, tuple(format_array))
		db.conn.commit()
			

class Test(Table):
	"""
	create table test (
		id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		name varchar(15) not null, 
		age int not null, 
		job_title varchar(50) not null
	); 
	"""
	
	name = None
	age = None
	job_title = None
	
	#required configuration field needed by base (Table) class
	values = ("name", "age", "job_title")
	values_t = "%s, %s, %s"
	
	def __init__(self, db = None, id = None, name = None, age = None, job_title = None):

		self.ID = id
		self.name = name
		self.age = age
		self.job_title = job_title
		
		Table.__init__(self, db)
		
	def __str__(self):
		return "#%s\t{Name: %s, Age: %s, Job title: %s}" % (self.ID, self.name, str(self.age), self.job_title)

# ===========
#	DEMO
# ===========
if __name__ == "__main__":

	def printTestTable():
		for o in Test.select():
			print o

	print "\n\n\t\tBefore adding new record...\n\n"
			
	printTestTable()

	print "\n\n\t\tAdding new record...\n\n"

	t = Test(db)	
	t.age = 45
	t.name = "John"
	t.job_title = "Smith"
	Test.save(t)

	printTestTable()