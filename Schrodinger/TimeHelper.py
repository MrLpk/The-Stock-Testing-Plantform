#coding=utf-8

from datetime import datetime, timedelta
import time

class TimeHelper(object):
	"""docstring for TimeHelper"""
	def __init__(self):
		super(TimeHelper, self).__init__()
		self.m_pTime 	= datetime.today()
		self.m_pOneDay	= timedelta(days = 1)

	def addTime(self, day):
		days 			= timedelta(days = day)
		self.m_pTime 	= self.m_pTime + days

	def subTime(self, day = 1):
		if day == 1:
			self.m_pTime	= self.m_pTime - self.m_pOneDay
		else:
			days 			= timedelta(days = day)
			self.m_pTime 	= self.m_pTime - days

	def lastDay(self):
		self.subTime()

		return self.m_pTime.date()

	def currentDay(self):
		return self.m_pTime.date()

if __name__ == '__main__':
	helper 	= TimeHelper()

	for x in xrange(1,50):
		string = helper.lastDay()
		print string

