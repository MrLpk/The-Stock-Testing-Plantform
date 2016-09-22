#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

''' 有保底的均线突破买入 '''

class B5(BaseBS):
	"""docstring for B5"""
	def __init__(self, ma = '20', atrKey = '20', atrTimes = 0.5):
		super(B5, self).__init__()
		ma = str(ma)
		atrKey = str(atrKey)
		atrTimes = float(atrTimes)

		self.formulas = [
			Formula(11, options = {'ma':ma}),
		]