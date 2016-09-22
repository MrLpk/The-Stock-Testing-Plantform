#coding=utf8

import sqlite3
from BaseData import BaseData

class DBHelper(object):
	"""docstring for DBHelper"""
	def __init__(self):
		super(DBHelper, self).__init__()

		self.lines	= open('cof.ini', 'r').readlines()
		self.connectDB()

	def connectDB(self):
		dbName		= self.lines[0].rstrip()
		self.conn 	= sqlite3.connect(dbName)
		self.cursor	= self.conn.cursor()

	def createTable(self):
		self.executeLine(1)
		self.executeLine(2)

	def createTableName(self):
		self.executeLine(3)
		self.executeLine(4)

	def insertData(self, datas):
		for data in datas:
			sql = data.getSQL()
			# print sql
			self.cursor.execute(sql)

		self.conn.commit()

	def executeLine(self, num):
		sql 		= self.lines[num]
		self.cursor.execute(sql)

	def close(self):
		self.cursor.close()
		self.conn.commit()
		self.conn.close()
