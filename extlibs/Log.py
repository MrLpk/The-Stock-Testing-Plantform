#coding=utf8
from MTool import MTool
from Singleton import Singleton

class Log(Singleton):
	"""docstring for Log"""
	def __init__(self):
		super(Log, self).__init__()
		# self.logCache = []
		# self.m = ''
		self.checkAttr('logCache', [])
		self.checkAttr('m', '')
		
	def log(self, word):
		self.logCache.append(word)
		print word
		
	def saveLog(self, path):
		content = u''

		for x in self.logCache:
			content = content + str(x) + u'\n'

		self.m.save(path, content.encode('utf8'))
		self.logCache = []

	def logs(self, infos):
		for x in infos:
			self.log(x)
		