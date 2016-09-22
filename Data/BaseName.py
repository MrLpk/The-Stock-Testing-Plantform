#coding=utf8

class BaseName(object):
	"""docstring for BaseName"""
	def __init__(self, id, code, name, filename):
		super(BaseName, self).__init__()
		self.id = id
		self.code = code
		self.name = name
		self.filename = filename

	def getSQL(self):
		sql = '''insert into m_name values (%d, %d, '%s', '%s')''' %(self.id, self.code, self.name, self.filename)

		return sql
