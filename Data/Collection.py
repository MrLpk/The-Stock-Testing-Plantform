#coding=utf8

import os
from BaseData import BaseData
from DBHelper import DBHelper
from BaseName import BaseName

class Collection(object):
	"""docstring for Collection"""
	def __init__(self):
		super(Collection, self).__init__()
		self.db = DBHelper()
		self.db.createTable()
		self.db.createTableName()

	def start(self): 
		path = 'Res/txt'
		stockDatas = []
		nameDatas = []
		files = os.listdir(path)  
		for fCount, f in enumerate(files):
			fCount = fCount + 1
			name = BaseName(fCount, 0, '', f[:-4])
			nameDatas.append(name)
			lines = open(path+os.sep+f, 'r').readlines()
			for lineCount, line in enumerate(lines):
				print fCount, lineCount, line[:-4]
				words = line.split(',')
				data = BaseData(fCount, words[0], words[1], words[2], words[3], words[4], words[5], words[6].rstrip())
				stockDatas.append(data)

				if(len(stockDatas) >= 100000):
					self.db.insertData(stockDatas)
					stockDatas = []
				# break
			# break

		self.db.insertData(stockDatas)	
		self.db.insertData(nameDatas)
		print 'success...'
		
if __name__ == '__main__':
	c = Collection()
	c.start()
